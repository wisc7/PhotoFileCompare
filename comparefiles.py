from tkinter import *
from tkinter import filedialog
#pip install pillow
from PIL import ImageTk, Image
import tkinter.messagebox
import tkinter

from os import listdir
import os

from os.path import isfile, join

#variables
mypath = "K:/" #start path (should probably put this in an ini or something)
comppath = 'p:/photos/' # start compare path (should probably put this in an ini or something)
PicWidth = 800 #determines the picture size (should probably put this in an ini or something)


#INIT
counter = 0
compfiles = []
compare = True




#functions
#when select button is clicked
def selectfolder():
    DirectoryValue.set(filedialog.askdirectory())
    
def selectfolderCompare():
    CDV.set(filedialog.askdirectory())
    

#load list box from path (run when entry box is changed)
def loadListbox(a, b, c):
    try: #cant get it if its the first time loaded, get it from the default.
        infilepath = DirectoryValue.get()
        if (infilepath[-1:])!='/':
                infilepath = infilepath + '/'
        if (DirectoryValue.get() == ''):
            dle.delete(0, END)
            return
    except:
        infilepath = mypath
    #get files from path above:
    counter=0
    if(os.path.isdir(DirectoryValue.get())): # check if the directory exists as they type.
        dle.delete(0, END)
        onlyfiles = [f for f in listdir(DirectoryValue.get()) if isfile(join(DirectoryValue.get(), f))]
        for value in onlyfiles:
            dle.insert(counter, value)
            if (compare):
                for element in ([x[1]+'/'+x[0] for x in compfiles if x[0] == value]): #file exists in the compare directory
                    if (os.path.getsize(infilepath+value) ==  os.path.getsize(element)): #check if size is the same
                        if (infilepath.lower()+value.lower() != element.lower()): #check that they arent the same file.
                            dle.itemconfig(counter, foreground="red")
            counter == counter + 1        

def selecteditemCompare(a):
#------------------------------------------------------------------------------------
#impose index over picture
#------------------------------------------------------------------------------------    
    if (mle.curselection()):  #something is actually selected. (nothing selected if they click out of the selection box into another selection box
        #print (Image.open(mle.get(mle.curselection())[7:].strip()))
        picturebox.set("Not an image file, select an image file")
        PicPanel.configure(image='', textvariable = picturebox)   
        try:
            img = Image.open(mle.get(mle.curselection())[7:].strip())
        except:
            picturebox.set("cant find: "+mle.get(mle.curselection())[7:].strip())
            PicPanel.configure(image='', textvariable = picturebox) 
        else:
            #img.width * X = 800
            multiplier = img.width / 800
            size = (round(img.width / multiplier), round(img.height / multiplier))
            img = img.resize(size, Image.ANTIALIAS)
            img = ImageTk.PhotoImage(img)
            PicPanel.configure(image = img)
            img.photo_ref = img
    
#when an item is selected in the file selection entry box...
def selecteditem(a):
#------------------------------------------------------------------------------------
#impose index over picture
#------------------------------------------------------------------------------------
    if (dle.curselection()):  #something is actually selected. (nothing selected if they click out of the selection box into another selection box
        if (DirectoryValue.get()[-1:])=='/':
            pad = ''
        else:
            pad = '/'
        try:
            img = Image.open(DirectoryValue.get()+pad+dle.get(dle.curselection()))
        except:
            picturebox.set("Image preview plane, select an image file to view")
            PicPanel.configure(image='', textvariable = picturebox)    
        else:
            #img.width * X = 800
            multiplier = img.width / PicWidth
            size = (round(img.width / multiplier), round(img.height / multiplier))
            img = img.resize(size, Image.ANTIALIAS)
            img = ImageTk.PhotoImage(img)
            PicPanel.configure(image = img)
            img.photo_ref = img    
        source = DirectoryValue.get()+pad+dle.get(dle.curselection())
        sourcefile = dle.get(dle.curselection())
        mle.delete(0, END)
        mle.insert(0, 'Source: '+ source)
        counter = 1 # want to enter into the second box as 0 is already take with the source file.
        #search for found pic in compare folder.
        for element in ([x[1]+'/'+x[0] for x in compfiles if x[0] == sourcefile]):
            if (os.path.getsize(source) ==  os.path.getsize(element)): #check if size is the same
                if (source.lower() != element.lower()): #check that they arent the same file. - this needs some work.
                    mle.insert(counter, 'Found: '+element)
                    counter == counter + 1
        #return dle.get(dle.curselection())

