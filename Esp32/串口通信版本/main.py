from machine import I2C, Pin
import time
from machine import Pin,DAC
import utime, math
import select
import _thread
import socket
import sys


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
        if(abs(cpulerp - cpu_value) <3):
            i = 0.0
        time.sleep(0.015)
        
        #如果在1.5秒内数值都相同那么归零表值
        countZero += 1
        if(countZero == 500):
            if(cpu_value == cpu_valueOld and ram_value == ram_valueOld):
                ram_value = 0
                cpu_value = 0
            cpu_valueOld = cpu_value
            ram_valueOld = ram_value
            countZero = 0
              

cpu_value = 0
ram_value = 0

#初始化DAC
dac_pin25 = Pin(25, Pin.OUT)
dac_pin26 = Pin(26, Pin.OUT)

dac25 = DAC(dac_pin25)
dac26 = DAC(dac_pin26)
dac25.write(0)
dac26.write(0)

p22 = Pin(2, Pin.OUT)

p = select.poll() 
p.register(
    sys.stdin,        # 检测标准输入 (REPL)
    select.POLLIN     # 检查是否有数据待读取
) 

_thread.start_new_thread( dacThread, ("Thread_1", 1, ) )
_thread.start_new_thread( dacThread2, ("Thread_2", 2, ) )

while(True):
    try:
        readInfo = sys.stdin.read(8)
        print(str(readInfo))
        array_value =  readInfo.split(".")[0].split(",")
        cpu_value = int(array_value[1])
        ram_value = int(array_value[0])
        time.sleep(0.1)
    except:
        #print(getTime()+" 连接断开...")
        time.sleep(0.1)
