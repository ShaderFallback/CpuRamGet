import serial
import serial.tools.list_ports
import logging
import time
from PyQt5.QtCore import QThread, pyqtSignal

logging.basicConfig(format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s', level=logging.INFO)


class Thread_GET_TARGET_PORT_AUTO(QThread):

    '''
    ※ 线程通信变量                          例
    list:   搜寻可用串口返回的结果  [串口号(已连接),串口号]
            如果没有可用串口        [无可用串口,None]
    '''
    my_signal = pyqtSignal(list)

    # 与下位机握手的校验字符串
    handshakeStr = 'handshake'

    # 连接的串口
    target_port = None

    def __init__(self):
        super(Thread_GET_TARGET_PORT_AUTO, self).__init__()
        # 自动扫描flag,默认手动扫描
        self.is_auth = False

    # 串口握手工具方法
    # 一个串口头两次通信response空，不知道为什么。
    # 所以发送三次，每次间隔1s
    def handshake(self, arduino):
        i = 0
        while i < 3:
            arduino.write(bytes(self.handshakeStr, 'utf-8'))
            response = arduino.readline().decode()
            time.sleep(1)
            i = i + 1
        return response

    def getTargetPort(self):
        # 获取所有串口
        portList = list(serial.tools.list_ports.comports())
        if len(portList) > 0:
            # 遍历所有串口
            for port in portList:
                logging.debug(port)
                try:
                    # 波特率默认使用115200，超时0.5秒
                    arduino = serial.Serial(port.name, baudrate=115200, timeout=1)
                    response = self.handshake(arduino)
                    logging.info(response)
                    # 串口握手校验
                    if response.strip() == self.handshakeStr:
                        self.my_signal.emit([port.name + "(已连接)", port.name])
                        self.target_port = port.name
                        arduino.close()
                        time.sleep(0.5)
                        logging.debug(port.name + " is usable")
                        break
                    else:
                        logging.debug(port.name + " can not use")
                except Exception:
                    # 搜寻串口时发生异常，可能是因为该串口已被占用
                    logging.debug(port.name + " can not use")
        else:
            # 没有任何串口
            logging.info("no any port")
            self.target_port = None
            self.my_signal.emit(["串口: 无", None])

    # 线程执行函数
    def run(self):
        if self.is_auth is True:
            # 自动扫描10s一次
            while True:
                if self.target_port is None:
                    logging.info("auto searching ...")
                    self.getTargetPort()
                self.sleep(10)
        else:
            # 手动扫描只执行一次
            if self.target_port is None:
                logging.info("manual searching ...")
                self.getTargetPort()
