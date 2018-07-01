#encoding:utf-8
import matplotlib.pyplot as plt
import threading
import smbus
import time
import math
import numpy as np
import RPi.GPIO as GPIO
from sensor import ly
from numpy import *
from beacontools import BeaconScanner
from multiprocessing import Process
from sensor import Ultrasonic_bee
from sensor import mpu6050


def main_Buletooth ():
    test = ly.Bluetooth()
    global data
    data = {}
    xd = []
    yd = []
    RSSIa = []
    RSSIb = []
    RSSIc = []
    plt.figure()

    while( 1 ):
        scanner = BeaconScanner(ly.scan_base)
        scanner.start()
        #将rssi值与mac地址分开
        flag = 1
        while( flag ):
            time.sleep(0.5)
            #print (data)
            """传入参数     待改正"""
            for add in data.keys():
                if add == u'10:01:12:ee:57:54':
                    RSSIa.append(data[add])
                    print("RSSIa=",len(RSSIa))
                    #print("RSSIa=",RSSIa)
                elif add == u'20:01:14:9c:57:54':
                    RSSIb.append(data[add])
                    print("RSSIb=",len(RSSIb))
                    #print("RSSIb=",RSSIb)
                else:
                    RSSIc.append(data[add])
                    print("RSSIc=",len(RSSIc))
                    #print("RSSIc=",RSSIc)
            if len(RSSIa) >= 20 and len(RSSIb) >= 20 and len(RSSIc) >= 20:
                flag = 0
                scanner.stop()
        ra = test.Gaussion_filter(RSSIa)
        rb = test.Gaussion_filter(RSSIb)
        rc = test.Gaussion_filter(RSSIc)
        #print(ra)
        #print(rb)
        #print(rc)
        r3 = test.RSSI_distance(ra)
        r1 = test.RSSI_distance(rb)
        r2 = test.RSSI_distance(rc)
        #print (r1)
        #print (r2)
        #print (r3)
        coordinate_D = test.fixed_point(r1,r2,r3)
        test.coordinate_system_data(coordinate_D)
        del RSSIa[:]
        del RSSIb[:]
        del RSSIc[:]
        data.clear()


def main_mpu6050():
    #calibration
    calGyroX = -0.3828125
    calGyroY = 0.05263671875
    calGyroZ = 7.254296875

    calAccX = 0
    calAccY = -1
    calAccZ = 0

    # Power management registers
    power_mgmt_1 = 0x6b
    power_mgmt_2 = 0x6c
    bus = smbus.SMBus(1) # or bus = smbus.SMBus(1) for Revision 2 boards
    address = 0x68       # This is the address value read via the i2cdetect command

    # Now wake the 6050 up as it starts in sleep mode
    bus.write_byte_data(address, power_mgmt_1, 0)

    FS_SEL=2
    AFS_SEL=1
    '''
    FS_SEL=0 => +/-250degree/s
    FS_SEL=1 => +/-500degree/s
    FS_SEL=2 => +/-1000degree/s
    FS_SEL=3 => +/-2000degree/s
    AFS_SEL=0 => +/-2g
    AFS_SEL=1 => +/-4g
    AFS_SEL=2 => +/-8g
    AFS_SEL=3 => +/-16g
    '''
    GYRO_CONFIG = bus.read_byte_data(address, 0x1B)
    bus.write_byte_data(address, 0x1B, GYRO_CONFIG | (FS_SEL<<3))
    ACCEL_CONFIG = bus.read_byte_data(address, 0x1C)
    bus.write_byte_data(address, 0x1C, ACCEL_CONFIG | (AFS_SEL<<3))
    i=0
    while (1):
        mpu6050.gyroPrint()
        print ("----------------")
        time.sleep(0.25)
        mpu6050.accelerometerPrint()
        i+=1


def main_Ultrasonic_bee():
    GPIO.setmode(GPIO.BCM)
    # 第3号针，GPIO2
    GPIO.setup(27, GPIO.OUT, initial=GPIO.LOW)
    # 第5号针，GPIO3
    GPIO.setup(22, GPIO.IN)

    time.sleep(2)
    try:
        while True:
            result = Ultrasonic_bee.checkdist()
            print('Distance: %0.2f m' % result)
            time.sleep(0.5)

            if (0 < result and result < 1) or result > 2:
                Ultrasonic_bee.beepAction(0.05, 0.05, 2)
                time.sleep(1)

    except KeyboardInterrupt:
        GPIO.cleanup()


threads = []
t2 = threading.Thread(target=main_mpu6050,args=())
threads.append(t2)
t3 = threading.Thread(target=main_Ultrasonic_bee,args=())
threads.append(t3)

main_Buletooth()
while ( 1 ):
    for t in threads:
        t.start()
