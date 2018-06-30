#! /usr/bin/python
# -*- coding:utf-8 -*-

import RPi.GPIO as GPIO
import time

def checkdist():

    #发出触发信号
    GPIO.output(27,GPIO.HIGH)
    #保持10us以上（我选择15us）
    time.sleep(0.000015)
    GPIO.output(27,GPIO.LOW)
    while not GPIO.input(22):
        pass
    #发现高电平时开时计时
    t1 = time.time()
    while GPIO.input(22):
        pass
    #高电平结束停止计时
    t2 = time.time()
    #返回距离，单位为米
    return (t2-t1)*340/2

# 哔N次，时长、间隔时长、重复次数作为参数传递
def beepAction(secs, sleepsecs, times):
    PIN_NO = 4  # GPIO编号，可自定义

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIN_NO, GPIO.OUT)

    for i in range(times):
        GPIO.output(PIN_NO, GPIO.HIGH)
        time.sleep(secs)
        GPIO.output(PIN_NO, GPIO.LOW)
        time.sleep(sleepsecs)

        

GPIO.setmode(GPIO.BCM)
#第3号针，GPIO2
GPIO.setup(27,GPIO.OUT,initial=GPIO.LOW)
#第5号针，GPIO3
GPIO.setup(22,GPIO.IN)

time.sleep(2)
try:
    while True:
        result=checkdist()
        print ('Distance: %0.2f m' %result)
        time.sleep(0.5)
        
        if (0 < result and result < 1 ) or result > 2:
            beepAction(0.05, 0.05, 2)
            time.sleep(1)

except KeyboardInterrupt:
    GPIO.cleanup()
    
# PIN_NO = 7  # GPIO编号，可自定义

# GPIO.setmode(GPIO.BOARD)
# GPIO.setup(PIN_NO, GPIO.OUT)
#
#
# # 哔1次，时长作为参数传递
# def beep(seconds):
#     GPIO.output(PIN_NO, GPIO.HIGH)
#     time.sleep(seconds)
#     GPIO.output(PIN_NO, GPIO.LOW)
#


# beepAction(0.02,0.02,30)
