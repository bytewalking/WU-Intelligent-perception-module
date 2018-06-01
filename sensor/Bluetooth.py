"""蓝牙模块"""


class Bluetooth:

    def __init__(self):
        """初始化蓝牙模块"""
        pass

    def fixed_point(self,xc,ya,yc,r1,r2,r3):
        """定位计算模块    xa  xb  yb  均为0"""
        yd=(r1**2-r3**2+ya**2)/2*ya
        xd=(r1**2-r2**2+xc**2+yc**2-2*yd*yc)/2*xc
        return xd,yd

    def RSSI_distance(self,rssi,A,N):
        """蓝牙RSSI计算距离"""
        d=10**((abs(rssi)-A)/10*N)
        """ A为发射端和接收端相隔一米时的信号强度
            N为环境衰减因子"""
        return d