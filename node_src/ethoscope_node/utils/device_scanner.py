from threading import Thread
import urllib2
import os
import datetime
import json
import time
import logging
import traceback
from functools import wraps

try:
    from scapy.all import srp, Ether, ARP
    _use_scapy = True
except ImportError:
    logging.warning("Cannot import scapy to scan subnet")
    _use_scapy = False


class ScanException(Exception):
    pass


def retry(ExceptionToCheck, tries=4, delay=3, backoff=2, logger=None):
    """Retry calling the decorated function using an exponential backoff.

    http://www.saltycrane.com/blog/2009/11/trying-out-retry-decorator-python/
    original from: http://wiki.python.org/moin/PythonDecoratorLibrary#Retry
    """
    def deco_retry(f):
        @wraps(f)
        def f_retry(*args, **kwargs):
            mtries, mdelay = tries, delay
            while mtries > 1:
                try:
                    return f(*args, **kwargs)
                except ExceptionToCheck as e:
                    time.sleep(mdelay)
                    mtries -= 1
                    mdelay *= backoff
            return f(*args, **kwargs)
        return f_retry
    return deco_retry



class DeviceScanner(Thread):
    _refresh_period = .5
    _filter_device_period = 5

    def __init__(self, local_ip = "192.169.123.1", ip_range = (6,100),device_refresh_period = 5, results_dir="/ethoscope_results"):
        self._is_active = True
        self._devices = {}
        self._device_id_map = {}
        self._device_id_list = {}
        self._local_ip = local_ip
        self._ip_range = ip_range
        self._use_scapy = _use_scapy

        for ip in  self._available_ips(local_ip, ip_range):
            self._devices[ip] = Device(ip, device_refresh_period, results_dir=results_dir)
            self._devices[ip].start()

        super(DeviceScanner, self).__init__()

    def _available_ips(self, local_ip, ip_range):
        if self._use_scapy :
            for c in self._arp_alive(local_ip):
                yield c
        else:
            for i in range(ip_range[0], ip_range[1] + 1):
                subnet_ip = local_ip.split(".")[0:3]
                subnet_ip = ".".join(subnet_ip)
                yield "%s.%i" % (subnet_ip, i)

    def _arp_alive(self, local_ip):
        try:
            if not self._use_scapy :
                raise Exception("Arp table can only be uses using scapy package")

            subnet_ip = local_ip.split(".")[0:3]
            subnet_address = ".".join(subnet_ip) + ".0/24"
            ans, unans = srp(Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=subnet_address), timeout=2, verbose=False)
            collection = [rcv.sprintf(r"%ARP.psrc%") for snd, rcv in ans]

            if len(collection) == 0:
                raise Exception("Empty ip list")
            return collection

        except Exception as e:
            logging.error("Cannot use scapy. Defaulting to subnet")
            logging.error(traceback.format_exc(e))
            self._use_scapy = False
            return []

    def run(self):
        last_device_filter_time = 0
        valid_ips = [ip for ip in self._available_ips(self._local_ip, self._ip_range)]
        while self._is_active :
            if time.time() - last_device_filter_time > self._filter_device_period:
                valid_ips = [ip for ip in self._available_ips(self._local_ip, self._ip_range)]
                last_device_filter_time = time.time()

            time.sleep(self._refresh_period)
            for d in self._devices.values():
                if d.ip() not in valid_ips:
                    d.skip_scanning(True)
                else:
                    d.skip_scanning(False)

                id = d.id()
                if id:
                    self._device_id_map[id] = d
                    self._device_id_list[id] = d.info()

    def get_device_list(self):
        return self._device_id_list

    def get_device(self, id):
        try:
            return self._device_id_map[id]
        except KeyError:
            raise KeyError("No such device: %s" % id)


    def stop(self):
        for d in self._devices.values():
            d.stop()
        self._is_active = False

