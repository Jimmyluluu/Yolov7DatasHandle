import os
import cv2

# 資料處理輸出時間檔案輸出秒數集時間以及座標
# 輸出格式為（'時間'：['0','x','y','h','w']）第一項0無意義
def datas_handle():
#--------------開啟影片檔並求出fps------------------#
    vid_cap = cv2.VideoCapture('Fish01.mp4') 
    fps = vid_cap.get(cv2.CAP_PROP_FPS)
#------------------------------------------------#
    datas = {}
    count = 0 #秒數
    filesortNum = []
    folderName = ""
    folderPath = "labels"
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
    return datas

def anxiety_status(datas):
    for data in datas:
        print(float(data[:-1]))


if __name__ == '__main__':
    datas = datas_handle()
    # print(datas)
    anxiety_status(datas)