"""超声波模块"""
import RPi.GPIO as GPIO # 此模块要在树莓派上安装测试
import time

class Gyroscope:

    def __init__(self, Trig_Pin, Echo_Pin):
        """初始超声波模块"""
        self.Trig_Pin = Trig_Pin  # Trig引脚
        self.Echo_Pin = Echo_Pin  # Echo引脚

    def ranging(self):
        """测量距离方法"""
        GPIO.output(self.Trig_Pin, GPIO.HIGH)
        time.sleep(0.00015)
        GPIO.output(self.Trig_Pin, GPIO.LOW)
        while not GPIO.input(self.Echo_Pin):
            pass
        t1 = time.time()
        while GPIO.input(self.Echo_Pin):
            pass
        t2 = time.time()
        return (t2 - t1) * 340 * 100 / 2