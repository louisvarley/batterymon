
# BatteryMon
BatteryMon is a Raspberry PI battery monitor, great if you are using a MCP3008 or similar Analogue to Digital converter to read battery voltage. 

Other packages exist which does battery along with other things but this is pure, simple, and just monitors battery. 

## Installation
SSH onto your PI
From your Home Directory 
Run
`Git Clone https://github.com/louisvarley/batterymon.git`

run
`cd batterymon`
`sudo bash ./install.sh`

script will install any required dependencys and install BatteryMon as a service

### Warning
BatteryMon is designed to run in your home directory within the directory `batterymon`
if you move this, services will not run and must be amended
Service is installed to `/lib/systemd/system/`

## Start Service

`Sudo service batterymon start`

## Config

There is a battermon.ini file which is used to configured various settings
 
 #### SPI
 SPI Settings are where you set the CLK, MISO, MOSI, and CS pins you have your MCP3008 connected to
#### General
##### ADC_TO_VOLTAGE_DIVIDE 
BatteryMon monitors the ADC number coming from the SPI. The number is used in the following equation 
**(ADC / ( ADC_TO_VOLTAGE_DIVIDE) ) / 2**

In other words, the ADC Divided by your ADC_TO_VOLTAGE_DIVIDE number, should be twice your voltage. 
This setting should be fine for most batterys but you can check and amend using a multi meter.

##### VOLTAGE_FULL
What voltage is considered to be a FULL battery. Above this is considered charging. 

##### VOLTAGE_CRITICAL
What voltage is considered to be critical. Below this, the PI will auto shutdown. Both these numbers are used to work out what your percentage is. 

## Icons

The percentage of the battery is rounded up or down to the nearest 10 and used to display an icon from the icon folder. For example
at 71% 70.png will be shown
at 86% 90.png will be shown 
at 33% 30.png will be shown


## Things to do... one day

I wish there was a battery way to monitor for charging. At the moment its checking for either a percentage over 100% or voltage above full. 
This seems to not always work. Sometimes the voltage during charging (atleast for me) starts below the batterys full voltage and ramps up.. so this only shows as charging when its almost full. Ideally. I'd put the the charging LED ground into the PI to signal charging

Also the timing isnt great, any change can take a couple of a seconds, depending on the number of checks and sleeps done. It's currently at a good mix, Maybe this could be in the config.ini to make it easier to change. 

## Credits 
Thanks to AndrewFromMelbourne for raspidmx and pngview, without which this wouldnt be possible. 

This was a quick project created in a couple of hours to run a Retropie handheld so have fun. 