#not used
#def selectfile(self): 
#    filename = tkFileDialog.askopenfilename(filetypes = (("Template files", "*.tplate")
#                                                           ,("HTML files", "*.html;*.htm")
#                                                             ,("All files", "*.*") ))

def ReadCompairPath(a, b, c):    
    try: #cant get it if its the first time loaded, get it from the default.
        infilepath = CDV.get()
    except:
        infilepath = comppath
    compfiles.clear()
    if (infilepath != ''):
        # r=root, d=directories, f = files
        for r, d, f in os.walk(infilepath):
            for file in f:
                #compfiles.append(os.path.join(r, file))
                compfiles.append([file,r])


#read files in photos dir into array
ReadCompairPath("","","")


#main window settings
MW = Tk()
MW.title("FileCompaire")
MW.minsize (800,1000)

#InputDirectory frame (everything on the left) 
IDF = Frame(MW)
IDF.pack(side = LEFT)

#DirectorySelectFrame (Directory select label, entry box and button)
DSF = Frame(IDF)
DSF.pack()

#FileDirectoryText
var = StringVar()
label = Label( DSF, textvariable=var)
var.set("Directory:")
label.pack(side = LEFT)

#SelectDirectoryEntryBox
DirectoryValue = StringVar()
DirectoryValue.set(mypath)
sde = Entry(DSF, textvariable=DirectoryValue)
DirectoryValue.trace('w',loadListbox) #when the direcory entery box changes, reload the grid.
sde.pack(side = LEFT)


#SelectDirectoryButton
sdb = Button(DSF, command=selectfolder, text ="Select Folder")
sdb.pack(side = LEFT)

#directory listbox frame
DSLF = Frame(IDF)
DSLF.pack()

#directory listbox box containing all the files.
dle = Listbox(DSLF, width = 70, height = 50)
loadListbox('','','')
dle.pack()
dle.bind('<<ListboxSelect>>', selecteditem) #run the selecteditem function when the select changes.

#Picture listbox frame
PLF = Frame(MW)
PLF.pack(side = RIGHT)

#Match File frame
#MFF = Frame(MW)
#MFF.pack(side = BOTTOM)

OF = Frame(MW)
OF.pack(side = TOP)

#match listbox entry 
mle = Listbox(PLF, width = 150)
mle.pack(side = BOTTOM)

picturebox = StringVar()
picturebox.set("select an image file to load")
PicPanel = Label(PLF, textvariable=picturebox)
PicPanel.pack(fill = "both", expand = "yes")

mle.bind('<<ListboxSelect>>', selecteditemCompare) #run the selecteditem function when the select changes..bind('<<ListboxSelect>>', selecteditem) #run the selecteditem function when the select changes.


#compare frame
CF = Frame(PLF)
CF.pack(side = BOTTOM)

#Compare Label
lblComp = StringVar()
cl =  Label(CF, textvariable=lblComp)
lblComp.set("Compare Directory:")
cl.pack(side = LEFT)

#Compare Entry box
CDV = StringVar()
CDV.set(comppath)
ce = Entry(CF, textvariable= CDV,width = 50)
CDV.trace('w',ReadCompairPath) #when the direcory entery box changes, reload the grid/array.
ce.pack(side = LEFT)


#compare browse button
cbb = Button(CF, command=selectfolderCompare, text ="Select Folder")
cbb.pack(side = LEFT)



#go!
MW.mainloop()

