import time
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
import tkinter
from typing import Sized
import cv2
import PIL.Image, PIL.ImageTk
from time import sleep
from threading import Thread
import numpy as np
from pyzbar.pyzbar import decode
import csv
import pyglet
import threading


window = Tk()
window.title("Tracking")

video = cv2.VideoCapture(0)
canvas_w=720
canvas_h=500
canvas = Canvas(window, width = canvas_w, height= canvas_h , bg= "green")
photo = None
count = 0




f = open('hoso.csv', 'r')
data = csv.reader(f)
data = np.array(list(data))
print(len(data))

i=0
listData=[]
def void1():
    music = pyglet.resource.media('pass.ogg')
    music.play()

def void2():
    music = pyglet.resource.media('police.wav')
    music.play()

def update_frame():
    global canvas, photo, bw, count 
    # Doc tu camera
    ret, frame = video.read()

    for barcode in decode(frame):
        myData = barcode.data.decode('utf-8')
        print(myData)  # [111,'luutunglinh','tiem 1 mui']
        myColor = ''
        for i in range(0, len(data)):

            listData.append(data[i][0])
            if data[i][0] == myData:
                # threading.Thread(target=void1).start()
                void1()
                print('data[i][0])', data[i][0])
                print('gia tri i:', i)
                myOutput = f'tiem {data[i][2]} mui'

                if data[i][2] == '0':
                    myColor = (0, 0, 255)

                elif data[i][2] == '1':
                    myColor = (0, 215, 255)

                elif data[i][2] == '2':
                    myColor = (0, 255, 0)
                # tạo bounding box
                pts = np.array([barcode.polygon], np.int32)
                pts = pts.reshape((-1, 1, 2)) # duỗi về 1 hàng 2 cột
                cv2.polylines(frame, [pts], True, myColor, 5)
                pts2 = barcode.rect
                cv2.putText(frame, myOutput, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX,
                            0.9, myColor, 2)
                listbox.delete(0, END)
                listbox.insert(END, "Name : {}".format(data[i][1]))
                listbox.insert(END, "Injections: {}".format(data[i][2]))
                listbox.insert(END, "Vaccine 1 : {}".format(data[i][3]))
                listbox.insert(END, "Vaccine 2: {}".format(data[i][4]))


            if myData not in listData:
                # print(' data[i][0] kkk', data[i][0])
                myOutput = 'user unknow'
                myColor = (0, 0, 255)
                void2()
                pts = np.array([barcode.polygon], np.int32)
                pts = pts.reshape((-1, 1, 2))
                cv2.polylines(frame, [pts], True, myColor, 5)
                pts2 = barcode.rect
                cv2.putText(frame, myOutput, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX,
                            0.9, myColor, 2)



    # Ressize
    frame = cv2.resize(frame, dsize=None, fx=1.2, fy=1.2)
    # Chuyen he mau

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # Convert hanh image TK
    photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    # Show
    canvas.create_image(0,0, image = photo, anchor=tkinter.NW)

    window.after(15, update_frame) # sau 15ms là nó gọi update_frame

update_frame()


Label(window,text="tracking covid",font=("tahoma",16)).grid(row=0,columnspan=2)
canvas.grid(rowspan=2,column=0)


Label(window,text="User Information",font=("tahoma",16)).place(x=770,y=70)
listbox=Listbox(window,width=30,height=10,font=("Arial Bold",12),fg='lime')
listbox.grid(row=1,column=3)




# frameButton=Frame()
# Label(frameButton,text="User Information",font=("tahoma",16)).pack(side=TOP)

# listbox=Listbox(frameButton,width=30,height=10,font=("Arial Bold",12),fg='lime').pack(side=BOTTOM)

# frameButton.grid(row=1,column=1)


button=Button(window,text='Thoat',command=window.quit)
button.grid(row=3,columnspan=2)


window.mainloop()