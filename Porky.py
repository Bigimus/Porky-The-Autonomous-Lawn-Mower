import RPi.GPIO as GPIO
from rplidar import RPLidar
import time
import sys
import pygame
lidarCtrl = 11
lidar = RPLidar("/dev/ttyS0")

def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(lidarCtrl, GPIO.OUT)import RPi.GPIO as GPIO
from rplidar import RPLidar
import time
import sys
import pygame
lidarCtrl = 11
lidar = RPLidar("/dev/ttyS0")

def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(lidarCtrl, GPIO.OUT)
    lidar.connect()

def destroy():
    GPIO.cleanup()
    lidar.stop()
    lidar.stop_motor()
    lidar.disconnect()
        
def loop():
    #info =lidar.get_info()
    #print('\n'.join('%s: %s' % (k, str(v)) for k, v in info.items()))
    while(True):
        GPIO.output(lidarCtrl, GPIO.HIGH)
        #lidar.start_motor()
        #lidar.get_health()
        #process_scan = lambda scan: None
        #for scan in lidar.iter_scans():
            #process_scan(scan)
        
if __name__ == '__main__':
    print('Porky is booting up!')
    setup()
    print('Porky is online!')
    try:
        loop()
    except KeyboardInterrupt:
        destroy()
        print('Porky is offline!')
        


    lidar.connect()

def destroy():
    GPIO.cleanup()
    lidar.stop()
    lidar.stop_motor()
    lidar.disconnect()
        
def loop():
    #info =lidar.get_info()
    #print('\n'.join('%s: %s' % (k, str(v)) for k, v in info.items()))
    while(True):
        GPIO.output(lidarCtrl, GPIO.HIGH)
        #lidar.start_motor()
        #lidar.get_health()
        #process_scan = lambda scan: None
        #for scan in lidar.iter_scans():
            #process_scan(scan)
        
if __name__ == '__main__':
    print('Porky is booting up!')
    setup()
    print('Porky is online!')
    try:
        loop()
    except KeyboardInterrupt:
        destroy()
        print('Porky is offline!')
        
