#!/usr/bin/env python3

import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import math
import time
import subprocess
import os
import re
import configparser

######################################
#CONFIG LOADER
######################################

config = configparser.ConfigParser()
config['SPI'] = {'CLK': 11,'MISO': 9,'MOSI': 10, 'CS': 8}
config['GENERAL'] = {'ADC_TO_VOLTAGE_DIVIDE': 1.961,'VOLTAGE_FULL': 4.07,'VOLTAGE_CRITICAL': 2.70}

with open('batterymon.ini', 'w') as configfile:
    config.write(configfile)
    
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
        if(self.visible == True):
            self.hide();
            time.sleep(0.1)
        self.__overlay_process_cmd = self.__pngview_call + [self.__icon]
        self.__overlay_process = subprocess.Popen(self.__overlay_process_cmd) 
        start = time.time()
        self.visible = True


    def hide(self):
        if(self.__overlay_process != None):
            self.__overlay_process.kill()  
            self.visible = False

def get_adc():
    return mcp.read_adc_difference(0)

def get_voltage():
    return adc_to_voltage(get_adc())

def adc_to_voltage(adc):
    return round((adc / float(config['GENERAL']['ADC_TO_VOLTAGE_DIVIDE'])) / 100,2)

def get_average_voltage(checks = 5, sleep = 2):

    voltages = []

    for x in range(checks):
        voltages.append(get_voltage())  
        time.sleep(sleep)
   
    return round(sum(voltages) / len(voltages) ,1)
    
    
def get_battery_percentage():    
   return round(get_average_voltage() / (float(config['GENERAL']['VOLTAGE_FULL']) / 100),0)
   
def roundup(x, n=10):
    res = math.ceil(x/n)*n
    if (x%n < n/2)and (x%n>0):
        res-=n
    return res
   
   
### Generic Vars defined
icon = pngviewer()
icon.set("0", 32, 10, 0)

def main():

    try:
        percentage = 0
        while True:
           now_percentage = roundup(get_battery_percentage())
           if(now_percentage != percentage):
               percentage = now_percentage
               icon.set(percentage, 32, 10, 0)
               print("Battery Is Now at " + str(percentage))
               
    finally:
        os.system('taskkill /f /im pngview')

if __name__=='__main__':
    main()    