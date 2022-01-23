using System;
using System.Management;
using System.Diagnostics;
using System.Threading;
using System.Net.Sockets;
using System.Text;
using System.Net;

namespace ConsoleApp1
{
    public class Class1
    {
        static PerformanceCounter cpuCounter;
        static PerformanceCounter ramCounter;
        static double getAllRam;
        static double useVoltage;
        static int updateTime;
        static string esp32Ip;
        static int esp32Port;
        static UdpClient udpClient = new UdpClient();

        static void Main(string[] args)
        {
            if (args.Length != 4)
            {
                Console.WriteLine("输入的配置项不正确!\n");
                Console.WriteLine("右键CpuRamGet.exe -> 创建快捷方式 -> 快捷方式右键属性 -> 目标 -> CpuRamGet.exe 尾部依照下列说明添加\n");
                Console.WriteLine("1.IP  2.端口号  2.电压表最大值(3.3V以内)  3.刷新时间(单位毫秒) 每项中间空格区分\n \n例: 192.168.1.199 2333 1 500");
                Console.ReadKey();
                return;
            }
                
            esp32Ip = args[0];
            esp32Port = Convert.ToInt32(args[1]);
            useVoltage = (255.0f / 3.30f) * Convert.ToDouble(args[2]);
            updateTime = Convert.ToInt32(args[3]);

            Init(out cpuCounter, out ramCounter,out getAllRam);
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
                double cpuProcessor = Math.Round(cpuCounter.NextValue(), 0);
                double ramMemory = Math.Round((1.0 - (ramCounter.NextValue() / getAllRam)) * 100, 0);
                Console.WriteLine("CPU使用率：" + cpuProcessor + "%");
                Console.WriteLine("总内存:" + getAllRam + " MB");
                Console.WriteLine("可使用内存：" + ramCounter.NextValue() + " MB");
                Console.WriteLine("占用内存百分比：" + ramMemory + "%");

                //dac的数值范围为0-255,实际输出电压值为0-3.3v
                Esp32Connected(Math.Round( RamapValue(ramMemory, 0, 100.0, 0, useVoltage),0) + ","+ Math.Round(RamapValue(cpuProcessor, 0, 100.0, 0, useVoltage), 0));
                System.Threading.Thread.Sleep(updateTime);
            }
        }

        static void Init(out PerformanceCounter cpuCounter, out PerformanceCounter ramCounter, out double getAllRam)
        {
            //获取Cpu使用率
            cpuCounter = new PerformanceCounter();
            cpuCounter.CategoryName = "Processor";
            cpuCounter.CounterName = "% Processor Time";
            cpuCounter.InstanceName = "_Total";
            cpuCounter = new PerformanceCounter("Processor", "% Processor Time", "_Total");
            ramCounter = new PerformanceCounter("Memory", "Available MBytes");

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
                Console.WriteLine("IP:"+esp32Ip + " 端口:"+esp32Port + " 发送信息: " + message);
            }
        }
    }
}