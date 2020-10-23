import sys
import time
from threading import Thread
from collections import Counter
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication,QMainWindow,QWidget,QLCDNumber,QVBoxLayout
from PyQt5 import QtCore, QtGui, QtWidgets
import RPi.GPIO as gpio
counter = 0 
buzzerMotor=12
gpio.setmode(gpio.BCM)
gpio.setwarnings(False)
gpio.setup(buzzerMotor,gpio.OUT)
 
class HMI(QMainWindow):
    
    def __init__(self):
        super(HMI, self).__init__()
        loadUi('magazine.ui',self)
        self.setWindowTitle('Autonomous Fish System')
        self.magazineStart.clicked.connect(self.Mag_Train)
        #self.magazineStart.clicked.connect(self.StartCounting)
    @pyqtSlot()
    def initUI(self):
            result = "Success on "
            timeEnd = time.asctime()
            magazineData = (result + timeEnd)
            self.dataDisplay.setText(magazineData)      
                 
    @pyqtSlot()
    def Mag_Train(self):
        global counter
        gpio.output(buzzerMotor, True)
        counter = counter + 1
        time.sleep(.3)
        gpio.output(buzzerMotor, False)
        self.lcdNumber.display(counter)
        time.sleep(1)
        self.initUI()
        
        
            
            
#     @pyqtSlot()       
#     def StartCounting(self):
#         for counter in range (1, 50):
#             
        
          
            
        
            
            
    
app=QApplication(sys.argv)
widget=HMI()
widget.show()
sys.exit(app.exec_())