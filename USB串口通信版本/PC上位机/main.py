import logging
import sys
import resource
import time
import psutil
import serial
import serial.tools.list_ports
from PyQt5.QtCore import QCoreApplication, QSharedMemory, QThread, pyqtSignal
from PyQt5.QtGui import QIcon
# 从PyQt库导入QtWidget通用窗口类,基本的窗口集在PyQt5.QtWidgets模块里.
from PyQt5.QtWidgets import (QAction, QApplication, QMenu, QMessageBox, QSystemTrayIcon, QWidget)

logging.basicConfig(format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s', level=logging.INFO)


class Example(QWidget):
    # 串口对象
    targetPort = None

    def __init__(self):
        super(Example, self).__init__()

        self.trayIconMenu = QMenu()
        self.statusAction = QAction("&串口: 未設定")
        self.statusAction.setIcon(QIcon(':/imgs/brightness.png'))
        self.trayIconMenu.addAction(self.statusAction)

        self.searchPortMenu = QMenu('&扫描串口')

        self.searchAuto = QAction('&自动扫描')
        self.searchAuto.setIcon(QIcon(':/imgs/checked.png'))
        self.searchAuto.setIconVisibleInMenu(False)
        self.searchAuto.triggered.connect(self.auto_search)
        self.searchPortMenu.addAction(self.searchAuto)

        self.searchManualAction = QAction('&手动扫描')
        self.searchManualAction.setIcon(QIcon(':/imgs/checked.png'))
        self.searchManualAction.setIconVisibleInMenu(False)
        self.searchManualAction.triggered.connect(self.start_search)
        self.searchPortMenu.addAction(self.searchManualAction)

        self.trayIconMenu.addMenu(self.searchPortMenu)

        # 直接退出可以用 quit_app
        self.closeAction = QAction('&退出')
        self.closeAction.triggered.connect(self.quit_app)
        self.trayIconMenu.addAction(self.closeAction)

        # 在系统托盘处显示图标
        self.trayIcon = QSystemTrayIcon(self)
        self.trayIcon.setIcon(QIcon(':/imgs/icon.png'))
        self.trayIcon.setContextMenu(self.trayIconMenu)
        self.trayIcon.show()

        # 实例化线程对象(串口扫描)
        self.auto_get_targetPort_thread = Thread_GET_TARGET_PORT_AUTO()
        self.auto_get_targetPort_thread.my_signal.connect(self.update_port)

        # 实例化线程对象(串口通信)
        self.port_trans_thread = Thread_PORT_TRANS()
        self.port_trans_thread.my_signal.connect(self.lose_port)

    def start_search(self):
        logging.debug('start_search ...')
        self.searchManualAction.setIconVisibleInMenu(True)
        self.searchAuto.setIconVisibleInMenu(False)
        self.auto_get_targetPort_thread.is_auth = False
        if self.auto_get_targetPort_thread.isRunning:
            self.auto_get_targetPort_thread.terminate()
        self.auto_get_targetPort_thread.start()

    def auto_search(self):
        logging.debug('auto_search ...')
        self.searchAuto.setIconVisibleInMenu(True)
        self.searchManualAction.setIconVisibleInMenu(False)
        self.auto_get_targetPort_thread.is_auth = True
        if self.auto_get_targetPort_thread.isRunning:
            self.auto_get_targetPort_thread.terminate()
        self.auto_get_targetPort_thread.start()

    def update_port(self, portList):
        logging.debug('update_port ...')
        self.statusAction.setText(portList[0])
        self.targetPort = portList[1]

        if self.targetPort is not None:
            self.trayIcon.showMessage('PC-Dashboard', '已连接串口' + self.targetPort, icon=0)
            self.statusAction.setIcon(QIcon(':/imgs/link.png'))
            self.port_trans_thread.targetPort = self.targetPort
            self.port_trans_thread.start()
        else:
            self.statusAction.setIcon(QIcon(':/imgs/brightness.png'))

    # USB拔出丢失串口
    def lose_port(self, portStatus):
        if portStatus is False:
            logging.debug('lose_port ...')
            self.port_trans_thread.terminate()
            self.statusAction.setIcon(QIcon(':/imgs/brightness.png'))
            self.statusAction.setText("串口: 未設定")
            self.targetPort = None
            self.auto_get_targetPort_thread.target_port = None

    # 关闭窗体程序
    def quit_app(self):
        QCoreApplication.instance().quit()
        self.trayIcon.setVisible(False)


class Thread_GET_TARGET_PORT_AUTO(QThread):
    # 返回信号list[显示文言,串口号]
    # 如果没有可用串口 第一位"无可用串口" 第二位None
    my_signal = pyqtSignal(list)

    # 与下位机握手的校验字符串
    handshakeStr = 'handshake'

    # 连接的串口
    target_port = None

    def __init__(self):
        super(Thread_GET_TARGET_PORT_AUTO, self).__init__()
        # 自动扫描flg
        self.is_auth = False

    # 线程执行函数
    def run(self):
        if self.is_auth is True:
            while True:
                logging.info("auto search " + str(self.target_port))
                if self.target_port is None:
                    self.getTargetPort()
                self.sleep(10)
        else:
            # 手动扫描只执行一次
            if self.target_port is None:
                self.getTargetPort()

    def getTargetPort(self):
        # 获取所有串口
        portList = list(serial.tools.list_ports.comports())
        if len(portList) > 0:
            # 遍历所有串口
            for port in portList:
                arduino = serial.Serial(port.name, baudrate=115200, timeout=.1)
                data = self.handshake(arduino)
                logging.info(data.decode())
                # 串口握手校验
                if data.decode().strip() == self.handshakeStr:
                    self.my_signal.emit([port.name + "(已连接)", port.name])
                    self.target_port = port.name
                    arduino.close()
                    logging.info(port.name + " is usable")
                else:
                    logging.info(port.name + " can not use")
        else:
            # 没有任何串口
            logging.info("no any port")
            self.target_port = None
            self.my_signal.emit(["串口: 无", None])

    # 串口握手工具方法
    # 一个串口头两次通信response空，不知道为什么。所以发三次每次间隔1s
    def handshake(self, arduino):
        i = 0
        while i < 3:
            arduino.write(bytes(self.handshakeStr, 'utf-8'))
            time.sleep(1)
            i = i + 1
        return arduino.readline()


class Thread_PORT_TRANS(QThread):

    my_signal = pyqtSignal(bool)

    targetPort = None

    def __init__(self):
        super(Thread_PORT_TRANS, self).__init__()
        self.is_on = True

    def run(self):
        while True:
            try:
                # 握手成功后 进行通信
                arduino = serial.Serial(self.targetPort, baudrate=115200, timeout=.1)
                message = "0,0"
                while True:
                    message = str(round(psutil.cpu_percent(0))) + "," + (str)(round(psutil.virtual_memory().percent))
                    logging.info(message)
                    time.sleep(1)
                    arduino.write(bytes(message, 'utf-8'))
                    time.sleep(1)
                    data = arduino.readline()
                    logging.info("response:" + data.decode())
                    self.my_signal.emit(True)
            except Exception:
                # 有异常后停止通信并再次 获取目标串口
                logging.info("lose port")
                self.my_signal.emit(False)
                time.sleep(1)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    share = QSharedMemory()
    share.setKey("main_window_1Xd#65E")

    if share.attach():
        msg_box = QMessageBox()
        msg_box.setWindowTitle("提示")
        msg_box.setWindowIcon(QIcon(":/imgs/icon.png"))
        msg_box.setText("软件已运行   \n请不要多开   ")
        msg_box.setIcon(QMessageBox.Information)
        msg_box.addButton("确定", QMessageBox.YesRole)
        msg_box.exec()
        sys.exit(-1)
    if share.create(1):
        # 关闭所有窗口,也不关闭应用程序
        QApplication.setQuitOnLastWindowClosed(False)
        ex = Example()
        sys.exit(app.exec_())
