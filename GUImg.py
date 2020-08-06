from tkinter import *
from tkinter.filedialog import *    
from PIL import Image
from PIL import ImageTk
import numpy as np
#from scipy import ndimage.filters
import cv2

def clicRechercher():
    global Frame1, Frame2, gray, img_RGB
    filepath = askopenfilename(title="Importer une image")
    if len(filepath)>0:
        img=cv2.imread(filepath)
        w=300
        #print(img.shape)
        img = cv2.resize(img, (w,int((w/img.shape[1])*img.shape[0])), 0, 0, cv2.INTER_NEAREST)
        img_RGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        #Cpying RGB image for local process
        img_rgb = img_RGB.copy()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        #Display origial image
        img_rgb = Image.fromarray(img_rgb)
        img_rgb = ImageTk.PhotoImage(img_rgb)
        Frame1.configure(image=img_rgb)
        Frame1.image=img_rgb
        #Display gray image
        graydisp = Image.fromarray(gray)
        graydisp = ImageTk.PhotoImage(graydisp)
        Frame2.configure(image=graydisp)
        Frame2.image = graydisp


def clicTraiter():
    global val, Seuillage
    seuil = val.get()
    seuillage = Seuillage.get()
    ret,thresh = cv2.threshold(gray,seuil,255,seuillage)
    thresh = Image.fromarray(thresh)
    thresh = ImageTk.PhotoImage(thresh)
    Frame2.configure(image=thresh)
    Frame2.image = thresh
    

def filtreOtsu():
    thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
    thresh = Image.fromarray(thresh)
    thresh = ImageTk.PhotoImage(thresh)
    Frame2.configure(image=thresh)
    Frame2.image = thresh


def watershadeSeg():
    thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)[1]
    kernel = np.ones((3,3), np.uint8)
    opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel,iterations=1)
    sure_bg = cv2.dilate(opening,kernel,iterations=2)

    # Finding sure foreground area
    dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,5)
    ret, sure_fg = cv2.threshold(dist_transform,0.7*dist_transform.max(),255,0)

    # Finding unknown region
    sure_fg = np.uint8(sure_fg)
    unknown = cv2.subtract(sure_bg,sure_fg)

    # Marker labelling
    ret, markers = cv2.connectedComponents(sure_fg)
    # Add one to all labels so that sure background is not 0, but 1
    markers = markers+1
    
    # Now, mark the region of unknown with zero
    markers[unknown==255] = 0
    markers = cv2.watershed(img_RGB, markers)
    img_RGB[markers == -1] = [255,0,0]
    segmented = Image.fromarray(img_RGB)
    segmented  = ImageTk.PhotoImage(segmented)
    Frame2.configure(image=segmented)
    Frame2.image = segmented


def autoConstarste():
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    cl1 = clahe.apply(gray)
    thresh = Image.fromarray(cl1)
    thresh = ImageTk.PhotoImage(thresh)
    Frame2.configure(image=thresh)
    Frame2.image = thresh


fenetre = Tk()
fenetre.geometry("820x760")
fenetre.title("HELPDOCTOR X-RAY")
P=PanedWindow(fenetre, orient=VERTICAL)
P.pack(side=TOP, expand=Y, fill=BOTH)

Chargement = LabelFrame(P, text="Charger une image")
boutonFile = Button(Chargement,text="Rechercher image", command = clicRechercher)
boutonFile.pack(pady=5)
P.add(Chargement)

Reglage = LabelFrame(P, text="Réglages", padx=5, pady=5)
PReglage = PanedWindow(Reglage, orient=HORIZONTAL)
frameSeuil=Frame(PReglage)
val=IntVar()

Scale(frameSeuil, variable=val,from_=0, to=255,orient=HORIZONTAL,tickinterval=20, length=350, label='Valeur du seuil').pack()

PReglage.add(frameSeuil)
barre = Frame(PReglage,height=100,width=2,bg="black")
barre.pack()
PReglage.add(barre)

frameSeuilage=Frame(PReglage)
Label(frameSeuilage, text="Type de seuilage").pack()

Seuillage = IntVar()

R1 = Radiobutton(frameSeuilage, text="Binaire", variable=Seuillage, value=0).pack(anchor = W)
R2 = Radiobutton(frameSeuilage, text="Binaire Inversé", variable=Seuillage, value=1).pack(anchor = W)
R3 = Radiobutton(frameSeuilage, text="Tronqué", variable=Seuillage, value=2).pack(anchor = W)
R4 = Radiobutton(frameSeuilage, text="Seuil à 0", variable=Seuillage, value=3).pack(anchor = W)
R5 = Radiobutton(frameSeuilage, text="Seuil à 0 inversé", variable=Seuillage, value=4).pack(anchor = W)

PReglage.add(frameSeuilage)

frameOperation = LabelFrame(PReglage, text="Autres opérations", padx=5, pady=2)
frameOperation['borderwidth'] = 4
Button(frameOperation,text="Suillage automatique", command=filtreOtsu).pack(padx=5,pady=5)
Button(frameOperation,text="Contours automatique", command=watershadeSeg).pack(padx=5,pady=5)
Button(frameOperation,text="Amélioration automatique",command=autoConstarste).pack(padx=5,pady=5)

PReglage.add(frameOperation)
PReglage.pack(padx=5, pady=5)


Button(Reglage,text = "Traiter", command = clicTraiter).pack(padx=5,pady=5)
Reglage.pack()
P.add(Reglage)

PanelB=LabelFrame(P,text = "Affichage", width=500, height=120)
Frame1 = Label(PanelB)
Frame1.pack(padx=5, pady=5,side=LEFT)
Frame2 = Label(PanelB)
Frame2.pack(padx=5, pady=5,side=RIGHT)
PanelB.pack()
P.add(PanelB)
fenetre.mainloop()
