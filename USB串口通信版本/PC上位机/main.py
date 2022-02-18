import logging
import sys
import resource
from PyQt5.QtCore import QCoreApplication, QSharedMemory
from PyQt5.QtGui import QIcon
# 从PyQt库导入QtWidget通用窗口类,基本的窗口集在PyQt5.QtWidgets模块里.
from PyQt5.QtWidgets import (QAction, QApplication, QMenu, QMessageBox, QSystemTrayIcon, QWidget)

from ThreadGetTargetPortAuto import Thread_GET_TARGET_PORT_AUTO
from ThreadPortTrans import Thread_PORT_TRANS

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

    # 手动扫描函数
    def start_search(self):
        logging.debug('manual_search ...')
        self.searchManualAction.setIconVisibleInMenu(True)
        self.searchAuto.setIconVisibleInMenu(False)
        self.auto_get_targetPort_thread.is_auth = False
        if self.auto_get_targetPort_thread.isRunning:
            self.auto_get_targetPort_thread.terminate()
        self.auto_get_targetPort_thread.start()

    # 自动扫描函数
    def auto_search(self):
        logging.debug('auto_search ...')
        self.searchAuto.setIconVisibleInMenu(True)
        self.searchManualAction.setIconVisibleInMenu(False)
        self.auto_get_targetPort_thread.is_auth = True
        if self.auto_get_targetPort_thread.isRunning:
            self.auto_get_targetPort_thread.terminate()
        self.auto_get_targetPort_thread.start()

    # 更新扫描结果
    def update_port(self, portList):
        logging.debug('update_port ...')
        self.statusAction.setText(portList[0])
        self.targetPort = portList[1]

        if self.targetPort is not None:
            self.trayIcon.showMessage('PC-Dashboard', '已连接串口' + self.targetPort, icon=0)
            self.statusAction.setIcon(QIcon(':/imgs/link.png'))
            # 将获取到的串口号传递给 传输数据用的线程
            self.port_trans_thread.targetPort = self.targetPort
            self.port_trans_thread.start()
        else:
            # 没有扫描到端口
            self.statusAction.setIcon(QIcon(':/imgs/brightness.png'))

    # 串口通信时，如果USB拔出丢失串口，需要更新状态
    def lose_port(self, portStatus):
        if portStatus is False:
            self.port_trans_thread.terminate()
            self.statusAction.setIcon(QIcon(':/imgs/brightness.png'))
            self.statusAction.setText("串口: 未設定")
            self.targetPort = None
            self.auto_get_targetPort_thread.target_port = None

    # 关闭窗体程序
    def quit_app(self):
        QCoreApplication.instance().quit()
        self.trayIcon.setVisible(False)


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
