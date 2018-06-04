"""蓝牙模块"""
import matplotlib.pyplot as plt
import time
from beacontools import BeaconScanner

class Bluetooth:

    def __init__(self):
        """初始化蓝牙模块"""
        pass
    def fixed_point(self,xc,ya,yc,r1,r2,r3):
        """定位计算模块，均为0,r1为BD距离，r2为DC距离，r3为AD距离"""
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
        """直角坐标系建系及绘图"""
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
            time.sleep(3)#睡眠时间自定义
            scanner.stop()
            return data


    A = int(input("请输发射端和接收端相隔一米时的信号强度，建议程序内部设置"))
    N = int(input("环境衰减因子,建议程序内部设置值"))
    xc = int(input("请输入xc的值"))
    yc = int(input("请输入yc的值"))
    ya = int(input("请输入ya的值"))
    xd = []
    yd = []
    data = bluetooch_data()
    RSSIa = data[Amac]#Amac待定
    RSSIb = data[Bmac]#Bmac待定
    RSSIc = data[Cmac]#Cmac待定
    distance = fixed_point(xc,ya,yc,r1,r2,r3)
    coordinate_system_data(distance)
    CSYS(xd, yd, xc, ya, yc)
