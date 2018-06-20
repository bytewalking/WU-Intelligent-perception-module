import time
import RPi.GPIO as GPIO
def checkdist():
        #发出触发信号
        GPIO.output(0,GPIO.HIGH)
        #保持15us的超声波发射，避免能量太低无法返回
        time.sleep(0.000015)
        #然后置位2号管脚低电平，即停止发射超声波
        GPIO.output(0,GPIO.LOW)
        while not GPIO.input(1):
                     pass
        #发现高电平时开时计时
        t1 = time.time()
        #如果有检测到反射返回的超声波，那么就持续计时，否则就跳出循环，计时结束
        while GPIO.input(1):
                     pass
        #高电平结束停止计时
        t2 = time.time()
        #返回距离，单位为米
        return (t2-t1)*340/2
GPIO.setmode(GPIO.BCM)
#第3号针，GPIO2
GPIO.setup(0,GPIO.OUT,initial=GPIO.LOW)
#第5号针，GPIO3 27.
GPIO.setup(1,GPIO.IN)
time.sleep(0)
try:
        while True:
                result=checkdist()
                print ("%.2f" % result)
                time.sleep(0.5)
except KeyboardInterrupt:
                GPIO.cleanup()
PIN_NO = 7  # GPIO编号，可自定义

GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIN_NO, GPIO.OUT)


# 哔1次，时长作为参数传递
def beep(seconds):
    GPIO.output(PIN_NO, GPIO.HIGH)
    time.sleep(seconds)
    GPIO.output(PIN_NO, GPIO.LOW)

# 哔N次，时长、间隔时长、重复次数作为参数传递
def beepAction(secs, sleepsecs, times):
    for i in range(times):
        beep(secs)
        time.sleep(sleepsecs)

 # beepAction(0.02,0.02,30)
import libbeep

while True:
    if result<=1
    libbeep.beepAction(0.05, 0.05, 2)
    time.sleep(1)
