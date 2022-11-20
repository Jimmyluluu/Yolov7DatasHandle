import os, random, cv2, argparse
# 資料處理輸出時間檔案輸出秒數集時間以及座標
# 輸出格式為（'時間'：['0','x','y','h','w']）第一項0無意義

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
    for data in datas:
        if float(datas[data][0][2]) > 0.75:
            time = data.split(".")[0]
            print(str(data) + ":" + "沉底")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("mp4Name", type=str, help='file_name1') #輸入mp4檔案取得fps
    parser.add_argument("coordinateFolder", type=str, help='file_name1') #輸入座標資料夾
    args = parser.parse_args()
    mp4Name = args.mp4Name
    coordinateFolder = args.coordinateFolder

    datas = datas_handle(mp4Name, coordinateFolder)
    anxiety_status(datas)
