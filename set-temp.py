#!/usr/bin/python
from datetime import datetime
import time
import numpy as np
import sys
import os
import Adafruit_DHT  #This is the module for using the temp/hum sensor
import csv
import pandas as pd
import matplotlib
#import heater_on    # Not sure if this is the right way to import other python files
#import heater_off
import matplotlib.pylab as pylab
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
plt.switch_backend('agg')   #This is something copied from stackoverflow on the advice$
path = '/home/pi/labtemplogger/' #Set your path
wwwpath = '/home/pi/labtemplogger/www/'

####################################
#### Extract Data write to file ####
####################################

# NOTE for use with the DHT11 temp/humidity sensor
# References http://www.circuitbasics.com/how-to-set-up-the-dht11-humidity-sensor-on-the-raspberry-pi/

now = datetime.now() #Get the date+time right now
# dd/mm/YY H:M:S  #The format for the date and time Date/month/Year Hour:Minute:Second
date = now.strftime("%Y/%d/%m") #The function for writing the date and time
exact_time = now.strftime("%H:%M:%S")


# Get data from the senor
humiditytemperature = Adafruit_DHT.read_retry(11,4) # Function for pulling the temp/humid data from DHT11
temperature = humiditytemperature[1]
humidity = humiditytemperature[0]
# Print the Date, Time, Temperature and Humidity
print "Date: ",date, "Time: ",exact_time , "Temperature: ",temperature,'C', "Humidity: ",humidity,'%'

# User entry for temperature setting in degree C
set_temp = float(raw_input("Enter the Set Temerature for the Incubator: "))
if set_temp > 80:
    print "You have set a target temperature above the threshold. Please enter a number below 80C"
    set_temp = raw_input("Enter a value below 80: ")
    if set_temp > 80:
	set_temp = float(37)
	print "You are taking the piss. Default temp 37 degrees has now been set."
	print "Set Temperature:",set_temp
    elif 40 <= set_temp <= 80:
	print "You entered:",set_temp,"this will kill most bacteria, are you sure? Please reenter to confirm."
        set_temp = raw_input("Reenter your Temperature to confirm: ")
	print "Set Temperature:",set_temp
elif 40 <= set_temp <= 80:
    print "You entered:",set_temp,"this will kill most bacteria, are you sure? Please reenter to confirm."
    set_temp = raw_input("Reenter your Temperature to confirm: ")
    print "Set Temperature:",set_temp
else:
    print "User Set Temperature:",set_temp
###############################
## Save Data and Plot Figure ##
###############################
def savetempdataplotasgraph(date,exact_time,temperature,humidity):
    # Write to a file
    temphistory = open(wwwpath+'temphum-record.csv', 'a') # 'a' means append to file
    w=csv.writer(temphistory)
    fields=[date,exact_time,temperature,humidity]
    w.writerow(fields)

    # Starting to use pandas to read the data
    df = pd.read_csv(wwwpath+'temphum-record.csv')
    df.Time=pd.to_datetime(df.Time)
    df.set_index('Time')
    x = df['Time']
    y1 = df['Temperature']
    y2 = df['Humidity']
    #print(x,y1,y2)
    #######################
    ##### PLOT THE DATA #####
    #######################
    # Plot parameters
    pylab.rcParams['figure.figsize'] = 10, 8  # that's default image size for this interactive session
    plt.plot(x, y1, x, y2)
    plt.legend(['Temperature', 'Humidity'],fontsize = 'x-small', loc=2)
    plt.grid(True) #puts dotted lines across chart (handy for analysis)
    #plt.xlim(950,2000) #Preference Add limits on X-Y axis scale
    #plt.ylim(0,4)
    plt.axhline(y=set_temp, color='r', linestyle='--')
    plt.tight_layout(pad=2.5, w_pad=2.5, h_pad=2.5)
    # beautify the x-labels
    plt.gcf().autofmt_xdate()
    #Name and Axes labels
    plt.xlabel('Date/Time', fontsize=13)
    plt.ylabel('Temperature', fontsize=13)
    plt.savefig(wwwpath+'temphum_graph.png')

##################################################
##### LOOP for finding optimal temperature ######
################################################
i = 0
while True: #temperature != set_temp and i <= 20:
# Get data from the senor
    humiditytemperature = Adafruit_DHT.read_retry(11,4) # Function for pulling the temp/humid data from DHT11
    temperature = humiditytemperature[1]
    humidity = humiditytemperature[0]
    date = now.strftime("%Y/%d/%m") #The function for writing the date and time
    exact_time = now.strftime("%H:%M:%S")
    time.sleep(float(1)) # Wait for x seconds.
    # Take an image and place in the www directory
    if i==5:
        print "recording date, time and updating graph"
        savetempdataplotasgraph(date,exact_time,temperature,humidity)
	i = 0
    if temperature < set_temp:
        print "Time: ", exact_time, "Current Temperature: ", temperature, "Target Temperature: ", set_temp
        print "Too Cold!"
    elif temperature > set_temp:
        print "Time: ", exact_time, "Current Temperature: ", temperature, "Target Temperature: ", set_temp
        print "Too Hot"
    else:
        print "At Set Temperature"
        print "Time: ", exact_time, "Current Temperature: ", temperature, "Target Temperature: ", set_temp
    #time.sleep(float(30)) # Wait for x seconds.
    i += 1
print "Exiting Temperature Loop"
#####
#END#
#####
