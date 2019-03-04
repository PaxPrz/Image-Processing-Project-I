

from tkinter import *
from PIL import Image,ImageTk
import numpy as np
from tkinter.messagebox import *
import os


from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg

from copy import deepcopy


def mul(t):
  ans=1
  for i in t:
    ans*=i
  return ans


def powerlaw():
    v=power_entry.get()
    try:
        v=float(v)
        if(v>=0.001 and v<=100.0):
            img = image**v
            img[img>255]=255
            img[img<0]=0
            histogramShow(img)
            data = Image.fromarray(img)
            img = ImageTk.PhotoImage(image=data, master=master)
            panel.configure(image=img)
            panel.image = img
        sliderDefault()
    except:
        showerror('Grayscale req', 'Try grayscaling first')


def brightness(event):
    try:
        v=slider.get()
        img = image+v
        img[img>255]=255
        img[img<0]=0
        histogramShow(img)
        data = Image.fromarray(img)
        img = ImageTk.PhotoImage(image=data, master=master)
        panel.configure(image=img)
        panel.image = img
    except:
        showerror('Grayscale req', 'Try grayscaling first')


image_name=[x for x in os.listdir() if x.endswith(('PNG','JPG','png','jpg','JPEG','jpeg'))]
count=1


def change():
    global count
    global image
    data = Image.open(image_name[count])
    image = np.array(data)
    img=ImageTk.PhotoImage(data, master=master)
    panel.configure(image=img)
    panel.image = img
    count=(count+1)%len(image_name)

#convert to grayscale
def grayscale():
    global image
    global panel
    img=[]
    for i in image:
      img_line=[]
      for j in i:
        img_line.append(np.average(j))
      img.append(np.array(img_line))
    image = np.array(img).astype('uint16')
    histogramShow(image)
    data = Image.fromarray(image)
    img = ImageTk.PhotoImage(image=data, master=master)
    panel.configure(image=img)
    panel.image = img
    sliderDefault()

def histogramShow(img):
    a.clear()
    a.hist(img.reshape((mul(img.shape),)), 256, [0,256])
    histCanvas.show()
    #histCanvas.get_tk_widget().pack(side=LEFT, fill=BOTH, expand=False)


def sliderDefault():
    if(slider.get()!=0):
            slider.set(0)


def getFilterValues():
    l=[]
    l.append([float(x11v.get()), float(x12v.get()), float(x13v.get())])
    l.append([float(x21v.get()), float(x22v.get()), float(x23v.get())])
    l.append([float(x31v.get()), float(x32v.get()), float(x33v.get())])
    return l


def fillGaussian():
    x11v.set(0.0625)
    x12v.set(0.125)
    x13v.set(0.0625)
    x21v.set(0.125)
    x22v.set(0.25)
    x23v.set(0.125)
    x31v.set(0.0625)
    x32v.set(0.125)
    x33v.set(0.0625)
    scalev.set(1.0)

def sobelFilter():
    x11v.set(1)
    x12v.set(3)
    x13v.set(1)
    x21v.set(0)
    x22v.set(0)
    x23v.set(0)
    x31v.set(-1)
    x32v.set(-3)
    x33v.set(-1)
    scalev.set(1.0)


def useFilter():
    try:
        f=getFilterValues()
        div = float(scalev.get())
    except x:
        showerror('FillIt', 'Fill float values in all the boxes')
        return
    try:
        img=[]
        for i in range(image.shape[0]):
            line=[]
            for j in range(image.shape[1]):
                if(i==0 or j==0 or i==(image.shape[0]-1) or j==(image.shape[1]-1)):
                    line.append(0)
                else:
                    val=0.0
                    for p in range(3):
                        for q in range(3):
                            val += f[p][q]*image[i+p-1][j+q-1]/div
                    line.append(val)
            img.append(np.array(line))
        img = np.array(img).astype('uint16')
        img[img>255]=255
        img[img<0]=0
        histogramShow(img)
        data = Image.fromarray(img)
        img = ImageTk.PhotoImage(image=data, master=master)
        panel.configure(image=img)
        panel.image = img
        sliderDefault()  
    except:
        showerror('Grayscale','Try grayscale first')


def filterMe(which):
    try:
        img=[]
        for i in range(image.shape[0]):
            line=[]
            for j in range(image.shape[1]):
                if(i==0 or j==0 or i==(image.shape[0]-1) or j==(image.shape[1]-1)):
                    line.append(0)
                else:
                    val=0.0
                    if(which=='min'):
                        val=255
                    for p in range(3):
                        for q in range(3):
                            if(which=='mean'):
                                val += image[i+p-1][j+q-1]
                            if(which=='max'):
                                val = image[i+p-1][j+q-1] if image[i+p-1][j+q-1]>val else val
                            if(which=='min'):
                                val = image[i+p-1][j+q-1] if image[i+p-1][j+q-1]<val else val
                    if(which=='mean'):
                        val=val/9
                    line.append(val)
            img.append(np.array(line))
        img = np.array(img).astype('uint16')
        img[img>255]=255
        img[img<0]=0
        histogramShow(img)
        data = Image.fromarray(img)
        img = ImageTk.PhotoImage(image=data, master=master)
        panel.configure(image=img)
        panel.image = img
        sliderDefault()  
    except:
        showerror('Grayscale','Try grayscale first')



