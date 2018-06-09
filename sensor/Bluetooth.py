"""蓝牙模块"""
import matplotlib.pyplot as plt
import time
import math
import numpy as np
from beacontools import BeaconScanner
def scan_base(bt_addr, rssi, packet, additional_info):
    print ("<%s, %d> %s %s" % (bt_addr, rssi, packet, additional_info))

class Bluetooth():
    def __init__(self):
        """初始化蓝牙模块"""
        self.A = int(input("请输发射端和接收端相隔一米时的信号强度，建议程序内部设置"))
        self.N = int(input("环境衰减因子,建议程序内部设置值"))
        self.xc = int(input("请输入xc的值"))
        self.yc = int(input("请输入yc的值"))
        self.ya = int(input("请输入ya的值"))

    def fixed_point(self,xc,ya,yc,r1,r2,r3):
        """定位计算模块,r1为BD距离，r2为DC距离，r3为AD距离"""
        yd = (r1**2-r3**2+ya**2)/2*ya
        xd = (r1**2-r2**2+xc**2+yc**2-2*yd*yc)/2*xc
        return xd, yd

    def RSSI_distance(self,rssi,A,N):
        """蓝牙RSSI计算距离"""
        r = 10**((abs(rssi)-A)/10*N)
        """ A为发射端和接收端相隔一米时的信号强度
            N为环境衰减因子"""
        return r

    def CSYS (self,xd,yd,xc,ya,yc):
        """直角坐标系建系及绘图，xd,yd 可以直接传数组"""
        plt.plot(xc, yc, 'or-')
        plt.plot(0, 0, 'or-')
        plt.plot(0, ya, 'or-')
        plt.plot(xd, yd , 'xb')
        for i in range(len(xd)-2):
            plt.annotate("", xytext=(xd[i], yd[i]), textcoords='data', xy=(xd[i + 1], yd[i + 1]), xycoords='data',arrowprops=dict(arrowstyle="->", connectionstyle="arc3", ec='y'))
        plt.figure()
        plt.show()

    def coordinate_system_data (self,distance):
        """探测坐标数据归类"""
        global xd
        global yd
        xd.append(distance[0])
        yd.append(distance[1])
        self.CSYS(xd, yd, self.xc, self.ya, self.yc)

    def callback(bt_addr, rssi, packet, additional_info):
        """蓝牙模块初始化传入参数"""
        data[bt_addr] = rssi
        #print ("<%s, %d># %s %s" % (bt_addr, rssi ,packet, additional_info))
        #scan for all iBeacon advertisements from beacons with the specified uuid

    def Gaussion_filter(self,RSSI): #lists为存放多个节点rssi强度的列表
        """高斯滤波算法"""
        gaussion_filter_num = []
        """均值"""
        rssi=0
        add = sum(RSSI)
        ave = add/len(RSSI)
        """标准差"""
        for i in range(len(RSSI)-1):
            rssi = rssi+(RSSI[i]-ave)**2
        standard_deviation = math.sqrt( rssi/len(RSSI) )
        """高斯滤波"""
        for j in range(len(RSSI)-1):
            value = ((math.exp((-((RSSI[j] - ave) ** 2) / (2 * standard_deviation ** 2)))) / standard_deviation * (math.sqrt(2 * math.pi)))
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
data = {}
xd = []
yd = []
RSSIa = []
RSSIb = []
RSSIc = []
while( 1 ):
    #scanner.start()
    #将rssi值与mac地址分开
    flag = 1
    while(flag):
        scanner = test.bluetooch_data(test.callback)
        print(scanner)
        for add in data.keys():
            if add == u'10:01:12:ee:57:54':
                RSSIa.append(data[add])
            elif add == u'20:01:14:9c:57:54':
                RSSIb.append(data[add])
            else:
                RSSIc.append(data[add])
                #print(len(RSSIc))
                #print(RSSIc)
        if len(RSSIa) == 20 :
            flag = 0
                #test.scanner.stop()
    ra = test.Gaussion_filter(RSSIa)
    rb = test.Gaussion_filter(RSSIb)
    rc = test.Gaussion_filter(RSSIc)
    # print(ra)
    # print(rb)
    # print(rc)
    r3 = test.RSSI_distance(ra, 47, 1.7)
    r1 = test.RSSI_distance(rb, 47, 1.7)
    r2 = test.RSSI_distance(rc, 47, 1.7)
    # print (r1)
    # print (r2)
    # print (r3)
    coordinate_D = test.fixed_point(test.xc,test.ya,test.yc,r1,r2,r3)
    #print (coordinate_D)
    test.coordinate_system_data(coordinate_D)
    del RSSIa[:]
    del RSSIb[:]
    del RSSIc[:]
    data.clear()
