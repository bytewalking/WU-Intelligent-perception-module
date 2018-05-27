"""陀螺仪模块"""
import smbus # 此模块要在树莓派上安装测试
import math


class Gyroscope:

    def __init__(self, power_mgmt_1, power_mgmt_2):
        """初始陀螺仪模块"""
        self.power_mgmt_1 = power_mgmt_1
        self.power_mgmt_2 = power_mgmt_2
