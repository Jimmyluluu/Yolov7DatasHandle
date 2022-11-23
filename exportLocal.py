# 資料處理輸出時間檔案輸出秒數集時間以及座標
# 輸出格式為（'時間'：['0','x','y','h','w']）第一項0無意義

import os, random, cv2, argparse, sys, PyQt5
import sys
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog, QMessageBox, QPushButton
from PyQt5.QtGui import QIcon

# 選擇檔案的頁面加入頁面
class App(QWidget):

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
        self.mybutton = QPushButton('button', self)
        self.mybutton.move(60, 50)
        self.mybutton.clicked.connect(self.openFileNameDialog)

        self.show()

    def openFileNameDialog(self):    
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        videoName, _ = QFileDialog.getOpenFileName(self,"選擇影片()", "","All Files (*);;Python Files (*.py)", options=options)
        if videoName:
            print(videoName)
            print("fileName")


    # def openFileNamesDialog(self):    
    #     options = QFileDialog.Options()
    #     options |= QFileDialog.DontUseNativeDialog
    #     files, _ = QFileDialog.getOpenFileNames(self,"選擇影片)", "","All Files (*);;Python Files (*.py)", options=options)
    #     if files:
    #         print(files)
    #         print("file")
            
    def close_window(self):
    	self.close()


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
    return datas #輸出資料夾

def anxiety_status(datas):
    tmp = 0.0
    for data in datas:
        time = data.split(".")[0]
        if float(datas[data][0][2]) > 0.8:
            print(str(data) + ":" + "沉底")

if __name__ == '__main__':

    app = QApplication(sys.argv)
    UIWindow = App()
    app.exec_()


    parser = argparse.ArgumentParser()
    parser.add_argument("mp4Name", type=str, help='file_name1') #輸入mp4檔案取得fps
    parser.add_argument("coordinateFolder", type=str, help='file_name2') #輸入座標資料夾
    args = parser.parse_args()
    mp4Name = args.mp4Name
    coordinateFolder = args.coordinateFolder

    datas = datas_handle(mp4Name, coordinateFolder)
    anxiety_status(datas)
