import sys
import serial
import serial.tools.list_ports
import psutil
import time
from PyQt5.QtCore import QCoreApplication, QLockFile, QThread, pyqtSignal
from PyQt5.QtGui import QIcon
# 从PyQt库导入QtWidget通用窗口类,基本的窗口集在PyQt5.QtWidgets模块里.
from PyQt5.QtWidgets import (QAction, QApplication, QMenu, QMessageBox, QSystemTrayIcon, QWidget)


class Example(QWidget):
    # 串口对象
    targetPort = None

    def __init__(self):
        super(Example, self).__init__()

        # 设置系统托盘图标的菜单

        def quitApp():
            # 关闭窗体程序
            QCoreApplication.instance().quit()
            self.trayIcon.setVisible(False)

        self.trayIconMenu = QMenu()

        self.statusAction = QAction("&串口: 未設定")
        self.statusAction.setIcon(QIcon('./imgs/brightness.png'))
        self.trayIconMenu.addAction(self.statusAction)

        self.searchPortMenu = QMenu('&扫描串口')

        self.searchAuto = QAction('&自动扫描')
        self.searchAuto.setIcon(QIcon('./imgs/checked.png'))
        self.searchAuto.setIconVisibleInMenu(False)
        self.searchAuto.triggered.connect(self.auto_search)
        self.searchPortMenu.addAction(self.searchAuto)

        self.searchManualAction = QAction('&手动扫描')
        self.searchManualAction.setIcon(QIcon('./imgs/checked.png'))
        self.searchManualAction.setIconVisibleInMenu(False)
        self.searchManualAction.triggered.connect(self.start_search)
        self.searchPortMenu.addAction(self.searchManualAction)

        self.trayIconMenu.addMenu(self.searchPortMenu)

        self.closeAction = QAction('&退出', triggered=quitApp)  # 直接退出可以用qApp.quit
        self.trayIconMenu.addAction(self.closeAction)

        # 在系统托盘处显示图标
        self.trayIcon = QSystemTrayIcon(self)
        self.trayIcon.setIcon(QIcon('./imgs/test.png'))
        self.trayIcon.setContextMenu(self.trayIconMenu)
        self.trayIcon.show()

        # 实例化线程对象(串口扫描)
        self.auto_get_targetPort_thread = Thread_GET_TARGET_PORT_AUTO()
        self.auto_get_targetPort_thread.my_signal.connect(self.update_port)

        # 实例化线程对象(串口通信)
        self.port_trans_thread = Thread_PORT_TRANS()
        self.port_trans_thread.my_signal.connect(self.lose_port)

    def start_search(self):
        self.searchManualAction.setIconVisibleInMenu(True)
        self.searchAuto.setIconVisibleInMenu(False)
        self.auto_get_targetPort_thread.is_auth = False
        if self.auto_get_targetPort_thread.isRunning:
            self.auto_get_targetPort_thread.terminate()
        self.auto_get_targetPort_thread.start()

    def auto_search(self):
        self.searchAuto.setIconVisibleInMenu(True)
        self.searchManualAction.setIconVisibleInMenu(False)
        self.auto_get_targetPort_thread.is_auth = True
        if self.auto_get_targetPort_thread.isRunning:
            self.auto_get_targetPort_thread.terminate()
        self.auto_get_targetPort_thread.start()

    def update_port(self, portList):
        self.statusAction.setText(portList[0])
        self.targetPort = portList[1]

        if self.targetPort is not None:
            self.trayIcon.showMessage('PC-Dashboard', '已连接串口' + self.targetPort, icon=0)
            self.statusAction.setIcon(QIcon('./imgs/link.png'))
            self.port_trans_thread.targetPort = self.targetPort
            self.port_trans_thread.start()
        else:
            self.statusAction.setIcon(QIcon('./imgs/brightness.png'))

    # USB拔出丢失串口
    def lose_port(self, portStatus):
        if portStatus is False:
            self.port_trans_thread.terminate()
            self.statusAction.setIcon(QIcon('./imgs/brightness.png'))
            self.statusAction.setText("串口: 未設定")
            self.targetPort = None
            self.auto_get_targetPort_thread.target_port = None

        # 信息提示
        # 参数1：标题
        # 参数2：内容
        # 参数3：图标（0没有图标 1信息图标 2警告图标 3错误图标），0还是有一个小图标
        # tp.showMessage('tp', 'tpContent', icon=0)

        # def message():
        #     print("弹出的信息被点击了")

        # tp.messageClicked.connect(message)

        # def act(reason):
        # 鼠标点击icon传递的信号会带有一个整形的值，1是表示单击右键，2是双击，3是单击左键，4是用鼠标中键点击
        # if reason == 2 or reason == 3:
        #     w.show()
        # print("系统托盘的图标被点击了")

        # tp.activated.connect(act)


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
                print("auto search " + str(self.target_port))
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
                print(data.decode())
                # 串口握手校验
                if data.decode().strip() == self.handshakeStr:
                    self.my_signal.emit([port.name + "(已连接)", port.name])
                    self.target_port = port.name
                    arduino.close()
                    print(port.name + " is usable")
                else:
                    print(port.name + " can not use")
        else:
            # 没有任何串口
            print("no any port")
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
                    print(message)
                    time.sleep(1)
                    arduino.write(bytes(message, 'utf-8'))
                    time.sleep(1)
                    data = arduino.readline()
                    print("response:" + data.decode())
                    self.my_signal.emit(True)
            except Exception:
                # 有异常后停止通信并再次 获取目标串口
                print("lose port")
                self.my_signal.emit(False)
                time.sleep(1)


if __name__ == '__main__':

    # 防止程序多开
    file = QLockFile('./single_app.lock')
    file.setStaleLockTime(0)
    if not file.tryLock():
        print('禁止程序多开')
        sys.exit(0)

    app = QApplication(sys.argv)
    # 关闭所有窗口,也不关闭应用程序
    QApplication.setQuitOnLastWindowClosed(False)
    ex = Example()
    sys.exit(app.exec_())
