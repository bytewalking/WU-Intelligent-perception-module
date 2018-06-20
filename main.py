from sensor import Bluetooth
from sensor import Ultrasonic_1
import mpu6050_demo
test = Bluetooth()
data = {}
xd = []
yd = []
RSSIa = []
RSSIb = []
RSSIc = []
while( 1 ):
    scanner = BeaconScanner(scan_base)
    scanner.start()
    #将rssi值与mac地址分开
    flag = 1
    while( flag ):
        """传入参数     待改正"""
        for add in data.keys():
            if add == u'10:01:12:ee:57:54':
                RSSIa.append(data[add])
            elif add == u'20:01:14:9c:57:54':
                RSSIb.append(data[add])
            else:
                RSSIc.append(data[add])
                #print(len(RSSIc))
                #print(RSSIc)
        if len(RSSIa) == 20:
            flag = 0
            scanner.stop()
    ra = test.Gaussion_filter(RSSIa)
    rb = test.Gaussion_filter(RSSIb)
    rc = test.Gaussion_filter(RSSIc)
    # print(ra)
    # print(rb)
    # print(rc)
    r3 = test.RSSI_distance(ra)
    r1 = test.RSSI_distance(rb)
    r2 = test.RSSI_distance(rc)
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
