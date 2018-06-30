import smbus
import math
import time

#calibration
calGyroX = -0.3828125
calGyroY = 0.05263671875
calGyroZ = 7.254296875

calAccX = 0
calAccY = -1
calAccZ = 0

# Power management registers
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c

def read_byte(adr):
    return bus.read_byte_data(address, adr)

def read_word(adr):
    high = bus.read_byte_data(address, adr)
    low = bus.read_byte_data(address, adr+1)
    val = (high << 8) + low
    return val

def read_word_2c(adr):
    val = read_word(adr)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val

def dist(a,b):
    return math.sqrt((a*a)+(b*b))

def get_y_rotation(x,y,z):
    radians = math.atan2(x, dist(y,z))
    return -math.degrees(radians)

def get_x_rotation(x,y,z):
    radians = math.atan2(y, dist(x,z))
    return math.degrees(radians)

#输出函数
#陀螺仪
def gyroPrint():
    #绕X轴旋转的角速度GYR_X
    gyro_xout = read_word_2c(0x43)
    #绕Y轴旋转的角速度GYR_Y
    gyro_yout = read_word_2c(0x45)
    #绕Z轴旋转的角速度GYR_Z 
    gyro_zout = read_word_2c(0x47)


    move = 1000*gyro_xout/32768
    if(move>-5 and move<5):
        print 'stop'
    elif(move>5):
        print'front'
    else:
        print'back'
       
        
   # print "y轴角速度：",1000*gyro_yout/32768-calAccY
   # print "z轴角速度：",1000*gyro_zout/32768
'''
    print "gyro data"
    print "---------"
    print "gyro_xout: ", gyro_xout, " scaled: ", (gyro_xout / 131)
    print "gyro_yout: ", gyro_yout, " scaled: ", (gyro_yout / 131)
    print "gyro_zout: ", gyro_zout, " scaled: ", (gyro_zout / 131)
    print "---------"
'''

#加速度计
def accelerometerPrint():
    #加速度计的X轴分量ACC_X
    accel_xout = read_word_2c(0x3b)
    #加速度计的Y轴分量ACC_Y
    accel_yout = read_word_2c(0x3d)
    #加速度计的Z轴分量ACC_Z
    accel_zout = read_word_2c(0x3f)
    #当前温度TEMP
    accel_temperature = read_word_2c(0x41)

    accel_xout_scaled = accel_xout / 16384.0
    accel_yout_scaled = accel_yout / 16384.0
    accel_zout_scaled = accel_zout / 16384.0
'''
    print "----------------加速度计--------------------"
    print "温度：",accel_temperature
    print "x轴加速度：",4*9.8*accel_xout/32768-calGyroX
    print "y轴加速度：",4*9.8*accel_yout/32768-calGyroY
    print "z轴加速度：",4*9.8*accel_zout/32768-calGyroZ

    print "accel_xout: ", accel_xout, " scaled: ", accel_xout_scaled
    print "accel_yout: ", accel_yout, " scaled: ", accel_yout_scaled
    print "accel_zout: ", accel_zout, " scaled: ", accel_zout_scaled
    
    #旋转
    print "x rotation: " , get_x_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)
    print "y rotation: " , get_y_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)

'''
bus = smbus.SMBus(1) # or bus = smbus.SMBus(1) for Revision 2 boards
address = 0x68       # This is the address value read via the i2cdetect command

# Now wake the 6050 up as it starts in sleep mode
bus.write_byte_data(address, power_mgmt_1, 0)

FS_SEL=2
AFS_SEL=1
'''
FS_SEL=0 => +/-250degree/s
FS_SEL=1 => +/-500degree/s
FS_SEL=2 => +/-1000degree/s
FS_SEL=3 => +/-2000degree/s

AFS_SEL=0 => +/-2g
AFS_SEL=1 => +/-4g
AFS_SEL=2 => +/-8g
AFS_SEL=3 => +/-16g
'''
GYRO_CONFIG = bus.read_byte_data(address, 0x1B)
bus.write_byte_data(address, 0x1B, GYRO_CONFIG | (FS_SEL<<3))

ACCEL_CONFIG = bus.read_byte_data(address, 0x1C)
bus.write_byte_data(address, 0x1C, ACCEL_CONFIG | (AFS_SEL<<3))

i=0
while (1):
    gyroPrint()
    print "----------------"
    time.sleep(0.25)
    accelerometerPrint()
    i+=1
