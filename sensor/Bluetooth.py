"""蓝牙模块"""
import matplotlib.pyplot as plt
import time
import math
import _thread
import numpy as np
from beacontools import BeaconScanner
from multiprocessing import Process
def scan_base(bt_addr, rssi, packet, additional_info):
    data[bt_addr]=rssi

class Bluetooth():
    def __init__(self):
        """初始化蓝牙模块"""
        self.A = 55
        self.N = 5
        self.xc = 4.4
        self.yc = 7.2
        self.ya = 7.2
        self.rssi = 0 

    def fixed_point(self,xc,ya,yc,r1,r2,r3):
        """定位计算模块,r1为BD距离，r2为DC距离，r3为AD距离"""
        time.sleep(0.1)
        yd = ((r1**2)-(r3**2)+(ya**2))/(2*ya)
        yd = int(yd*100)
        yd = yd/100.0
        xd = (( r1**2)-(r2**2)+(xc**2)+(yc**2)-(2*yd*yc))/(2*xc)
        return xd, yd

    def RSSI_distance(self,rssi):
        """蓝牙RSSI计算距离"""
        endRSSI=abs(rssi)-self.A
        endN=10*self.N
        r = 10**(endRSSI/endN)
        """ A为发射端和接收端相隔一米时的信号强度
            N为环境衰减因子"""
        return r

    def CSYS (self,xd,yd,xc,ya,yc):
        """直角坐标系建系及绘图，xd,yd 可以直接传数组"""
        plt.close()
        plt.plot(xc, yc, 'or-')
        plt.plot(0, 0, 'or-')
        plt.plot(0, ya, 'or-')
        plt.plot(xd, yd , 'xb')
        #plt.ion()
        i = 1 
        for i in range(len(xd)-1):
            plt.annotate("", xytext=(xd[i], yd[i]), textcoords='data', xy=(xd[i-1], yd[i-1]), xycoords='data',arrowprops=dict(arrowstyle="->", connectionstyle="arc3", ec='y'))
        time.sleep(0.1)
        plt.show()
        #plt.show(block = False)
        

    def coordinate_system_data (self,distance):
        """探测坐标数据归类"""
        global xd
        global yd
        xd.append(distance[0])
        yd.append(distance[1])
        _thread.start_new_thread(self.CSYS,(xd, yd, self.xc, self.ya, self.yc))

    #def callback(bt_addr, rssi, packet, additional_info):
        """蓝牙模块初始化传入参数"""
     #   data[bt_addr] = rssi
       
    def Gaussion_filter(self,RSSI): #lists为存放多个节点rssi强度的列表
        """高斯滤波算法"""
        gaussion_filter_num = []
        rssinum = 0
        for i in RSSI:
            rssinum=rssinum+1
            
        """均值"""
        add = sum(RSSI)
        ave = add/rssinum
        """标准差"""
        for i in range(rssinum-1):
            self.rssi = self.rssi+(RSSI[i]-ave)**2
        print (self.rssi)
        standard_deviation = math.sqrt( self.rssi/rssinum )
        print (standard_deviation)
        """高斯滤波"""
        for j in range(rssinum-1):
            pi=math.sqrt(2 * math.pi)
            standard_deviation2=standard_deviation ** 2
            print (standard_deviation2)
            value = (math.exp((-((RSSI[j] - ave) ** 2) / (2 * standard_deviation2)))) / standard_deviation * pi            
            upper_limit = ave+value*standard_deviation
            lower_limit = ave-value*standard_deviation
            if upper_limit > RSSI[j] and lower_limit<RSSI[j]:
                gaussion_filter_num.append(RSSI[j])
            elif upper_limit < RSSI[j]:
                gaussion_filter_num.append(upper_limit)
            else:
                gaussion_filter_num.append(lower_limit)
        gaussion_ave = sum(gaussion_filter_num)/len(gaussion_filter_num)
        return gaussion_ave


test = Bluetooth()
global data
data = {}
xd = []
yd = []
RSSIa = []
RSSIb = []
RSSIc = []
plt.figure()

while( 1 ):
    scanner = BeaconScanner(scan_base)
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
    coordinate_D = test.fixed_point(test.xc,test.ya,test.yc,r1,r2,r3)
    print (coordinate_D)
    test.coordinate_system_data(coordinate_D)    
    del RSSIa[:]
    del RSSIb[:]
    del RSSIc[:]
    data.clear()