import RPi.GPIO as GPIO
import time

Trig_Pin = 20
Echo_Pin = 21

GPIO.setmode(GPIO.BCM)
GPIO.setup(Trig_Pin, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(Echo_Pin, GPIO.IN)
time.sleep(2)
class UltrasonicData:#超声波数据
    def __init__(self,time1,data1):#定义类，self是类的实例，time1是间隔，data1是数据存放地
        self.time1=time1
        self.data1=data1
    def action(self, time1):#运行 ,time1是间隔
        self.time1=time1
        GPIO.output(Trig_Pin, GPIO.HIGH)#超声波模块使用代码开始
        time.sleep(time1)
        GPIO.output(Trig_Pin, GPIO.LOW)
        while not GPIO.input(Echo_Pin):
            pass
        t1 = time.time()
        while GPIO.input(Echo_Pin):
            pass
        t2 = time.time()#超声波模块使用代码结束
        self.data1= "Distance:%0.2f cm" % (t2 - t1) * 340 * 100 / 2
    def use(self):
        return self.data1
try:
    while True:
        obj1=UltrasonicData(time1, a)
        obj.use()
        time.sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()