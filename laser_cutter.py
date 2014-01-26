#!/usr/bin/python2
import re
import sys
import math
import serial
import time
import os


stepper_table=[9,10,6,5]
ser = serial.Serial('/dev/ttyACM3', 9600, timeout=1) 

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

#def line(x0, y0, x1, y1):
#
#	dx =  abs(x1-x0), sx = x0<x1 ? 1 : -1
#	dy = -abs(y1-y0), sy = y0<y1 ? 1 : -1
#	err = dx+dy, e2
#
#	while(1): 
#        	printf(x0,y0)
#        if ((x0=x1) and (y0==y1)):
#		break
#        e2 = 2*err
#        if (e2 > dy):
#        	err += dy
#	        x0 += sx
#        
#        if (e2 < dx):
#        	err += dx
#	        y0 += sy
#        
   
f = open('foo.gcode')
firstline = f.readline()
a=firstline.split();
x1=int(20*float(a[1][1:]))
y1=int(20*float(a[2][1:]))
f.close()



f = open('foo.gcode')
content = f.readlines()


#x1=0
#y1=0
x2=0
y2=0
x=0
y=0
for line in content:
	a=line.split();
	x2=int(20*float(a[1][1:]))
	y2=int(20*float(a[2][1:]))
	#print "#####" 
        #print "x1 y1",x1,y1
        #print "x2 x2",x2,y2
        #print "#####" 
	#print Brensenham_line((int(float(x1)),int(float(x1)),int(float(x1)),int(float(x1)))
	#print Brensenham_line(x1,y1,x2,y2)
	points=Brensenham_line(x1,y1,x2,y2)
	x1=x2
	y1=y2


	for i in points:
    		print i[0],i[1]
		#ser.write(dec2hex(stepper_table[x&3] | stepper_table[y&3]<<4)+" 38 = ")
		#print dec2hex(stepper_table[x&3] | stepper_table[x&3]<<4)+" 38 = "
		#while ( (x != i[0]) and (y != i[1]) ):
		#	if x<i[0]:
		#		x=x+1
		#	if y<i[1]:
		#		y=y+1
		#	if x>i[0]:
		#		x=x-1
		#	if y>i[1]:
		#		y=y-1
		#	#ser.write(dec2hex(stepper_table[x&3] | stepper_table[y&3]<<4)+" 38 = ")
		ser.write(dec2hex(stepper_table[i[0]&3] | stepper_table[i[1]&3]<<4)+" 38 = ")
		time.sleep(.03)
                #        print x,y


ser.write("00 38 = ") 
f.close()
ser.close()
ser.open()

ser.write("ff 37 = ") 
#ser.write(dec2hex(stepper_table[x&3] | stepper_table[x&3]<<4)+" 38 = ") 
#print dec2hex(stepper_table[x&3] | stepper_table[x&3]<<4)+" 38 = " 
time.sleep(.01)
ser.write("00 38 = ") 




