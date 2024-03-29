#     Author: Alessandro Zanni
#     <alessandro.zanni3@unibo.it>

import subprocess
import threading
import time
import Config
import Messages

def delete_exited_containers():
    cmd = "docker ps -a | grep Exit | cut -d ' ' -f 1 | xargs docker rm"
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    for line in iter(proc.stdout.readline,''):
        line = line.decode("utf-8").replace("\n","")
        print(line)
        if line is "":
            break

class myThread_Hostapd(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.lastDevice = ""
    def get_devices(self):
        cmd = "sudo hostapd_cli all_sta"
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        count = 1
        for line in iter(proc.stdout.readline,''):
            line = line.decode("utf-8").replace("\n","")
            if count == 2:
                return line
            elif count < 2:
                count+=1
            else:
                break
        return ""
    def run(self):
        while True:
            device_mac = "mac_address"
            #device_mac = ""
            #device_mac = self.get_devices()
            print("device: " + device_mac)
            if (device_mac != "") and (device_mac != self.lastDevice):
                print("Device MAC detected:" + device_mac)
                print("Send a cloud request for mobile presence")
                Messages.send("mobile_presence", mac="mac_address")
            elif (device_mac == "") and (device_mac != self.lastDevice):
                print("Lost device")
                delete_exited_containers()
                print("Unused containers deleted")
            self.lastDevice = device_mac
                
            time.sleep(Config.HOSTAPD_TIMEFRAME)