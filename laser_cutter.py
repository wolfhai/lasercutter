#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re
import sys
import math
import serial
import time
import os
from datetime import datetime
from datetime import timedelta
scale = 120
duty_cycle = 0  # milliseconds
duty_pause = 0.8  # seconds
speed_move = 0.007
speed_cut = 0.007
curve_section = 20

global start_time
global gcode_coordinates
global ser
global x2
global y2
global x1
global y1

try:
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
except:
    print('Serial connection failed')
    quit()

def millis():
    dt = datetime.now() - start_time
    ms = (dt.days * 24 * 60 * 60 + dt.seconds) * 1000 + dt.microseconds \
        / 1000.0
    return ms

def laser(x):
    if x == 0:
        print('Laser off')
        ser.write(b'00 31 = ')
        ser.write(b'00 32 = ')
    if x == 1:
        print('Laser on')
        global start_time
        start_time = datetime.now()
        ser.write(b'01 31 = ')
        ser.write(b'01 32 = ')

def dec2hex(n):
    return '%02X' % n

def Brensenham_line(x,y,x2,y2):
    x=round(scale * float(x))
    y=round(scale * float(y))
    x2=round(scale * float(x2))
    y2=round(scale * float(y2))
    
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

def serial_write():
    stepper_table = [9, 10, 6, 5]
    try:
        ser.write(bytes(dec2hex(stepper_table[gcode_coordinates[1] & 3]|stepper_table[gcode_coordinates[0] & 3] << 4)+' 38 = ', encoding='ascii'))
    except:
        print('failed at...')
        print(x1,y1,x2,y2,gcode_coordinates[1],gcode_coordinates[0])        
        quit()

ser.write(b'FF 37 = ')
try:
    f = open(sys.argv[1])
except:
    print('no file found')
    quit()
laser(0)
x1=0
y1=0
content = f.readlines()
for line in content:
    if line[:1] == 'G':
        a = line.split()
        if a[0] == 'G00':
            if (a[1])[:1] == 'Z':
                if float((a[1])[1:]) > 0:
                    laser(0)
            if (a[1])[:1] == 'X':
                print(a[1], a[2])
                x2 = a[1][1:]
                y2 = a[2][1:]
                points = Brensenham_line(x1, y1, x2, y2)
                x1 = x2
                y1 = y2
                for gcode_coordinates in points:
                    serial_write()
                    time.sleep(speed_move)
        if a[0] == 'G01':
            if a[1][:1] == 'Z':
                if float(a[1][1:]) < 0:
                    laser(1)
                if float(a[1][1:]) > 0:
                    laser(0)
            if a[1][:1] == 'X':
                print(a[1], a[2])
                x2 = a[1][1:]
                y2 = a[2][1:]
                points = Brensenham_line(x1, y1, x2, y2)
                x1 = x2
                y1 = y2
                for gcode_coordinates in points:
                    serial_write()
                    time.sleep(speed_cut)
                    if ((duty_cycle != 0) and (millis() > duty_cycle)):
                        laser(0)
                        time.sleep(duty_pause)
                        laser(1)
        if a[0] == 'G02' or 'G03':
            if (line.find('X') != -1 and line.find('Y') != -1 and line.find('I') != -1 and line.find('J') != -1):
                x = float((a[1][1:]))
                y = float((a[2][1:]))
                I = float((a[4][1:]))
                J = float((a[5][1:]))
                print(a[1], a[2], a[4], a[5])
                center_x =  I+float(x1)
                center_y =  J+float(y1)
                ax = (float(x1) - center_x)
                ay = (float(y1) - center_y)
                bx = (float(x) - center_x)
                by = (float(y) - center_y)
                if a[0] == 'G02':    
                    angle_a = math.atan2(by, bx)
                    angle_b = math.atan2(ay, ax)
                if a[0] == 'G03':                    
                    angle_a = math.atan2(ay, ax)
                    angle_b = math.atan2(by, bx)
                if (angle_b <= angle_a): 
                    angle_b = angle_b +2 * math.pi
                angle = angle_b - angle_a
                radius = math.sqrt((ax * ax) + (ay * ay))
                length = radius * angle
                steps = int (math.ceil(length*curve_section))
                for s in range(1 ,steps):
                    if a[0] == 'G02': 
                        one_step =  steps - s
                    if a[0] == 'G03': 
                        one_step =  s
                    arc_x = center_x + radius * math.cos(angle_a + angle * (float (one_step) / steps) )
                    arc_y = center_y + radius * math.sin(angle_a + angle * (float (one_step) / steps) )
                    points = Brensenham_line(x1, y1, arc_x,arc_y )
                    x1=arc_x
                    y1=arc_y
                    for gcode_coordinates in points:
                        serial_write()
                        time.sleep(speed_cut)
                        if ((duty_cycle != 0) and (millis() > duty_cycle)):
                            laser(0)
                            time.sleep(duty_pause)
                            laser(1)
ser.write(b'00 38 = ')
f.close()
ser.close()
print('Done')
