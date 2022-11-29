# 資料處理輸出時間檔案輸出秒數集時間以及座標
# 輸出格式為（'時間'：['0','x','y','h','w']）第一項0無意義

import os, cv2, sys, csv
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
            datas.update({str(round(file/fps,2)): text})
            count = count + 1
            f.close
        #print(datas)
        return datas #輸出資料夾

def fish_status(mp4Name, datas):
    countFps = 0
    localtionsX = []
    localtionsY = []
    result_datas = {"時間":"狀態"}
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
        cv2.putText(frame, "Print \"Q\" can quit", (20, 120), font, 1, (0, 255, 255), 2, cv2.LINE_4)
        cv2.imshow('video', frame)

        localtionsX.append(float(datas[data][0][1]))
        localtionsY.append(float(datas[data][0][2]))

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        if float(datas[data][0][2]) > 0.8:
            print(str(data) + ":" + "沉底")
            status = "Drop"

        elif countFps > 7:
            if stopFlag == 0:
                tmpX = localtionsX[0]
                tmpY = localtionsY[0]
            
            if abs(localtionsX[-1] - tmpX) < float(datas[data][0][4]) / 5 and abs(localtionsY[-1]) - tmpY < float(datas[data][0][4]) / 5 and stopFlag == 0:
                print(str(data) + ":" + "靜止")
                status = "Stop"
                stopFlag = 1
                print(tmpX)
                print(tmpY)
                tmpX = localtionsX[-1]
                tmpY = localtionsY[-1]
            if stopFlag == 1 and abs(localtionsX[0] - tmpX) < float(datas[data][0][4]) / 7 and abs(localtionsY[0]) - tmpY < float(datas[data][0][4]) / 7:
                print(str(data) + ":" + "靜止")
                status = "Stop"
                print(tmpX)
                print(tmpY)
            else:
                countFps = 0
                stopFlag = 0
            print(countFps)
            print(localtionsX)
            print(localtionsY)
            localtionsX = []
            localtionsY = []

        else :
            status = "Normal"

        result_datas[str(data)+ "s"] =  status

    cap.release()
    cv2.destroyAllWindows()
    return result_datas

# 選擇檔案的頁面加入頁面
class App(QWidget):
    videoName = ''
    coordinateFolder = ''
    result_datas = {}

    def __init__(self):
        super().__init__()
        self.title = '控制面版'
        self.left = 10
        self.top = 10
        self.width = 450
        self.height = 800
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.vidoeButton = QPushButton('影片檔', self)
        self.vidoeButton.setGeometry(130, 50, 200, 70)

        self.folderButton = QPushButton('座標資料夾', self)
        self.folderButton.setGeometry(130, 250, 200, 70)

        self.printButton = QPushButton('產生結果', self)
        self.printButton.setGeometry(130, 450, 200, 70)

        self.exportButton = QPushButton('輸出結果', self)
        self.exportButton.setGeometry(130, 600, 200, 70)

        self.videoLabel = QLabel("檔案為：", self)
        self.videoLabel.setWordWrap(True)
        self.videoLabel.setGeometry(150, 120, 150, 50)

        self.folderLabel = QLabel("資料夾為：", self)
        self.folderLabel.setWordWrap(True)
        self.folderLabel.setGeometry(150, 320, 150, 50)

        self.vidoeButton.clicked.connect(self.openFileNameDialog)
        self.folderButton.clicked.connect(self.openFolderNameDialog)
        self.printButton.clicked.connect(self.printResult)
        self.exportButton.clicked.connect(self.exportResult)

        self.show()

    def closeEvent(self, event):
        replay = QMessageBox.question(self, "關閉視窗", "確定要關閉視窗？", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if replay == QMessageBox.Yes:
            event.accept()
            print("close")
        else:
            event.ignore()

    def exportResult(self, result):
        for file in os.listdir("export"):
            if file == 'export.csv':
                os.remove('export/export.csv')

        if self.result_datas == {}:
            QMessageBox.information(None, '成功', '結果尚未產生')
        else:
            with open('export/export.csv', 'w', newline='') as file:
                writer = csv.writer(file, quoting=csv.QUOTE_ALL)
                for row in self.result_datas.items():
                    writer.writerow(row)
                     
            QMessageBox.information(None, '成功', '檔案存致 export 中，重新輸出後檔案會刪除，請記得將檔案另存')

    def printResult(self):
        if self.videoName == '':
            QMessageBox.information(None, '注意！！', '請輸入影片')
        elif self.coordinateFolder == '':
            QMessageBox.information(None, '注意！！', '請輸入座標檔')
        elif self.videoName.endswith(".mp4")!= True:
            QMessageBox.information(None, '注意！！', '影片檔格式錯誤')

        else: 
            datas = datas_handle(self.videoName, self.coordinateFolder)
            self.result_datas = fish_status(self.videoName, datas)
            QMessageBox.information(None, '恭喜', '成功')
        

    def openFileNameDialog(self):    
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        Name, _ = QFileDialog.getOpenFileName(self,"選擇影片檔", "","All Files (*);;Python Files (*.py)", options=options)
        self.videoName = Name
        if Name:
            self.videoLabel.setText(self.videoName)
            self.videoLabel.setGeometry(150, 120, 200, 70)

    def openFolderNameDialog(self):    
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        Name = str(QFileDialog.getExistingDirectory(self,"選擇座標檔" , options=options))
        self.coordinateFolder = Name
        if Name:
            self.folderLabel.setText(self.coordinateFolder)
            self.folderLabel.setGeometry(150, 320, 200, 70)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    UIWindow = App()
    app.exec_()
