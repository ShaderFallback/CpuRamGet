import serial
import serial.tools.list_ports
import logging
import time
import psutil
from PyQt5.QtCore import QThread, pyqtSignal

logging.basicConfig(format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s', level=logging.INFO)


class Thread_PORT_TRANS(QThread):

    '''
    ※ boolean型线程通信变量
    目标串口不可用时，设为False
    '''
    my_signal = pyqtSignal(bool)

    # 目标串口号，外部获得
    targetPort = None

    def __init__(self):
        super(Thread_PORT_TRANS, self).__init__()

    def run(self):
        while True:
            try:
                # 握手成功后 进行通信
                arduino = serial.Serial(self.targetPort, baudrate=115200, timeout=1)
                message = "0,0"
                while True:
                    self.my_signal.emit(True)
                    message = str(round(psutil.cpu_percent(0))) + "," + (str)(round(psutil.virtual_memory().percent))
                    logging.debug("send:" + message)
                    arduino.write(bytes(message, 'utf-8'))
                    time.sleep(1)
                    data = arduino.readline()
                    logging.debug("response:" + data.decode())
            except Exception:
                # 有异常后停止通信并再次 获取目标串口
                logging.info("lose port")
                # 线程通信信号量设为 False
                self.my_signal.emit(False)
                self.targetPort = None
