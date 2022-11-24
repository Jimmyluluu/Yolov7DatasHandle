# 資料處理輸出時間檔案輸出秒數集時間以及座標
# 輸出格式為（'時間'：['0','x','y','h','w']）第一項0無意義

import os, random, cv2, argparse, sys, PyQt5
import sys
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog, QMessageBox, QPushButton, QLabel
from PyQt5.QtGui import QIcon
def datas_handle(mp4Name, coordinateFolder):
    #--------------開啟影片檔並求出fps------------------#
        vid_cap = cv2.VideoCapture(mp4Name) 
        fps = vid_cap.get(cv2.CAP_PROP_FPS)
    #------------------------------------------------#
        datas = {}
        count = 0 #秒數
        filesortNum = []
        folderName = ""
        folderPath = coordinateFolder
        listdir = os.listdir(folderPath)

        for l in listdir:
            filesortNum.append(int(l.split('_')[1].split('.')[0]))
            folderName = l.split('_')[0]
        filesortNum = (sorted(filesortNum))

        for file in filesortNum:
            text = []
            fileName = folderName + "_" + str(file) + ".txt"
            filepath = os.path.join(folderPath, fileName)

            f = open(filepath)
            for line in f:
                line = line.split(' ')
                if len(line) > 4:
                    line[4] = line[4].replace("\n", "")
                text.append(line)
            datas.update({str(round(file/fps,2)) + "s": text})
            count = count + 1
            f.close
        print(datas)
        return datas #輸出資料夾

def anxiety_status(datas):
    tmp = 0.0
    for data in datas:
        time = data.split(".")[0]
        if float(datas[data][0][2]) > 0.8:
            print(str(data) + ":" + "沉底")

# 選擇檔案的頁面加入頁面
class App(QWidget):
    videoName = ''
    coordinateFolder = ''

    def __init__(self):
        super().__init__()
        self.title = '選擇影片'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()

    def closeEvent(self, event):
        replay = QMessageBox.question(self, "關閉視窗", "確定要關閉視窗？", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if replay == QMessageBox.Yes:
            event.accept()
            print("close")
        else:
            event.ignore()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.buttonOne = QPushButton('影片檔', self)
        self.buttonOne.move(60, 50)

        self.buttonTwo = QPushButton('座標資料夾', self)
        self.buttonTwo.move(60, 150)

        self.buttonThree = QPushButton('印出沈底', self)
        self.buttonThree.move(60, 250)

        self.labelOne = QLabel("檔案為：", self)
        self.labelOne.setGeometry(70, 70, 300, 50)

        self.labelTwo = QLabel("資料夾為：", self)
        self.labelTwo.setGeometry(70, 170, 300, 50)

        self.buttonOne.clicked.connect(self.openFileNameDialog)
        self.buttonTwo.clicked.connect(self.openFolderNameDialog)
        self.buttonThree.clicked.connect(self.callingFunction)

        self.show()

    def callingFunction(self):
        datas = datas_handle(self.videoName, self.coordinateFolder)
        anxiety_status(datas)

    def openFileNameDialog(self):    
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        Name, _ = QFileDialog.getOpenFileName(self,"選擇影片()", "","All Files (*);;Python Files (*.py)", options=options)
        self.videoName = Name
        if Name:
            print(Name)
            self.labelOne.setText(self.videoName)
            self.labelOne.setGeometry(70, 70, 300, 50)

    def openFolderNameDialog(self):    
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        Name = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.coordinateFolder = Name
        if Name:
            print(Name)
            self.labelTwo.setText(self.coordinateFolder)
            self.labelTwo.setGeometry(70, 170, 300, 50)


    
if __name__ == '__main__':

    app = QApplication(sys.argv)
    UIWindow = App()
    app.exec_()

