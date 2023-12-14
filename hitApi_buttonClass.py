import sys
from PyQt5.QtWidgets import QDialog,QLabel, QWidget, QToolButton,QPushButton, QGridLayout, QVBoxLayout, QHBoxLayout
import requests
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
import os


class APIClientWidget(QDialog):
    
    def __init__(self, FinalBasic_path, camButtonsAPIDic, parent=None):
        super(APIClientWidget, self).__init__(parent)

        self.finalBasePath = FinalBasic_path
        self.camDic = camButtonsAPIDic

        self.button_imgPath = {
            'left': os.path.join(self.finalBasePath,'buttons_images', 'left.png'),
            'right': os.path.join(self.finalBasePath,'buttons_images', 'right.png'),
            'up': os.path.join(self.finalBasePath,'buttons_images', 'up.png'),
            'down': os.path.join(self.finalBasePath,'buttons_images', 'down.png'),
            'zoomup': os.path.join(self.finalBasePath,'buttons_images', 'zoomUp.png'),
            'zoomdown': os.path.join(self.finalBasePath,'buttons_images', 'zoomdown.png'),
            'focusup': os.path.join(self.finalBasePath,'buttons_images', 'focusup.png'),
            'focusdown': os.path.join(self.finalBasePath,'buttons_images', 'focusdown.png')
        }

        # """Buttons API's"""
        # self.leftStart_api = 'http://192.168.1.163/ajaxcom?szCmd={"SysCtrl":{"PtzCtrl":{"nChanel":0,"szPtzCmd":"left_start", "byValue":60}}}'
        # self.leftStop_api = 'http://192.168.1.163/ajaxcom?szCmd={"SysCtrl":{"PtzCtrl":{"nChanel":0,"szPtzCmd":"left_stop", "byValue":60}}}'
        
        # self.rightStart_api = 'http://192.168.1.163/ajaxcom?szCmd={"SysCtrl":{"PtzCtrl":{"nChanel":0,"szPtzCmd":"right_start", "byValue":60}}}'
        # self.rightStop_api = 'http://192.168.1.163/ajaxcom?szCmd={"SysCtrl":{"PtzCtrl":{"nChanel":0,"szPtzCmd":"right_stop", "byValue":60}}}'
        
        # self.upStart_api = 'http://192.168.1.163/ajaxcom?szCmd={"SysCtrl":{"PtzCtrl":{"nChanel":0,"szPtzCmd":"up_start", "byValue":60}}}'
        # self.upStop_api = 'http://192.168.1.163/ajaxcom?szCmd={"SysCtrl":{"PtzCtrl":{"nChanel":0,"szPtzCmd":"up_stop", "byValue":60}}}'
        
        # self.downStart_api = 'http://192.168.1.163/ajaxcom?szCmd={"SysCtrl":{"PtzCtrl":{"nChanel":0,"szPtzCmd":"down_start", "byValue":60}}}'
        # self.downStop_api = 'http://192.168.1.163/ajaxcom?szCmd={"SysCtrl":{"PtzCtrl":{"nChanel":0,"szPtzCmd":"down_stop", "byValue":60}}}'
        
        # self.zoomInStart_api = 'http://192.168.1.163/ajaxcom?szCmd={"SysCtrl":{"PtzCtrl":{"nChanel":0,"szPtzCmd":"zoomadd_start", "byValue":60}}}'
        # self.zoomInStop_api = 'http://192.168.1.163/ajaxcom?szCmd={"SysCtrl":{"PtzCtrl":{"nChanel":0,"szPtzCmd":"zoomadd_stop", "byValue":60}}}'
        
        # self.zoomOutStart_api = 'http://192.168.1.163/ajaxcom?szCmd={"SysCtrl":{"PtzCtrl":{"nChanel":0,"szPtzCmd":"zoomdec_start", "byValue":60}}}'
        # self.zoomOutStop_api = 'http://192.168.1.163/ajaxcom?szCmd={"SysCtrl":{"PtzCtrl":{"nChanel":0,"szPtzCmd":"zoomdec_stop", "byValue":60}}}'
        
        # self.focusInStart_api = 'http://192.168.1.163/ajaxcom?szCmd={"SysCtrl":{"PtzCtrl":{"nChanel":0,"szPtzCmd":"focusadd_start", "byValue":60}}}'
        # self.focusInStop_api = 'http://192.168.1.163/ajaxcom?szCmd={"SysCtrl":{"PtzCtrl":{"nChanel":0,"szPtzCmd":"focusadd_stop", "byValue":60}}}'
        
        # self.focusOutStart_api = 'http://192.168.1.163/ajaxcom?szCmd={"SysCtrl":{"PtzCtrl":{"nChanel":0,"szPtzCmd":"focusdec_start", "byValue":60}}}'
        # self.focusOutStop_api = 'http://192.168.1.163/ajaxcom?szCmd={"SysCtrl":{"PtzCtrl":{"nChanel":0,"szPtzCmd":"focusdec_start", "byValue":60}}}'
        
        
        """Buttons API's"""
        self.leftStart_api = self.camDic['leftStart_but']
        self.leftStop_api = self.camDic['leftStop_but']
        print('self.left: ',self.leftStart_api, self.leftStop_api)
        
        self.rightStart_api = self.camDic['rightStart_but']
        self.rightStop_api = self.camDic['rightStop_but']
        print('self.right: ',self.rightStart_api, self.rightStop_api)
        
        self.upStart_api = self.camDic['upStart_but']
        self.upStop_api = self.camDic['upStop_but']
        print('self.up: ',self.upStart_api, self.upStop_api)
        
        self.downStart_api = self.camDic['downStart_but']
        self.downStop_api = self.camDic['downStop_but']
        print('self.down: ',self.downStart_api, self.downStop_api)
        
        self.zoomInStart_api = self.camDic['zoomInStart_but']
        self.zoomInStop_api = self.camDic['zoomInStop_but']
        print('self.zoomIn: ',self.zoomInStart_api, self.zoomInStop_api)
        
        self.zoomOutStart_api = self.camDic['zoomOutStart_but']
        self.zoomOutStop_api = self.camDic['zoomOutStop_but']
        print('self.zoomOut: ',self.zoomOutStart_api, self.zoomOutStop_api)
        
        self.focusInStart_api = self.camDic['focusInStart_but']
        self.focusInStop_api = self.camDic['focusInStop_but']
        print('self.focusIn: ',self.focusInStart_api, self.focusInStop_api)
        
        self.focusOutStart_api = self.camDic['focusOutStart_but']
        self.focusOutStop_api = self.camDic['focusOutStop_but']
        print('self.focusOut: ',self.focusOutStart_api, self.focusOutStop_api)
        
        self.init_ui()

    def init_ui(self):
        self.HBL = QHBoxLayout()

        self.GridLayout = QGridLayout()

        left_button = QPushButton(self)
        left_button.setIcon(QIcon(self.button_imgPath['left']))
        left_button.setIconSize(left_button.sizeHint())
        left_button.pressed.connect(lambda: self.start_api(self.leftStart_api))
        left_button.released.connect(lambda: self.stop_api (self.leftStop_api))

        # Apply a custom style to round the edges
        left_button.setStyleSheet("border: none; border-radius: 5px")

        right_button = QPushButton(self)
        right_button.setIcon(QIcon(self.button_imgPath['right']))
        right_button.setIconSize(right_button.sizeHint())

        right_button.pressed.connect(lambda: self.start_api(self.rightStart_api))
        right_button.released.connect(lambda: self.stop_api(self.rightStop_api))

        # Apply a custom style to round the edges
        right_button.setStyleSheet("border: none; border-radius: 5px")

        up_button = QPushButton(self)
        up_button.setIcon(QIcon(self.button_imgPath['up']))
        up_button.setIconSize(up_button.sizeHint())
        up_button.pressed.connect(lambda: self.start_api(self.upStart_api))
        up_button.released.connect(lambda: self.stop_api(self.upStop_api))

        # Apply a custom style to round the edges
        up_button.setStyleSheet("border: none; border-radius: 5px")

        down_button = QPushButton(self)
        down_button.setIcon(QIcon(self.button_imgPath['down']))
        down_button.setIconSize(down_button.sizeHint())
        down_button.pressed.connect(lambda: self.start_api(self.downStart_api))
        down_button.released.connect(lambda: self.stop_api(self.downStop_api))
        
        # Apply a custom style to round the edges
        down_button.setStyleSheet("border: none; border-radius: 5px")

        zoomIn_button = QPushButton(self)
        zoomIn_button.setIcon(QIcon(self.button_imgPath['zoomup']))
        zoomIn_button.setIconSize(zoomIn_button.sizeHint())
        zoomIn_button.pressed.connect(lambda: self.start_api(self.zoomInStart_api))
        zoomIn_button.released.connect(lambda: self.stop_api(self.zoomInStop_api))
        
        # Apply a custom style to round the edges
        zoomIn_button.setStyleSheet("border: none; border-radius: 5px")

        zoomOut_button = QPushButton(self)
        zoomOut_button.setIcon(QIcon(self.button_imgPath['zoomdown']))
        zoomOut_button.setIconSize(zoomOut_button.sizeHint())
        zoomOut_button.pressed.connect(lambda: self.start_api(self.zoomOutStart_api))
        zoomOut_button.released.connect(lambda: self.stop_api(self.zoomOutStop_api))
        
        # Apply a custom style to round the edges
        zoomOut_button.setStyleSheet("border: none; border-radius: 5px")

        focusIn_button = QPushButton(self)
        focusIn_button.setIcon(QIcon(self.button_imgPath['focusup']))
        focusIn_button.setIconSize(focusIn_button.sizeHint())
        focusIn_button.pressed.connect(lambda: self.start_api(self.focusInStart_api))
        focusIn_button.released.connect(lambda: self.stop_api(self.focusInStop_api))
        
        # Apply a custom style to round the edges
        focusIn_button.setStyleSheet("border: none; border-radius: 5px")

        focusOut_button = QPushButton(self)
        focusOut_button.setIcon(QIcon(self.button_imgPath['focusdown']))
        focusOut_button.setIconSize(focusOut_button.sizeHint())
        focusOut_button.pressed.connect(lambda: self.start_api(self.focusOutStart_api))
        focusOut_button.released.connect(lambda: self.stop_api(self.focusOutStop_api))
        
        # Apply a custom style to round the edges
        focusOut_button.setStyleSheet("border: none; border-radius: 5px")

        # Set fixed sizes for the buttons
        button_size = (100, 60)  # Adjust the size as needed

        zoomIn_button.setFixedSize(*button_size)
        zoomOut_button.setFixedSize(*button_size)
        focusIn_button.setFixedSize(*button_size)
        focusOut_button.setFixedSize(*button_size)

        self.GridLayout.addWidget(left_button, 1, 1)     # row 1, column 0
        self.GridLayout.addWidget(right_button, 1, 3)    # row 1, column 2
        self.GridLayout.addWidget(up_button, 0, 2)       # row 0, column 1
        self.GridLayout.addWidget(down_button, 2, 2)     # row 2, column 1
        # Set alignment to align buttons to the bottom
        self.GridLayout.setAlignment(Qt.AlignCenter)

        self.VBL1 = QVBoxLayout()
        self.VBL1.addWidget(focusIn_button, 0)     
        self.VBL1.addWidget(focusOut_button, 0)
        focus_label = QLabel('FOCUS', self)
        focus_label.setStyleSheet("background-color: black; color: white;")    
        self.VBL1.addWidget(focus_label, 0, alignment=Qt.AlignCenter)

        # Set alignment to align buttons to the bottom
        self.VBL1.setAlignment(Qt.AlignCenter)

        self.VBL2 = QVBoxLayout()
        self.VBL2.addWidget(zoomIn_button, 0)     
        self.VBL2.addWidget(zoomOut_button, 0) 
        zoom_label = QLabel('ZOOM', self)
        zoom_label.setStyleSheet("background-color: black; color: white;")       
        self.VBL2.addWidget(zoom_label, 0, alignment=Qt.AlignCenter) 

        # Set alignment to align buttons to the bottom
        self.VBL2.setAlignment(Qt.AlignCenter)

        self.HBL.addLayout(self.VBL1)
        self.HBL.addLayout(self.GridLayout)
        self.HBL.addLayout(self.VBL2)
  
        self.setLayout(self.HBL)
        self.setStyleSheet("background-color: black;")

        self.setGeometry(300, 300, 350, 250)
        self.setWindowTitle('Movement buttons')
        self.show()

    def start_api(self, api_url):
        try:
            response = requests.get(api_url)
            if response.status_code == 200:
                print('Start API Response:', response.json())
            else:
                print('Error:', response.status_code)
        except Exception as e:
            print('Error:', e)

    def stop_api(self, api_url):
        try:
            response = requests.get(api_url)
            if response.status_code == 200:
                print('Stop API Response:', response.json())
            else:
                print('Error:', response.status_code)
        except Exception as e:
            print('Error:', e)

