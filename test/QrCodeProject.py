import cv2
import numpy as np
from pyzbar.pyzbar import decode
import csv

#img = cv2.imread('1.png')
cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)

# with open('myDataFile.text') as f:
#     myDataList = f.read().splitlines()

f = open('hoso.csv', "r")
data = csv.reader(f)
data = np.array(list(data))
print(len(data))

i=0
listData=[]
while True:

    success, img = cap.read()
    for barcode in decode(img):
        myData = barcode.data.decode('utf-8')
        print(myData) 
        myColor=''
        for i in range(0,len(data)):
            listData.append(data[i][0])
            if data[i][0]==myData:
                 print('data[i][0])', data[i][0])
                 print('gia tri i:', i)
                 myOutput = f'tiem {data[i][2]} mui'

                 if data[i][2] =='0':
                     myColor = (0, 0, 255)

                 elif data[i][2] =='1':
                     myColor = (0, 215, 255)

                 elif data[i][2] =='2':
                     myColor = (0, 255, 0)

                 pts = np.array([barcode.polygon], np.int32)
                 pts = pts.reshape((-1, 1, 2))
                 cv2.polylines(img, [pts], True, myColor, 5)
                 pts2 = barcode.rect
                 cv2.putText(img, myOutput, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX,
                         0.9, myColor, 2)



            if myData  not in listData:
                print(' data[i][0] kkk',data[i][0])
                myOutput ='user unknow'
                myColor = (0, 0, 255)
                pts = np.array([barcode.polygon], np.int32)
                pts = pts.reshape((-1, 1, 2))
                cv2.polylines(img, [pts], True, myColor, 5)
                pts2 = barcode.rect
                cv2.putText(img, myOutput, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX,0.9, myColor, 2)

    cv2.imshow('Result',img)
    cv2.waitKey(1)

