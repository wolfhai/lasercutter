#!/usr/bin/python2
import re
import sys
import math
import serial
import time
import os
from datetime import datetime
from datetime import timedelta

scale=120
duty_cycle=3000  #milliseconds
duty_pause=0.8   #seconds
speed_move=0.008
speed_cut=0.03

def millis():
   dt = datetime.now() - start_time
   ms = (dt.days * 24 * 60 * 60 + dt.seconds) * 1000 + dt.microseconds / 1000.0
   return ms

def laser(x):
    if (x==0):
	print "Laser off"
	ser.write("00 31 = ")
	ser.write("00 32 = ")
    if (x==1):
	print "Laser on"
	global start_time
	start_time = datetime.now()
	ser.write("01 31 = ")
	ser.write("01 32 = ")

def dec2hex(n):
    return "%02X" % n

def Brensenham_line(x,y,x2,y2):
    steep = 0
    coords = [] 
    dx = abs(x2 - x)
    if (x2 - x) > 0: sx = 1
    else: sx = -1
    dy = abs(y2 - y)
    if (y2 - y) > 0: sy = 1
    else: sy = -1
    if dy > dx:
        steep = 1
        x,y = y,x
        dx,dy = dy,dx
        sx,sy = sy,sx
    d = (2 * dy) - dx
    for i in range(0,dx):
        if steep: coords.append((y,x))
        else: coords.append((x,y))
        while d >= 0:
            y = y + sy
            d = d - (2 * dx)
        x = x + sx
        d = d + (2 * dy)
    coords.append((x2,y2))
    return coords 

global start_time

x2=0;y2=0;x1=0;y1=0

stepper_table=[9,10,6,5]
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1) 
ser.write("FF 37 = ") 
f = open(sys.argv[1])
content = f.readlines()
laser(0)

for line in content:
        if (line[:1]=="G"):
		a=line.split()

       		if (a[0]=="G00"):
			if (a[1][:1]=="Z"):
                        	if (float(a[1][1:])>0):
					laser(0)
			if (a[1][:1]=="X"):
				print a[1],a[2]
				x2=int(scale*float(a[1][1:]))
				y2=int(scale*float(a[2][1:]))
				points=Brensenham_line(x1,y1,x2,y2)
				x1=x2
				y1=y2
				for i in points:
					ser.write(dec2hex(stepper_table[i[1]&3] | stepper_table[i[0]&3]<<4)+" 38 = ")
					time.sleep(speed_move)
		if (a[0]=="G01"):
			if (a[1][:1]=="Z"):
                        	if (float(a[1][1:])<0):
					laser(1)
                        	if (float(a[1][1:])>0):
					laser(0)
			if (a[1][:1]=="X"):
				print a[1],a[2]
				x2=int(scale*float(a[1][1:]))
				y2=int(scale*float(a[2][1:]))
				points=Brensenham_line(x1,y1,x2,y2)
				x1=x2
				y1=y2
				for i in points:
					ser.write(dec2hex(stepper_table[i[1]&3] | stepper_table[i[0]&3]<<4)+" 38 = ")
					time.sleep(speed_cut)
					if (millis()>duty_cycle):
						laser(0)
						time.sleep(duty_pause)
						laser(1)
ser.write("00 38 = ") 
f.close()
ser.close()
print "Done"