def threshold(th):
    try:
        if(th<0 or th>255):
            showerror('value error','threshold must be betn 0 to 255')
            return
        img = deepcopy(image)
        img[img>th]=255
        img[img<=th]=0        
        histogramShow(img)
        data = Image.fromarray(img)
        img = ImageTk.PhotoImage(image=data, master=master)
        panel.configure(image=img)
        panel.image = img
        sliderDefault()
    except:
        showerror('threshold','enter threshold value (0-255)')
        
if __name__=="__main__":    
    master = Tk()
    
    gray_button = Button(master, text="GrayScale", command=grayscale)
    gray_button.pack()
    bt=Button(master, text='change', command=change)
    bt.pack()
    
    slider=Scale(master, from_=-255, to=255, orient=HORIZONTAL, length=500, tickinterval=255)
    slider.bind('<ButtonRelease-1>', brightness)
    slider.pack()
    power_entry = Entry(master, width=5)
    power_entry.pack()
    power_entry_button = Button(master, text='Power', command=powerlaw)
    power_entry_button.pack()
    # canvas = Canvas(master, width = 500, height = 500)
    # canvas.pack()
    data = Image.open(image_name[0])
    image = np.array(data)
    #img = Image.fromarray(gs(image))
    img = ImageTk.PhotoImage(data, master=master)
    panel = Label(master, image=img)
    panel.image = img
    panel.pack(side=LEFT, fill='both', expand='yes')
    
    histFrame = Frame(master=master)
    
    f = Figure(figsize=(4,4), dpi=100)
    a =  f.add_subplot(111)
    a.hist(image.reshape((mul(image.shape),)), 256, [0,256])
    #a.plot([1,2,3,4,5,6,7,8],[4,3,7,8,3,7,4,6])
    
    histCanvas = FigureCanvasTkAgg(f, master=histFrame)
    histCanvas.show()
    histCanvas.get_tk_widget().pack(side=LEFT, fill=BOTH, expand=False)
    
    toolbar = NavigationToolbar2TkAgg(histCanvas, histFrame)
    histCanvas._tkcanvas.pack(side=BOTTOM, fill=BOTH, expand=False)
    
    histFrame.pack(side=LEFT, fill=BOTH, expand=True)
    
    filterframe = Frame(master=master, width=210, height=300)
    x11v=DoubleVar(master)
    x11 = Entry(master=filterframe, width=10, textvariable=x11v)
    x11.place(x=10, y=10, width=60, height=20)
    x12v=DoubleVar(master)
    x12 = Entry(master=filterframe, width=10, textvariable=x12v)
    x12.place(x=80, y=10, width=60, height=20)
    x13v=DoubleVar(master)
    x13 = Entry(master=filterframe, width=10, textvariable=x13v)
    x13.place(x=150, y=10, width=60, height=20)
    x21v=DoubleVar(master)
    x21 = Entry(master=filterframe, width=10, textvariable=x21v)
    x21.place(x=10, y=40, width=60, height=20)
    x22v=DoubleVar(master)
    x22 = Entry(master=filterframe, width=10, textvariable=x22v)
    x22.place(x=80, y=40, width=60, height=20)
    x23v=DoubleVar(master)
    x23 = Entry(master=filterframe, width=10, textvariable=x23v)
    x23.place(x=150, y=40, width=60, height=20)
    x31v=DoubleVar(master)
    x31 = Entry(master=filterframe, width=10, textvariable=x31v)
    x31.place(x=10, y=70, width=60, height=20)
    x32v=DoubleVar(master)
    x32 = Entry(master=filterframe, width=10, textvariable=x32v)
    x32.place(x=80, y=70, width=60, height=20)
    x33v=DoubleVar(master)
    x33 = Entry(master=filterframe, width=10, textvariable=x33v)
    x33.place(x=150, y=70, width=60, height=20)
    scalev=DoubleVar(master,value=1.0)
    xscale = Entry(master=filterframe, width=10, textvariable=scalev)
    xscale.place(x=80, y=100, width=60, height=20)
    filterbutton = Button(filterframe, text='Filter', command=useFilter)
    filterbutton.place(x=80, y=130)
    gaubutton = Button(filterframe, text='Gaussian', command=fillGaussian)
    gaubutton.place(x=10, y=160)
    sobbutton = Button(filterframe, text='Sobel', command=sobelFilter)
    sobbutton.place(x=80, y=160)
    
    Button(filterframe, text='Mean', command=lambda:filterMe('mean')).place(x=10, y=200)
    Button(filterframe, text='Max', command=lambda:filterMe('max')).place(x=10, y=230)
    Button(filterframe, text='Min', command=lambda:filterMe('min')).place(x=10, y=260)
    xth = DoubleVar(master, value=127.0)
    thEntry = Entry(filterframe, width=5, textvariable=xth)
    thEntry.place(x=120, y=250)
    Button(filterframe, text='Threshold', command=lambda:threshold(xth.get())).place(x=100, y=270)
    
    filterframe.pack(side=LEFT, fill=BOTH, expand=False)
    #canvas.create_image(20,20, anchor=NW, image=ImageTk.PhotoImage(data))
    mainloop()

