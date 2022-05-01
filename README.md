## PC 状态物理监控表
- **1.全部资料请勿用作商业用途,转载请注明出处[超连接]**
- **2.表盘图片版权归原作者所有**
- **3.3D打印模型请根据切片软件单位放大或缩小 (制作时的单位是厘米), 推荐使用KT板制作外壳,成本更低**
    (注意如果使用这个3D模型打印外壳，开发板要购买没有焊接排针版本,才能安装进去)
- **4.表盘制作时使用300 DPI,打印时注意设置300 DPI, 根据打印机画幅排版即可**
- **5.视频中的电压表的型号是 91C4 ,电压最大量程要小于3.3V**
- **6.esp32 固件采用MicroPython,请去官网下载最新**
- **7.下载程序前请记得修改main.py 中的 Wifi 名和密码, 端口不冲突可保持默认4999串口版本无需修改** 
- **8.IDE 推荐使用 thonny 刷机 or 下载程序**
- **9.开机自动运行可以使用 Windows <任务计划程序>**
- **10.创建基本任务 -> 触发器设置为计算机启动时 -> 启动程序 -> 浏览到CpuRamGet.exe ，添加参数即可**
    (任务计划程序启动的 "控制台程序"默认会在后台运行,记得在设置里取消"运行超过3天停止任务选项",勾选使用管理员运行 )
- **可配置的参数ID(6选2):  1 CPU使用率, 2 CPU温度, 3 内存使用率, 4 GPU使用率, 5 GPU显存占用, 6 GPU温度**
- **11.Esp32 USB 开发板的串口驱动下载 CP210x Windows Drivers** [CP210x Windows Drivers](https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers)

- **.新增USB串口通信支持,无需配置Wifi**
我的电脑属性-> 设备管理器 -> 端口 -> 查看你开发板的端口号,波特率使用115200
USB串口示例: com4 115200 1 500 1 2


- **.有任何疑问欢迎在视频下留言**
[www.bilibili.com/video/BV1jL4y1x7gx](https://www.bilibili.com/video/BV1jL4y1x7gx)

- **.感谢【大肠杆君的日常】,贡献的图形化客户端**
[https://space.bilibili.com/3490242](https://space.bilibili.com/3490242)
[https://github.com/hanchengxu](https://github.com/hanchengxu)

- **.留言区搜集的其他网友的实现**
https://github.com/gitsang/loadoutput

### 祝大家玩的开心~

![image](https://github.com/ShaderFallback/CpuRamGet/blob/main/Image/成品展示1.jpg)
![image](https://github.com/ShaderFallback/CpuRamGet/blob/main/Image/成品展示2.jpg)
![image](https://github.com/ShaderFallback/CpuRamGet/blob/main/Image/接线图.png)
![image](https://github.com/ShaderFallback/CpuRamGet/blob/main/Image/硬件清单.jpg)
![image](https://github.com/ShaderFallback/CpuRamGet/blob/main/Image/组装细节.jpg)
