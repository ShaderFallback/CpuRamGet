from machine import I2C, Pin
import time
from machine import Pin,DAC
import utime, math
import _thread
import socket
import sys

def getTime():
    t = time.gmtime()
    timeY = str(t[0]) #年
    timeM = str(t[1]) #月
    timeD = str(t[2]) #日
    timeHour = str(t[3]) #时
    timeMinute = str(t[4]) #分
    timeSecond = str(t[5]) #秒
    return str(timeY+"/"+timeM+"/"+timeD +" "+timeHour+":"+timeMinute+":"+timeSecond)

def do_connect():
    global addressIp
    try:
        import network
        wlan = network.WLAN(network.STA_IF)
        wlan.active(False) #先将Wifi断开,方便模拟断网调试
        wlan.active(True)
        if not wlan.isconnected():
            print('connecting to network...')
            wlan.connect('Wifi账号', '密码')
            while not wlan.isconnected():#没有返回True将循环等待
                pass
        print('network config:', wlan.ifconfig())
        addressIp = str(wlan.ifconfig())
    except:
        pass
    
def lerp(v1,v2,d):
    return v1 * (1 - d) + v2 * d

def dacThread( threadName, delay):
    global ram_value
    ramlerp = 0
    i = 0.0
    while(True):
        i += 0.01
        ramlerp = lerp(ramlerp,ram_value,i)
        dac25.write(int(ramlerp))
        if(ramlerp >= ram_value):
            i = 0.0
        time.sleep(0.015)
        
        
def dacThread2( threadName, delay):
    global cpu_value
    global ram_value
    cpulerp = 0
    i = 0.0
    countZero = 0
    cpu_valueOld = 0
    ram_valueOld = 0
    while(True):
        i += 0.01
        cpulerp = lerp(cpulerp,cpu_value,i)
        dac26.write(int(cpulerp))
        if(cpulerp >= cpu_value):
            i = 0.0
        time.sleep(0.015)
        
        #如果在1.5秒内数值都相同那么归零表值
        countZero += 1
        if(countZero == 100):
            if(cpu_value == cpu_valueOld and ram_value == ram_valueOld):
                ram_value = 0
                cpu_value = 0
            cpu_valueOld = cpu_value
            ram_valueOld = ram_value
            countZero = 0
        
        
        
def dacThread3( threadName, delay):
    global ram_value
    global cpu_value
    while(True):
        try:
            #print(getTime() + " 开始监听...")
            data,addr=s.recvfrom(32)
            stringKey = data.decode("utf-8")
            array_value =  stringKey.split(",")
            cpu_value = int(array_value[1])
            ram_value = int(array_value[0])
            #print(getTime()+" 接收信息..."+ stringKey)
            time.sleep(0.1)
        except:
            #print(getTime()+" 连接断开...")
            time.sleep(0.1)
        
        
cpu_value = 0
ram_value = 0

#初始化DAC
dac_pin25 = Pin(25, Pin.OUT)
dac_pin26 = Pin(26, Pin.OUT)

dac25 = DAC(dac_pin25)
dac26 = DAC(dac_pin26)
dac25.write(0)
dac26.write(0)

#连接Wifi
do_connect()

#创建socks,监听4999
port = 4999
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

addressIp = addressIp.replace("(","")
addressIp = addressIp.replace(")","")
addressIp = addressIp.replace("'","")
addressIp = addressIp.split(",")
s.bind((addressIp[0], port))

_thread.start_new_thread( dacThread, ("Thread_1", 1, ) )
_thread.start_new_thread( dacThread2, ("Thread_2", 2, ) )
_thread.start_new_thread( dacThread3, ("Thread_3", 3, ) )