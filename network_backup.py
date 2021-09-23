from netmiko import ConnectHandler
import datetime
import os


class Device:

    def __init__(self, device_type, host, username, password, secret, sh_conf, sh_int):
        self.sh_conf = sh_conf
        self.sh_int = sh_int
        self.switch = {
            'device_type': device_type,
            'host': host,
            'username': username,
            'password': password,
            'secret': secret
        }

    def backup_config(self):
        net_connect = ConnectHandler(**self.switch)
        net_connect.enable()
        config = net_connect.send_command(sh_conf)
        int_status = net_connect.send_command(sh_int)
        net_connect.disconnect()
        return config + int_status


date = datetime.datetime.now()
date = date.strftime("%Y%m%d")
os.mkdir(date)

# CSV file format
# hostname,device_type,host IP,username,password,secret,sh_conf,sh_ip_int_br
device_file = open('devices.csv', 'r')
device_list = device_file.readlines()

for device in device_list:
    name, dev_type, hostname, username, password, secret, sh_conf, sh_int = device.split(',')
    dev = Device(dev_type, hostname, username, password, secret, sh_conf, sh_int)
    with open(date + '/' + name + '-' + date + '.txt', 'w') as file:
        file.write(dev.backup_config())
