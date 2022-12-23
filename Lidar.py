import csv
import time
import math
import sys
import numpy
import Messages
from LidarDriver import Lidar
import pygame
from collections import deque
#from occupancy_grid import OccupancyGrid

porkyStartUp = 'PORKY: Booting Up!'
porkyShutDown = 'PORKY: Powering Down!'
Port = '/dev/ttyS0'
lidar = Lidar(port = Port)

def setup():
    lidar.reboot()
    
def loop():
    lidar.startScan()
    lastScan = deque([], 100)
    currentScan = []
    print(lastScan)
    #while(True):
     #   lidar.startScan()
      #  lastScan = deque([], 100)
       # currentScan = []
        #print(lastScan)
    
def destroy():
    lidar.stopScan()
    
if __name__ == '__main__':
    print(porkyStartUp)
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        print(porkyShutDown)
        destroy()

