#!/usr/bin/env python3

import time
import Adafruit_GPIO.SPI as SPI
import datetime
import Adafruit_MCP3008
import math
import time
import subprocess
import os
import re
import configparser
from decimal import *

######################################
#CONFIG LOADER
######################################

config = configparser.ConfigParser()

with open("/home/pi/batterymon/batterymon.ini", 'r') as file:
    config_data = file.read()

config.read_string(config_data)



mcp = Adafruit_MCP3008.MCP3008(clk=int(config['SPI']['CLK']), cs=int(config['SPI']['CS']), miso=int(config['SPI']['MISO']), mosi=int(config['SPI']['MOSI']))

class pngviewer(object):

    visible = False

    def __init__(self):
        self.visible = False
              
    def set(self, icon, icon_size = 32, x = 0, y = 0 ):   
        self.__icon = "/home/pi/batterymon/icons/" + str(icon) + ".png"
        self.__icon_size = icon_size
        self.__y = str(y)
        self.__x = str(x) 
        self.__pngview_path = "/usr/local/bin/pngview"
        self.__pngview_call = [self.__pngview_path, "-d", "0", "-b", "0x0000", "-n", "-l", "15000", "-y", self.__y, "-x", self.__x]       
        self.__fbfile="tvservice -s"
        self.__resolution=re.search("(\d{3,}x\d{3,})", subprocess.check_output(self.__fbfile.split()).decode().rstrip()).group().split('x')  
        self.__overlay_process = None
        self.show()
    
    def show(self):        
        self.hide();
        time.sleep(0.1)
        self.__overlay_process_cmd = self.__pngview_call + [self.__icon]
        self.__overlay_process = subprocess.Popen(self.__overlay_process_cmd) 
        start = time.time()

    def hide(self):
        os.system('killall pngview')


def get_adc():
    return mcp.read_adc_difference(0)

def get_voltage():
    return adc_to_voltage(get_adc())

def adc_to_voltage(adc):
    d = Decimal(config['GENERAL']['ADC_TO_VOLTAGE_DIVIDE'])
    return round((adc / d) / 100,2)

def get_average_voltage(checks = 2, sleep = 1):

    voltages = []

    for x in range(checks):
        voltages.append(get_voltage())  
        time.sleep(sleep)
   
    return round(sum(voltages) / len(voltages) ,1)
    
    
def get_battery_percentage():    

    #Average Voltage
    a = Decimal(get_average_voltage())
    
    #Critcal Voltage minus Average Voltage
    b = Decimal(Decimal(a) - Decimal(config['GENERAL']['VOLTAGE_CRITICAL']))
    
    #Difference Between Full and Empty / 100
    c = Decimal((Decimal(config['GENERAL']['VOLTAGE_FULL']) - Decimal(config['GENERAL']['VOLTAGE_CRITICAL'])) / 100)
  
    # B / C
    d = Decimal(b / c)
  
    return round(d,0)
   
def roundup(x, n=10):
    res = math.ceil(x/n)*n
    if (x%n < n/2)and (x%n>0):
        res-=n
    return res
   
def log(logln):
    logFile = "/home/pi/batterymon/batterymon.log"
    f = open(logFile, "a") 
    count = len(open(logFile).readlines(  ))
    
    # Keeps Log at 300 Lines
    if(count > 300):
        with open(logFile, 'r') as fin:
            data = fin.read().splitlines(True)
        with open(logFile, 'w') as fout:
            fout.writelines(data[1:])
    
    print(str(logln))
    f.write(str(datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")) + ":" + str(logln) + "\r\n")
    f.close()    
   
### Generic Vars defined
icon = pngviewer()
icon.set("0", 32, 10, 0)

def main():

    try:
        log("BatteryMon Started...")
        log("Full Battery At " + config['GENERAL']['VOLTAGE_FULL'])
        log("Critical Battery At " + config['GENERAL']['VOLTAGE_CRITICAL'])
        percentage = 0
        while True:
            now_percentage = get_battery_percentage()
            if(now_percentage != percentage):
                percentage = now_percentage
                log("Battery Is at " + str(percentage) + "%")
                log("Voltage Is at " + str(get_voltage()) + "v")                
                if(get_voltage() > float(config['GENERAL']['VOLTAGE_FULL']) or percentage > 100):
                    icon.set("charging", 32, 10, 0)
                    log("Battery charging") 
                    
                elif(get_voltage() <= float(config['GENERAL']['VOLTAGE_CRITICAL'])):
                    icon.set("critical", 32, 10, 0)
                    log("Battery Critical, shutdown in 10 seconds...") 
                    time.sleep(10)
                    os.system('shutdown -tf 0')
                else:
                    icon.set(roundup(percentage), 32, 10, 0)


    finally:
        log("BatteryMon Stopping...")
        os.system('killall pngview')

if __name__=='__main__':
    main()    
