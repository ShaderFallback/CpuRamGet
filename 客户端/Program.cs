using System;
using System.Management;
using System.Diagnostics;
using System.Threading;
using System.Net.Sockets;
using System.Text;
using System.Net;
using OpenHardwareMonitor.Hardware;
using System.Collections.Generic;

namespace ConsoleApp1
{
    public class Class1
    {
        static double getAllRam = 0;
        static double useVoltage = 0;
        static int updateTime = 0;
        static int sendValueID_1 = 0;
        static int sendValueID_2 = 0;

        static string esp32Ip;
        static int esp32Port = 4999;
        static UdpClient udpClient = new UdpClient();
        static Computer computer;

        static double cpuLoad = 0;
        static double cpuTemperature = 0;
        static double ramLoad = 0;
        static double gpuLoad = 0;
        static double gpuRamLoad = 0;
        static double gpuTemperature = 0;
        static void Main(string[] args)
        {
           
            if (args.Length != 6)
            {
                Console.WriteLine("输入的配置项不正确!\n");
                Console.WriteLine("右键CpuRamGet.exe -> 创建快捷方式 -> 快捷方式右键属性 -> 目标 -> CpuRamGet.exe 尾部依照下列说明添加\n");
                Console.WriteLine("1.IP  2.端口号  3.电压表最大值(3.3V以内)  4.刷新时间(单位毫秒)  5.发送数据ID 1  6.发送数据ID 2\n");
                Console.WriteLine("可选的ID(6选2):  1 CPU使用率, 2 CPU温度, 3 内存使用率, 4 GPU使用率, 5 GPU显存占用, 6 GPU温度\n");
                Console.WriteLine("每项中间空格区分\n \n例: 192.168.1.199 2333 1 500 1 2");
                Console.ReadKey();
                return;
            }

            esp32Ip = args[0];
            esp32Port = Convert.ToInt32(args[1]);
            useVoltage = (255.0f / 3.30f) * Convert.ToDouble(args[2]);
            updateTime = Convert.ToInt32(args[3]);
            sendValueID_1 = Convert.ToInt32(args[4]);
            sendValueID_2 = Convert.ToInt32(args[5]);

            Init();
            Thread thread = new Thread(SetEsp32);
            thread.Start();
        }

