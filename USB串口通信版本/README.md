
## 软件实现思路
### 1.上位机程序
这个分支使用了Python的psutil包来获取cpu以及ram信息。 
再利用pyserial包通过串口与下位机进行交互。 

作为web软件工程师，原本想使用最熟悉的Java语言来实现上位机的程序。  
但经过调查，发现使用Java进行串口通信的依赖包使用起来比较复杂，  
于是放弃了Java，选择了Python。

并且使用Python后可以利用pyqt5来制作上位机图形界面，也比较容易。


### 2.下位机(Esp32)
下位机接收到文本数据后如何显示在电压表上,也与main分支稍微不同。  
我使用了ledcwrite的PWM来处理信息的显示。  

由于基于串口通信，不依赖wifi。理论上下位机可以替换成arduino uno等单片机。  
但同样因为PWM的原因arduino与esp32写法存在差异，目前下位机代码只能在esp32上运行。

## 开发指南
### 1.上位机
上位机采用python开发，图形库为pyqt5。开发IDE为vscode。
#### 启动
1. `cd USB串口通信版本/PC上位机` 进入上位机文件夹
2. `pip install -r requirements.txt` 安装开发依赖
3. `python main.py`  启动上位机
#### 依赖包
使用`pip`新增或变更依赖后请执行下列来更新依赖文件
```
pip freeze > requirements.txt
```
#### 图片资源文件
修改或变更图片资源后，请在根目录执行下列命令来生成和更新resource.py文件 
```
pyrcc5 resource.qrc -o resource.py
```
代码中引用图片资源:  
```
self.searchManualAction.setIcon(QIcon(':/imgs/checked.png'))
```
#### 打包可exe执行文件
目前只在windows10 64位机上测试过
```
pyinstaller -F main.py -i ./icon.ico --noconsole
```
解决windows10打包后图标缓存
```
ie4uinit.exe -show
```

### 2.下位机
通过串口接受到数据，下位机采用PWM的方式控制电压表，由于没有使用Wifi传输  
数据，这使得我们可以使用arduino uno等开发板。下位机文件夹里提供了esp32和  
arduino的不同实现。  

核心区别就是esp32使用了`ledcWrite`而arduino uno使用的是`analogWrite`函数。

#### ⚠️串口驱动
⚠️初次使用Esp32在电脑上连接的时候，如果扫描不到串口，需要安装串口驱动。⚠️  
(驱动地址)[https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers]  
安装这个驱动: CP210x Windows Drivers with Serial Enumerator

😭看来使用串口方式还是直接用arduino开发板才能即插即用。唉，心累。


