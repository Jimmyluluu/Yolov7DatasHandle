import os
import cv2

def datas_handle():
    vid_cap = cv2.VideoCapture('/Users/lujingyuan/Desktop/fish01/Fish01.mp4')
    fps = vid_cap.get(cv2.CAP_PROP_FPS)
    print(fps)
    datas = {}
    count = 0 #秒數
    filesortNum = []
    folderName = ""
    folderPath = "/Users/lujingyuan/Desktop/fish01/labels"
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