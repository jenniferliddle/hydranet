#
# sensehat.py
# Program to run on the raspberry pi using the sensehat board
#
# Author: Jennifer Liddle <jennifer@jsquared.co.uk>
# Copyright: J-Squared Ltd 2017
#
# Released under the
# GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007
#
from sense_hat import SenseHat
import time
import os

ALPHA = 0.5
PERIOD = 60 * 30

BLACK = [0,0,0]
RED = [255,64,64]
GREEN = [64,255,64]
BLUE = [64,64,255]

global checkpoint
checkpoint = time.time()

sense = SenseHat()
graph = {}
graph['temperature'] = {}
graph['temperature']['data'] = [0,0,0,0,0,0,0,0]
graph['temperature']['offset'] = 15
graph['temperature']['scale'] = 2

graph['humidity'] = {}
graph['humidity']['data'] = [0,0,0,0,0,0,0,0]
graph['humidity']['offset'] = 20
graph['humidity']['scale'] = 8

graph['pressure'] = {}
graph['pressure']['data'] = [0,0,0,0,0,0,0,0]
graph['pressure']['offset'] = 900
graph['pressure']['scale'] = 50

def bump_graph():
    global checkpoint
    for sensor in (graph):
        d = graph[sensor]['data']
        d.pop(0)
        d.append(0)
    checkpoint = time.time()

def save_value(sensor, v):
    x = sensor['data'].pop()
    if (x):
        x = ALPHA * v + (1 - ALPHA) * x
    else:
        x = v
    sensor['data'].append(x)
    #print v, sensor['data']

def get_cpu_temp():
    res = os.popen("vcgencmd measure_temp").readline()
    t = float(res.replace("temp=","").replace("'C\n",""))
    return(t)

def get_temperature():
    t = sense.get_temperature_from_humidity()
    t_cpu = get_cpu_temp()
    t = t - ((t_cpu-t)/1.5)
    save_value(graph['temperature'], t)
    return t

def get_pressure():
    p = sense.pressure
    save_value(graph['pressure'], p)
    return p

def get_humidity():
    h = sense.humidity
    save_value(graph['humidity'], h)
    return h

def xy2p(x,y):
    if (x<0): x=0
    if (x>7): x=y
    if (y<0): y=0
    if (y>7): y=7
    return (7-y)*8+x

def draw_line(grid, x, v, colour, offset, scale):
    v = int((v-offset)/scale+0.5)
    for y in (range(v)):
        p = xy2p(x,y)
        grid[p] = colour

def dump_grid(grid):
    n = 0
    while (n<64):
        print grid[n],grid[n+1],grid[n+2],grid[n+3],grid[n+4],grid[n+5],grid[n+6],grid[n+7]
        n = n+8

def display_barchart(sensor, colour):
    data = sensor['data']
    grid = [BLACK] * 64
    for x in range(0,len(data)):    
        v = data[x]
        draw_line(grid,x,v,colour,sensor['offset'],sensor['scale'])
    #dump_grid(grid)
    sense.set_pixels(grid)
    time.sleep(1)

def display_things(t, p, h):
    global graph
    sense.show_message(str(int(t+0.5))+" C",.1,RED)
    display_barchart(graph['temperature'],RED)
    sense.show_message(str(int(h+0.5))+" %",.1,BLUE)
    display_barchart(graph['humidity'],BLUE)
    sense.show_message(str(int(p+0.5))+" ",.1,GREEN)
    display_barchart(graph['pressure'],GREEN)

while True:
    temperature = get_temperature()
    pressure = get_pressure()
    humidity = get_humidity()
    display_things(temperature, pressure, humidity)
    if (time.time() - checkpoint) > PERIOD:
        bump_graph()