        static double RamapValue(double Value, double Low1Val, double High1Val, double Low2Val, double High2Val)
        {
            double re = (Value - Low1Val) * (High2Val - Low2Val) / (High1Val - Low1Val) + Low2Val;
            return re;
        }
        static void SetEsp32()
        {
            while (true)
            {
                Console.Clear();

                foreach (var hardware in computer.Hardware)
                {
                    hardware.Update();

                    if (hardware.HardwareType == HardwareType.CPU)
                    {
                        foreach (var sensor in hardware.Sensors)
                        {
                            if (sensor.SensorType == SensorType.Load)
                            {
                                if (sensor != null)
                                {
                                    if (sensor.Index == 0) //总占用率
                                    {
                                        cpuLoad = (double)sensor.Value;
                                    }
                                }
                            }
                            if (sensor.SensorType == SensorType.Temperature)
                            {
                                if (sensor != null)
                                {
                                    if (sensor.Index == 0)
                                    {
                                        cpuTemperature = (double)sensor.Value;
                                    }
                                }
                            }
                        }
                    }
                    else if (hardware.HardwareType == HardwareType.RAM)
                    {
                        foreach (var sensor in hardware.Sensors)
                        {
                            if (sensor.SensorType == SensorType.Load)
                            {
                                if (sensor != null)
                                {
                                    ramLoad = (double)sensor.Value;
                                }
                            }
                        }
                    } //没有此显卡为空
                    else if (hardware.HardwareType == HardwareType.GpuAti)
                    {
                        foreach (var sensor in hardware.Sensors)
                        {
                            if (sensor.SensorType == SensorType.Load)
                            {
                                if (sensor != null)
                                {
                                    if (sensor != null)
                                    {
                                        if (sensor.Index == 0) //总占用率
                                        {
                                            gpuLoad = (double)sensor.Value;
                                        }
                                        else if (sensor.Index == 4) //显存占用
                                        {
                                            gpuRamLoad = (double)sensor.Value;
                                        }
                                    }
                                }
                            }
                            if (sensor.SensorType == SensorType.Temperature)
                            {
                                if (sensor != null)
                                {
                                    if (sensor.Index == 0) //Gpu温度
                                    {
                                        gpuTemperature = (double)sensor.Value;
                                    }
                                }
                            }
                        }
                    }
                    else if (hardware.HardwareType == HardwareType.GpuNvidia)
                    {
                        foreach (var sensor in hardware.Sensors)
                        {
                            if (sensor.SensorType == SensorType.Load)
                            {
                                if (sensor != null)
                                {
                                    if (sensor.Index == 0) //总占用率
                                    {
                                        gpuLoad = (double)sensor.Value;
                                    }
                                    else if (sensor.Index == 4) //显存占用
                                    {
                                        gpuRamLoad = (double)sensor.Value;
                                    }
                                }
                            }
                            if (sensor.SensorType == SensorType.Temperature)
                            {
                                if (sensor != null)
                                {
                                    if (sensor.Index == 0) //总占用率
                                    {
                                        gpuTemperature = (double)sensor.Value;
                                    }
                                }
                            }
                        }
                    }
                    
                }

                cpuLoad = Math.Round(cpuLoad,0);
                cpuTemperature = Math.Round(cpuTemperature, 0);
                ramLoad = Math.Round(ramLoad, 0);
                gpuLoad = Math.Round(gpuLoad, 0);
                gpuRamLoad = Math.Round(gpuRamLoad, 0);
                gpuTemperature = Math.Round(gpuTemperature, 0);

                Console.WriteLine("===================bilibili日出东水===================\n");
                Console.WriteLine("ID_1  CPU 使用率: " + cpuLoad + " %\n");
                Console.WriteLine("ID_2  CPU 温度: " + cpuTemperature + " C\n");

                //Console.WriteLine("总内存: " + getAllRam + " MB");
                Console.WriteLine("ID_3  内存使用率: " + ramLoad + " %\n");

                Console.WriteLine("ID_4  GPU 使用率: " + gpuLoad + " %\n");
                Console.WriteLine("ID_5  GPU 显存占用: " + gpuRamLoad + " %\n");
                Console.WriteLine("ID_6  GPU 温度: " + gpuTemperature + " C\n");

                //dac的数值范围为0-255,实际输出电压值为0-3.3v
                string _sendType_1;
                string _sendType_2;
                double _sendValue_1 =  SwitchSendValue(sendValueID_1, out _sendType_1);
                double _sendValue_2 = SwitchSendValue(sendValueID_2, out _sendType_2);

                Console.WriteLine("配置的数据类型: [" + _sendType_1 +"] / ["+ _sendType_2+"]\n");

                string sendStr1 = Convert.ToString(Math.Round(RamapValue(_sendValue_1, 0, 100.0, 0, useVoltage), 0));
                string sendStr2 = Convert.ToString(Math.Round(RamapValue(_sendValue_2, 0, 100.0, 0, useVoltage), 0));
                Esp32Connected(sendStr2 + "," + sendStr1);
                Console.WriteLine("\n----------------OpenHardwareMonitor------------------");
                System.Threading.Thread.Sleep(updateTime);
            }
        }

        static double SwitchSendValue(int index,out string dataType)
        {
            switch (index)
            {
                case 1:
                    dataType = "CPU 使用率";
                    return cpuLoad;
                case 2:
                    dataType = "CPU 温度";
                    return cpuTemperature;
                case 3:
                    dataType = "内存使用率";
                    return ramLoad;
                case 4:
                    dataType = "GPU 使用率";
                    return gpuLoad;
                case 5:
                    dataType = "GPU 显存占用";
                    return gpuRamLoad;
                case 6:
                    dataType = "GPU 温度";
                    return gpuTemperature;
            }
            dataType = "传参错误";
            return 0;
        }

        static void Init()
        {
            //获取Cpu,Gpu使用率温度等
            computer = new Computer();
            computer.CPUEnabled = true;
            computer.RAMEnabled = true;
            computer.GPUEnabled = true;
            computer.Open();

            //获取总物理内存大小
            ManagementClass cimobject1 = new ManagementClass("Win32_PhysicalMemory");
            ManagementObjectCollection moc1 = cimobject1.GetInstances();
            double capacity = 0;
            foreach (ManagementObject mo1 in moc1)
            {
                capacity += ((Math.Round(Int64.Parse(mo1.Properties["Capacity"].Value.ToString()) / 1024 / 1024 / 1024.0, 1)));
            }
            moc1.Dispose();
            cimobject1.Dispose();
            getAllRam = capacity * 1024;
        }

        static void Esp32Connected(string message)
        {
            //UDP 方式发送信息给开发板
            byte[] buffer = Encoding.UTF8.GetBytes(message);

            if (udpClient != null)
            {
                IPAddress remoteIp = IPAddress.Parse(esp32Ip);
                IPEndPoint remotePoint = new IPEndPoint(remoteIp, esp32Port);
                udpClient.Send(buffer, buffer.Length, remotePoint);
                Console.WriteLine("IP:" + esp32Ip + " 端口:" + esp32Port + " 发送信息: " + message);
            }
        }
    }
}
