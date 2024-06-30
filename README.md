## PC Status Physical Monitoring Table

- **1. All materials are not for commercial use; please credit the source when sharing [Hyperlink]**
- **2. The copyright of the dial images belongs to the original author**
- **3. Adjust the size of the 3D print model according to the slicer software's units (the units used during creation are centimeters). It is recommended to use KT board to make the shell, as it is more cost-effective**
    (Note: If using this 3D model to print the shell, you need to purchase a development board without soldered headers to fit it in)
- **4. Use 300 DPI when creating the dial, and make sure to set 300 DPI when printing. Arrange the layout according to the printer's print size**
- **5. The voltmeter model in the video is 91C4. The maximum voltage range should be less than 3.3V**
- **6. The esp32 firmware uses MicroPython; please download the latest version from the official website**
- **7. Before downloading the program, remember to modify the WiFi name and password in main.py. If the port does not conflict, keep the default 4999. No changes are needed for the serial version**
- **8. Thonny IDE is recommended for flashing the firmware or downloading the program**
- **9. You can use Windows <Task Scheduler> to run the program automatically on startup**
- **10. Create a basic task -> Set the trigger to "At startup" -> Start a program -> Browse to CpuRamGet.exe, and add parameters**
    (By default, the "console program" started by Task Scheduler will run in the background. Remember to uncheck "Stop the task if it runs longer than 3 days" in the settings and check "Run with highest privileges")
- **Configurable parameter IDs (select 2 out of 6): 1 CPU Usage, 2 CPU Temperature, 3 Memory Usage, 4 GPU Usage, 5 GPU Memory Usage, 6 GPU Temperature**
- **11. Download the CP210x Windows Drivers for the Esp32 USB development board serial driver** [CP210x Windows Drivers](https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers)

- **. New USB serial communication support, no WiFi configuration needed**
  Go to My Computer -> Device Manager -> Ports to see your development board's port number. Use a baud rate of 115200
  USB serial example: com4 115200 1 500 1 2

- **. If you have any questions, feel free to leave a comment under the video**
  [https://www.youtube.com/watch?v=8Lh_D1dhlAI](https://www.youtube.com/watch?v=8Lh_D1dhlAI)

### Have fun, everyone!

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

- **.搜集的其他网友的实现**
https://github.com/gitsang/loadoutput
[https://space.bilibili.com/3490242](https://space.bilibili.com/3490242)
[https://github.com/hanchengxu](https://github.com/hanchengxu)

### 祝大家玩的开心~

![image](https://github.com/ShaderFallback/CpuRamGet/blob/main/Image/成品展示1.jpg)
![image](https://github.com/ShaderFallback/CpuRamGet/blob/main/Image/成品展示2.jpg)
![image](https://github.com/ShaderFallback/CpuRamGet/blob/main/Image/接线图.png)
![image](https://github.com/ShaderFallback/CpuRamGet/blob/main/Image/硬件清单.jpg)
![image](https://github.com/ShaderFallback/CpuRamGet/blob/main/Image/组装细节.jpg)
