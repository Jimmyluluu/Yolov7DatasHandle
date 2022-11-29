# 資料處理輸出時間檔案輸出秒數集時間以及座標
# 輸出格式為（'時間'：['0','x','y','h','w']）第一項0無意義

import os, cv2, sys, PyQt5, time
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog, QMessageBox, QPushButton, QLabel
from PyQt5.QtGui import QIcon

def timer(t):
    n = 0
    while n < t:
        mins, secs = divmod(n, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        print(timer, end="\r")
        time.sleep(1)
        n += 1
      
    print('Fire in the hole!!')

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
            datas.update({str(round(file/fps,2)): text})
            count = count + 1
            f.close
        print(datas)
        return datas #輸出資料夾

def anxiety_status(mp4Name, datas):
    countFps = 0
    localtionsX = []
    localtionsY = []
    tmpX = 0.000
    tmpY = 0.000
    stopFlag = 0
    status = "Normal"
    cap = cv2.VideoCapture(mp4Name)
    fps = cap.get(cv2.CAP_PROP_FPS)

    for data in datas:
        countFps += 1
        ret, frame = cap.read()
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, status, (150, 50), font, 1, (0, 255, 255), 2, cv2.LINE_4)
        cv2.putText(frame, str(int(float(data))) + "s", (20, 50), font, 1, (0, 255, 255), 2, cv2.LINE_4)
        cv2.imshow('video', frame)

        localtionsX.append(float(datas[data][0][1]))
        localtionsY.append(float(datas[data][0][2]))

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        if float(datas[data][0][2]) > 0.8:
            print(str(data) + ":" + "沉底")
            status = "Drop"

        elif countFps == int(fps):
            tmpX = localtionsX[0]
            tmpY = localtionsY[0]
            for i in range(len(localtionsX)):
                if (localtionsX[i] - tmpX < 0.0005 and localtionsY[i] - tmpY < 0.0005):
                    stopFlag +=1
                tmpX = localtionsX[i]
                tmpY = localtionsX[i]
            if stopFlag > fps:
                print(str(data) + ":" + "####靜止####")
                status = "Stop"
            stopFlag = 0
            countFps = 0
        else :
            status = "Normal"
       
    cap.release()
    cv2.destroyAllWindows()

# 選擇檔案的頁面加入頁面
class App(QWidget):
    videoName = ''
    coordinateFolder = ''

    def __init__(self):
        super().__init__()
        self.title = '選擇影片'
        self.left = 10
        self.top = 10
        self.width = 1080
        self.height = 720
        self.initUI()

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

    def closeEvent(self, event):
        replay = QMessageBox.question(self, "關閉視窗", "確定要關閉視窗？", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if replay == QMessageBox.Yes:
            event.accept()
            print("close")
        else:
            event.ignore()

    def callingFunction(self):
        datas = datas_handle(self.videoName, self.coordinateFolder)
        anxiety_status(self.videoName, datas)

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
