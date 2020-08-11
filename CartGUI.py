from tkinter import *
from tkinter.filedialog import *    
from PIL import Image
from PIL import ImageTk
import numpy as np
from datetime import datetime
import cv2
import os


def importImage():
    global Frame1, Frame2, img
    filepath = askopenfilename(title="Choisir une image", filetypes=(('fichiers jpeg','*.jpg'),('fichiers png','*.png')))
    if len(filepath)>0:
        img=cv2.imread(filepath)
        w=300
        img_RGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        img_RGB = cv2.resize(img_RGB, (w,int((w/img.shape[1])*img.shape[0])), 0, 0, cv2.INTER_NEAREST)
                    
        #Display origial image
        img_RGB = Image.fromarray(img_RGB)
        img_RGB = ImageTk.PhotoImage(img_RGB)
        Frame1.configure(image=img_RGB)
        Frame1.image=img_RGB
        
                    


def cartoonizeStyle1(sig_r=0.4, sig_s=50):
    global img_result   
    imgToCartoon = img.copy()
    gray = cv2.cvtColor(imgToCartoon, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray,(3,3) ,0)
    edged = cv2.Laplacian(gray, -1, ksize=5)

    edged = 255 - edged
    edgedPreserve = cv2.edgePreservingFilter(imgToCartoon, flags=2, sigma_s=sig_s, sigma_r=sig_r)
    img_result = cv2.bitwise_and(edgedPreserve, edgedPreserve, mask=edged)
    img_result = cv2.GaussianBlur(img_result,(3,3) ,0)
    img_result = cv2.medianBlur(img_result,3)
    #cv2.imshow("resultat2",result)
    #cv2.imwrite("results/t33.jpg",result)  
    preview = img_result.copy()
    preview = cv2.resize(preview, (300,int((300/img_result.shape[1])*img_result.shape[0])), 0, 0, cv2.INTER_NEAREST)
    preview = cv2.cvtColor(preview,cv2.COLOR_BGR2RGB)
    preview = Image.fromarray(preview)
    preview = ImageTk.PhotoImage(preview)
    Frame2.configure(image=preview)
    Frame2.image=preview


def applyFilter():
    cartoonizeStyle1(sig_r=sigR_val.get(), sig_s=sigS_val.get() if sigS_val.get() > 0 else 10 )


def saveImg():
    img_dir = askdirectory()
    if img_dir != "":
        os.chdir(img_dir)
        now = datetime.timestamp(datetime.now())
        ts = str(now)+".jpg"
        cv2.imwrite(ts,img_result)
    else:
        pass



fenetre = Tk()
fenetre.geometry("720x580")
fenetre.title("EasyCartoon")
p = PanedWindow(fenetre, orient=VERTICAL)                    
p.pack(side=TOP, expand=Y, fill=BOTH)

frameSeuilage=Frame(p)
sigS_val = IntVar()
sigR_val =  DoubleVar()

Scale(frameSeuilage, variable=sigR_val, from_=0.1, to=1, resolution = 0.1, orient=HORIZONTAL, tickinterval=0.1, length=200,label='Lissage').pack()
Scale(frameSeuilage, variable=sigS_val, from_=0, to=200, orient=HORIZONTAL, tickinterval=50, length=300,label='Eclairage').pack()
p.add(frameSeuilage)
                     
frameOperation = LabelFrame(p,text="Controle",padx=5,pady=2,width=500,height=110)
frameOperation['borderwidth'] = 4

Button(frameOperation, text="Importer", command=importImage).pack(padx=5,pady=5)
Button(frameOperation, text="Traiter", command=applyFilter).pack(padx=5,pady=5)
Button(frameOperation, text="Enregistrer", command=saveImg).pack(padx=5,pady=5)
p.add(frameOperation)

PanelB=LabelFrame(p,text="Affichage")
Frame1 = Label(PanelB)
Frame1.pack(padx=5, pady=5,side=LEFT)
Frame2 = Label(PanelB)
Frame2.pack(padx=5, pady=5,side=RIGHT)
PanelB.pack()
p.add(PanelB)
fenetre.mainloop()

