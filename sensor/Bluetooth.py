"""蓝牙模块"""
import matplotlib.pyplot as plt
import time
import math
from beacontools import BeaconScanner
class Bluetooth:
    def __init__(self):
        """初始化蓝牙模块"""
        A = int(input("请输发射端和接收端相隔一米时的信号强度，建议程序内部设置"))
        N = int(input("环境衰减因子,建议程序内部设置值"))
        xc = int(input("请输入xc的值"))
        yc = int(input("请输入yc的值"))
        ya = int(input("请输入ya的值"))

    def fixed_point(self,xc,ya,yc,r1,r2,r3):
        """定位计算模块,r1为BD距离，r2为DC距离，r3为AD距离"""
        yd = (r1**2-r3**2+ya**2)/2*ya
        xd = (r1**2-r2**2+xc**2+yc**2-2*yd*yc)/2*xc
        return xd,yd
    def RSSI_distance(self,rssi,A,N):
        """蓝牙RSSI计算距离"""
        d = 10**((abs(rssi)-A)/10*N)
        """ A为发射端和接收端相隔一米时的信号强度
            N为环境衰减因子"""
        return d
    def CSYS (self,xd,yd,xc,ya,yc):
        """直角坐标系建系及绘图，xd,yd 可以直接传数组"""
        plt.plot(xc, yc, 'or-')
        plt.plot(0, 0, 'or-')
        plt.plot(0, ya, 'or-')
        plt.figure()
        plt.plot(xd, yd,'xb-')
        plt.show()
    def coordinate_system_data (self,distance):
        """探测坐标数据归类"""
        global xd
        global yd
        xd.append(distance[0])
        yd.append(distance[1])
    def bluetooch_data(self):
        """蓝牙模块初始化传入参数"""
        global data
        data = {}
        def callback(bt_addr, rssi, packet, additional_info):
            data[bt_addr] = rssi
        #   print ("<%s, %d> %s %s" % (bt_addr, rssi, packet, additional_info))
        # scan for all iBeacon advertisements from beacons with the specified uuid
        while (1):
            scanner = BeaconScanner(callback)
            scanner.start()
            #time.sleep(3)#睡眠时间自定义
            scanner.stop()
            return data
    def Gaussion_filter(self,RSSI):
        """高斯滤波算法"""
        rssi = 0
        gaussion_filter_num = []
        """均值"""
        add = sum(RSSI)
        ave = add/len(RSSI)
        """标准差"""
        for i in range(len(RSSI)-1):
            rssi = rssi+(RSSI[i]-ave)**2
        standard_deviation = math.sqrt( rssi/len(RSSI) )
        """高斯滤波"""
        for j in range(len(RSSI)-1):
            gaussion_filter_num = gaussion_filter_num.append((1/math.sqrt(2*math.pi)*standard_deviation)*math.exp(-(RSSI[j]/ave)**2/2*(standard_deviation**2)))
        return gaussion_filter_num

    def Gaussion_Smoothing_filter(self,rssi,x1):
        """基于高斯滤波的平滑滤波，看情况选用
           把高斯滤波后的数值取平滑"""
        gaussion_smoothing_filter=[]
        for i in range(len(rssi)-1):
            gaussion_smoothing_filter=gaussion_smoothing_filter.append(x1+(rssi[i]-x1)/len(rssi))
        return gaussion_smoothing_filter


    xd = []
    yd = []
    data = bluetooch_data()
    RSSIa = []
    RSSIa = RSSIa.append(data[Amac])#Amac待定
    RSSIb = []
    RSSIb = RSSIb.append(data[Bmac])#Bmac待定
    RSSIc = []
    RSSIc = RSSIc.append(data[Cmac])#Cmac待定
    distance = fixed_point(xc,ya,yc,r1,r2,r3)
    coordinate_system_data(distance)
    CSYS(xd, yd, xc, ya, yc)