class Device(Thread):
    _ethoscope_db_credentials = {"user": "ethoscope",
                                "passwd": "ethoscope",
                                "db":"ethoscope_db"}

    _id_page = "id"
    _user_options_page = "user_options"
    _static_page = "static"
    _controls_page = "controls"
    _allowed_instructions_status = { "start": ["stopped"],
                                     "start_record": ["stopped"],
                                     "stop": ["running", "recording"],
                                     "poweroff": ["stopped"]}

    def __init__(self,ip, refresh_period= 2, port = 9000, results_dir="/ethoscope_results"):
        self._results_dir = results_dir
        self._ip = ip
        self._port = port
        self._id_url = "http://%s:%i/%s" % (ip, port, self._id_page)
        self._id = ""
        self._info = {}
        self._is_active = True
        self._skip_scanning = False

        self._refresh_period = refresh_period

        super(Device,self).__init__()

    def run(self):
        last_refresh = 0
        while self._is_active:
            time.sleep(.2)
            if time.time() - last_refresh > self._refresh_period:
                self._update_info()
                last_refresh = time.time()

    def send_instruction(self,instruction,post_data):
        post_url = "http://%s:%i/%s/%s/%s" % (self._ip, self._port, self._controls_page,self._id, instruction)
        self._check_instructions_status(instruction)

        # we do not expect any data back when device is powered off.
        if instruction == "poweroff":
            try:
                self._get_json(post_url, 3, post_data)
            except ScanException:
                pass

        else:
            self._get_json(post_url, 3, post_data)
        self._update_info()

    def _check_instructions_status(self, instruction):
        self._update_info()
        status = self._info["status"]

        try:
            allowed_inst = self._allowed_instructions_status[instruction]
        except KeyError:
            raise KeyError("Instruction %s is not allowed" % instruction)

        if status not in allowed_inst:
            raise Exception("You cannot send the instruction '%s' to a device in status %s" %(instruction, status))

    def ip(self):
        return self._ip
    def id(self):
        return self._id
    def info(self):
        return self._info

    def skip_scanning(self, value):
        self._skip_scanning = value

    def user_options(self):
        user_options_url= "http://%s:%i/%s/%s" % (self._ip, self._port, self._user_options_page, self._id)
        out = self._get_json(user_options_url)
        return out

    def last_image(self):
        try:
            img_path = self._info["last_drawn_img"]
        except KeyError:
            raise KeyError("Cannot find last image for device %s" % self._id)
        img_url = "http://%s:%i/%s/%s" % (self._ip, self._port, self._static_page, img_path)
        file_like = urllib2.urlopen(img_url)
        return file_like

    def dbg_img(self):
        try:
            img_path = self._info["dbg_img"]
        except KeyError:
            raise KeyError("Cannot find dbg img path for device %s" % self._id)

        img_url = "http://%s:%i/%s/%s" % (self._ip, self._port, self._static_page, img_path)
        try:
            file_like = urllib2.urlopen(img_url)
            return file_like
        except Exception as e:
            logging.warning(traceback.format_exc(e))




    @retry(ScanException, tries=3, delay=1, backoff=1)
    def _get_json(self, url,timeout=2, post_data=None):

        try:
            req = urllib2.Request(url, data=post_data, headers={'Content-Type': 'application/json'})
            f = urllib2.urlopen(req, timeout=timeout)
            message = f.read()

            if not message:
                # logging.error("URL error whist scanning url: %s. No message back." % self._id_url)
                raise ScanException("No message back")
            try:
                resp = json.loads(message)
                return resp
            except ValueError:
                # logging.error("Could not parse response from %s as JSON object" % self._id_url)
                raise ScanException("Could not parse Json object")
        except urllib2.URLError as e:
            raise ScanException(str(e))
        except Exception as e:
            raise ScanException("Unexpected error" + str(e))


    def _update_id(self):
        if self._skip_scanning:
            raise ScanException("Not scanning this ip.")

        old_id = self._id
        resp = self._get_json(self._id_url)
        self._id = resp['id']
        if self._id != old_id:
            logging.warning("Device id changed!")
            self._info = {}

        self._info["ip"] = self._ip


    def _update_info(self):
        try:
            self._update_id()
        except ScanException:
            self._info["status"] = "not_in_use"
            return

        try:
            data_url = "http://%s:%i/data/%s" % (self._ip, self._port, self._id)
            resp = self._get_json(data_url)
            self._info.update(resp)
            resp = self._make_backup_path()
            self._info.update(resp)
            resp = self._get_last_backup_time(self._info["backup_path"])
            self._info.update(resp)
        except ScanException:
            pass

    def _get_last_backup_time(self, backup_path):
        try:
            time_since_backup = time.time() - os.path.getmtime(backup_path)
            return {"time_since_backup": time_since_backup}
        except OSError:
            return {"time_since_backup": "None"}
        except Exception as e:
            logging.error(traceback.format_exc(e))
            return {"time_since_backup": "None"}

    def _make_backup_path(self,  timeout=30):
        try:
            import MySQLdb
            device_id = self._info["id"]
            device_name = self._info["name"]
            com = "SELECT value from METADATA WHERE field = 'date_time'"

            mysql_db = MySQLdb.connect(host=self._ip,
                                       connect_timeout=timeout,
                                       **self._ethoscope_db_credentials)
            cur = mysql_db.cursor()
            cur.execute(com)
            query = [c for c in cur]
            timestamp = float(query[0][0])
            mysql_db.close()
            date_time = datetime.datetime.fromtimestamp(timestamp)
            formatted_time = date_time.strftime('%Y-%m-%d_%H-%M-%S')
            file_name = "%s_%s.db" % (formatted_time, device_id)
            output_db_file = os.path.join(self._results_dir,
                                          device_id,
                                          device_name,
                                          formatted_time,
                                          file_name
                                          )

        except Exception as e:
            logging.error("Could not generate backup path for device. Probably a MySQL issue")
            logging.error(traceback.format_exc(e))
            return {}

        return {"backup_path": output_db_file}

    def stop(self):
        self._is_active = False