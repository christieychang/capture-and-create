from Tkinter import *
from tkColorChooser import askcolor
import cv2
import numpy as np
from tkFileDialog import askopenfilename, asksaveasfilename




#Works Cited
#Buttons: 15-112 Course Website Tkinter Buttons
#http://www.java2s.com/Code/Python/GUI-Tk/Buttonforegroundcolor.htm
#http://effbot.org/tkinterbook/tkinter-file-dialogs.htm
#http://docs.opencv.org/3.0-beta/doc/py_tutorials/py_tutorials.html
#http://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/
            #py_setup/py_table_of_contents_setup/py_table_of_contents_setup.html
#https://mail.python.org/pipermail/tutor/2008-July/063119.html
#http://www.java2s.com/Tutorial/Python/0360__Tkinker/Canvaspaintprogram.htm
#http://www.tutorialspoint.com/python/tk_pack.htm
#http://scikit-image.org/docs/dev/user_guide/numpy_images.html
#http://docs.opencv.org/3.1.0/d7/d4d/tutorial_py_thresholding.html#gsc.tab=0
#http://docs.opencv.org/2.4/modules/imgproc/doc/
            #miscellaneous_transformations.html
#http://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/
                #py_imgproc/py_contours/py_contours_begin/py_contours_begin.html
#http://effbot.org/tkinterbook/photoimage.htm
#https://www.youtube.com/watch?v=6jBlqICn4_I
#sentdex from Youtube (OpenCV)




def init(root, canvas):
    buttonFrame = Frame(root)
    canvas.data["image"] = None
    canvas.height = 700
    canvas.width = 1100
    canvas.data["x"] = canvas.width/2
    canvas.data["y"] = canvas.height/2
    canvas.data["pencolor"] = "black"
    canvas.data["penwidth"] = 5
    canvas.data["drawMode"] = None      #draw, erase
    canvas.data["dragMode"] = None      #paint, shape
    canvas.data["shape"] = None         #c1, c2, r1, r2, line
    canvas.data["shapecolor"] = "black"
    canvas.data["imageMode"] = "move"   #move, placed
    canvas.trackedCenters = []
    canvas.current = None
    canvas.array = np.zeros((canvas.height,canvas.width))
    canvas.permanArray = np.zeros((canvas.height,canvas.width))
    (canvas.moveX, canvas.moveY) = (0,0)

    while True:
        file = "background.jpg"
        img = cv2.imread(file, 1)
        cv2.imshow('C&C: Capture and Create', img)
        k = cv2.waitKey(1) & 0xFF
        if k==ord("c"):
            cv2.destroyAllWindows()
            break

    def captureB():
        captureButton(canvas)
    capture=Button(buttonFrame, text="capture", fg="#00ffff", command=captureB)
    capture.config(font=('helvetica', 15))
    capture.grid(row=0,column=0)


    def saveB():
        saveButton(canvas)
    save = Button(buttonFrame, text="save", command = saveB)
    save.config(font=('helvetica', 15))
    save.grid(row=0, column = 2)
    
    def placeB():
        placeButton(canvas)
    place = Button(buttonFrame, text="place", command = placeB)
    place.config(font=('helvetica', 15))
    place.grid(row=0, column = 3)
    
    def mouseDrawB():
        mouseDrawButton(canvas)
    draw = Button(buttonFrame, text="draw", command=mouseDrawB)
    draw.config(font=('helvetica', 15))
    draw.grid(row=0,column=4)

    def penBigB():
        penBigButton(canvas)
    penBWidth = Button(buttonFrame, text="pen +", command=penBigB)
    penBWidth.config(font=('helvetica', 15))
    penBWidth.grid(row=0, column=5)
    
    def penSmallB():
        penSmallButton(canvas)
    penSWidth = Button(buttonFrame, text="pen -", command=penSmallB)
    penSWidth.config(font=('helvetica', 15))
    penSWidth.grid(row=0, column=6)
    
    def eraseB():
        eraseButton(canvas)
    erase = Button(buttonFrame, text="erase", command=eraseB)
    erase.config(font=('helvetica', 15))
    erase.grid(row=0, column=7)
    
    def shapesB():
        createShape(canvas)
    shapes = Button(buttonFrame, text="shapes", command=shapesB)
    shapes.config(font=('helvetica', 15))
    shapes.grid(row=0, column=8)

    def clearB():
        clearButton(canvas)
    clear = Button(buttonFrame, text="clear", command=clearB)
    clear.config(font=('helvetica', 15))
    clear.grid(row=0, column=9)
    
    buttonFrame.pack(side=TOP)
    canvas.pack() # moved canvas packing to here (after buttonFrame pack)



######## Event-based functions ########


def mousePressed(canvas, event):
    if canvas.current != None:
        if canvas.data["imageMode"] == "move":
            canvas.delete(ALL)
            buttonBorder = 25
            if (event.y > buttonBorder):
                canvas.moveX,canvas.moveY = event.x, event.y
                (x,y) = (canvas.moveX, canvas.moveY)
                canvas.array = np.zeros((canvas.height,canvas.width))
                try:
                    for row in range(canvas.current.rows):
                        for col in range(canvas.current.cols):
                            if canvas.current.array[row][col] == 1:
                                canvas.array[y+row][x+col] = 1
                except:
                    newRows = canvas.current.rows
                    newCols = canvas.current.cols
                    if (y+canvas.current.rows > canvas.height):
                        newRows = canvas.height - y
                    if (x+canvas.current.cols > canvas.width):
                        newCols = canvas.width - x
                    for row in range(newRows):
                        for col in range(newCols):
                            if canvas.current.array[row][col] == 1:
                                canvas.array[y+row][x+col] = 1
            redrawAll(canvas)
            
        if canvas.data["dragMode"] == "shape":
            (canvas.data["init x"], canvas.data["init y"]) = (event.x, event.y)
            
            
    
def keyPressed(canvas, event):
    pass

    
def mouseDrag(canvas, event):
    if canvas.data["dragMode"] == "paint":
        paint(canvas, event)


def mouseRelease(canvas, event):
    if canvas.data["dragMode"] == "shape":
        (canvas.data["final x"], canvas.data["final y"]) = (event.x, event.y)
        drawShape(canvas, event)


    
def paint( canvas, event ):
    if canvas.data["drawMode"] == "draw":
        radius = canvas.data["penwidth"]
        x1, y1 = ( event.x - radius ), ( event.y - radius )
        x2, y2 = ( event.x + radius ), ( event.y + radius )
        canvas.create_oval( x1, y1, x2, y2, fill = canvas.data["pencolor"], 
                                            outline= canvas.data["pencolor"])
        
    if canvas.data["drawMode"] == "erase":
        radius = 5
        x1, y1 = ( event.x - radius ), ( event.y - radius )
        x2, y2 = ( event.x + radius ), ( event.y + radius )
        canvas.create_oval( x1, y1, x2, y2, fill = "white", outline = "white")



def drawShape(canvas, event):
    (x1,y1,x2,y2) = (canvas.data["init x"], canvas.data["init y"],
                                canvas.data["final x"], canvas.data["final y"])
    color = canvas.data["shapecolor"]
    if canvas.data["shape"] == "c1":
        diam = (y2-y1)
        canvas.create_oval(x1,y1,x1+diam,y2,fill=None, outline=color, width=5)
    if canvas.data["shape"] == "c2":
        diam = (y2-y1)
        canvas.create_oval(x1,y1,x1+diam,y2,fill=color, outline=color, width=5)
    if canvas.data["shape"] == "r1":
        canvas.create_rectangle(x1,y1,x2,y2,fill=None, outline = color, width=5)
    if canvas.data["shape"] == "r2":
        canvas.create_rectangle(x1,y1,x2,y2,fill=color, outline = color)
    if canvas.data["shape"] == "line":
        canvas.create_line(x1,y1,x2,y2,fill=color,width=5)
        


def redrawAll(canvas):

    if canvas.data["imageMode"] == "move":
        canvas.delete(ALL)
        for row in range(len(canvas.permanArray)):
            for col in range(len(canvas.permanArray[0])):
                if canvas.permanArray[row][col] == 1:
                    canvas.create_rectangle(col,row,col,row,fill="black")
        for row in range(len(canvas.array)):
            for col in range(len(canvas.array[0])):
                if canvas.array[row][col] == 1:
                    canvas.create_rectangle(col,row,col,row,fill="black")
    if canvas.data["imageMode"] == "placed":
        for row in range(len(canvas.permanArray)):
            for col in range(len(canvas.permanArray[0])):
                if canvas.permanArray[row][col] == 1:
                    canvas.create_rectangle(col,row,col,row,fill="black")
    canvas.update()
    
    
    
####### Drawing Class ########

class Drawing(object):
    def __init__(self, canvas, array, rows, cols, filename):
        self.array = array
        self.rows = rows
        self.cols = cols
        self.file = filename
        
        
        
        
        
############# Buttons ##############


def captureButton(canvas):
    webcam(canvas)
    canvas.data["imageMode"] = "move"
    canvas.array = np.zeros((canvas.height,canvas.width))
    for row in range(canvas.current.rows):
            for col in range(canvas.current.cols):
                if canvas.current.array[row][col] == 1:
                    canvas.array[row][col] = 1
    redrawAll(canvas)
    canvas.create_text(15,canvas.height,
        text='Instructions: Click where you would like to move the drawing. "Place" drawing when finished', anchor=SW)


      
def placeButton(canvas):
    canvas.data["imageMode"] = "placed"
    for row in range(len(canvas.array)):
        for col in range(len(canvas.array[0])):
            if canvas.array[row][col] == 1:
                canvas.permanArray[row][col] = 1
    redrawAll(canvas)
        
def saveButton(canvas):
    Tk().withdraw()
    filename = asksaveasfilename(defaultextension = ".ps", title="Save As...")
    canvas.postscript(file=filename,colormode='color')
      

def penBigButton(canvas):
    if canvas.data["imageMode"] == "move":
        canvas.create_text(15, canvas.height, text='Instructions: Capture and Place drawing first!', anchor = SW)
    else:
        if canvas.data["penwidth"] < 30:
            canvas.data["penwidth"] += 2
            

def penSmallButton(canvas):
    if canvas.data["imageMode"] == "move":
        canvas.create_text(15, canvas.height, text='Instructions: Capture and Place drawing first!', anchor = SW)
    else:
        if canvas.data["penwidth"] > 0:
            canvas.data["penwidth"] -= 2

    
def mouseDrawButton(canvas):
    if canvas.data["imageMode"] == "move":
        canvas.create_text(15, canvas.height, text='Instructions: Capture and Place drawing first!', anchor = SW)
    else:
        canvas.data["drawMode"] = "draw"
        (triple, hexstr) = askcolor()
        chosenColor = '#%02x%02x%02x' % (triple[0], triple[1], triple[2])
        canvas.data["pencolor"] = chosenColor
        canvas.data["dragMode"] = "paint"
        canvas.data["drawMode"] = "draw"

    

def eraseButton(canvas):
    if canvas.data["imageMode"] == "move":
        canvas.create_text(15, canvas.height, text='Instructions: Capture and Place drawing first!', anchor = SW)
    else:
        canvas.data["drawMode"] = "erase"
        

def clearButton(canvas):
    top = Toplevel()
    top.title("C&C: Clear")
    top.geometry('500x200')

    msg = Message(top, text="Are you sure you would like to clear the canvas?",
                                                                anchor=CENTER)
    msg.pack()

    def confirmClearB():
        confirmClear(top, canvas)
    button1 = Button(top, text="Yes", command=confirmClearB)
    button1.pack()
    button2 = Button(top, text="No", command=top.destroy)
    button2.pack()


def confirmClear(top, canvas):
    canvas.permanArray = np.zeros((canvas.height,canvas.width))
    canvas.array = np.zeros((canvas.height,canvas.width))
    
    top.destroy()
    canvas.data["imageMode"] = "move"
    redrawAll(canvas)
    


def createShape(canvas):
    if canvas.data["imageMode"] == "move":
        canvas.create_text(15, canvas.height, text='Instructions: Capture and Place drawing first!', anchor = SW)
    else:
        top = Toplevel()
        top.title("C&C: Shapes")
        top.geometry('600x250')
        width = 600
        height = 200
        canvas2 = Canvas(top, width=width, height=height)
        canvas2.pack()
        top.bind("<Button-1>", lambda event: shapePressed(canvas, event, top))
        top.canvas2 = canvas2.canvas2 = canvas2
        canvas.data["dragMode"] = "shape"
        
        gridWidth = width/5 #120
        rad = gridWidth/2-20    
        
        canvas2.create_text(width/2,20,text="Choose a shape to draw! Click 'Done' when you are finished",
                                                fill="magenta", font="helvetica 20")
        canvas2.create_text(60,60,text="circle",fill="blue", font="helvetica 15")
        canvas2.create_text(60+gridWidth,60,text="filled circle",
                                                fill="blue", font="helvetica 15")
        canvas2.create_text(60+gridWidth*2,60,text="rectangle",
                                                fill="blue", font="helvetica 15")
        canvas2.create_text(60+gridWidth*3,60,text="filled rectangle",
                                                fill="blue", font="helvetica 15")
        canvas2.create_text(60+gridWidth*4,60,text="line",
                                                fill="blue", font="helvetica 15")
        
        #filled circle, outline circle, fill rectangle, outline rectangle, line
        canvas2.create_rectangle(3,76,gridWidth, 76+gridWidth,fill="black",
                                                                outline="white")
        (cx,cy) = (117/2,76+60)
        canvas2.create_oval(cx-rad+4,cy-rad,cx+rad+4,cy+rad,fill=None,
                                                outline="light blue", width=5)
                                                    
        
        
        
        canvas2.create_rectangle(gridWidth,76,2*gridWidth,76+gridWidth,
                                                fill="black",outline="white")
        (cx2,cy2) = (180,76+60)
        
        canvas2.create_oval(cx2-rad+4,cy2-rad,cx2+rad+4,cy2+rad,
                            fill="light blue", outline="light blue", width=5)
        
        
        
        
        canvas2.create_rectangle(gridWidth*2,76,3*gridWidth,76+gridWidth,
                                                fill="black",outline="white")
        bdr = 20 #border
        canvas2.create_rectangle(gridWidth*2+bdr,76+bdr,3*gridWidth-bdr,
                    76+gridWidth-bdr,fill=None,outline="light blue", width=5)
        
        
        
        
        canvas2.create_rectangle(3*gridWidth,76,4*gridWidth,76+gridWidth,
                                                fill="black",outline="white")
        canvas2.create_rectangle(3*gridWidth+bdr,76+bdr,4*gridWidth-bdr,
            76+gridWidth-bdr,fill="light blue",outline="light blue", width=5)
        
        
        
        
        canvas2.create_rectangle(4*gridWidth-5,76,5*gridWidth,
                                    76+gridWidth,fill="black",outline="white")
        canvas2.create_line(4*gridWidth+20, 76+20, 5*gridWidth-20,
                                    76+gridWidth-20, fill="lightblue", width=5)
            
        
        buttonFrame = Frame(top)
        def shapeColor():
            chooseShapeColor(top, canvas)
        color = Button(buttonFrame, text="choose color", command=shapeColor)
        color.grid(row=0,column=0)
        
        exit = Button(buttonFrame, text="Done", command=top.destroy)
        exit.grid(row=0,column=1)
        buttonFrame.pack(side=BOTTOM)
        canvas2.pack()
        canvas.data["dragMode"] = "shape"
    
                            
def shapePressed(canvas, event, top):
    gridWidth= 120
    (x,y) = (event.x, event.y)
    if x>3 and y>76 and x<gridWidth and y<76+gridWidth:
        canvas.data["shape"] = "c1"
    if x>gridWidth and y>76 and x<2*gridWidth and y<76+gridWidth:
        canvas.data["shape"] = "c2"
    if x>gridWidth*2 and y>76 and x<3*gridWidth and y<76+gridWidth:
        canvas.data["shape"] = "r1"
    if x>gridWidth*3 and y>76 and x<4*gridWidth and y<76+gridWidth:
        canvas.data["shape"] = "r2"
    if x>gridWidth*4 and y>76 and x<5*gridWidth and y<76+gridWidth:
        canvas.data["shape"] = "line"
    
    
def chooseShapeColor(top, canvas):
    (triple, hexstr) = askcolor()
    chosenColor = '#%02x%02x%02x' % (triple[0], triple[1], triple[2])
    canvas.data["shapecolor"] = chosenColor
    

    
############ Image Edit ###########


def transparent(img):
    image = img.convert("RGBA")
    pixdata = image.load()

    for y in range(image.size[1]):
        for x in range(image.size[0]):
            if pixdata[x, y] == (255, 255, 255, 255):
                pixdata[x, y] = (255, 255, 255, 0)
    return image



def getArray(filename, canvas):
    alpha = cv2.imread(filename, cv2.IMREAD_UNCHANGED)
    (rows, cols) = alpha.shape
    array = np.zeros((rows,cols))
    for row in range(rows):
        for col in range(cols):
            if alpha[row, col] == 0:
                array[row][col] = 1
    return (array, rows, cols)
    



def crop(image):   
    height, width = image.shape
    rectCoords = dict()
    for coords in canvas.trackedCenters:
        (x,y) = coords
        distance = 40
        if ((x < width/3) and (y < height/2)):
            rectCoords[0] = (x+distance,y+distance)
        elif ((x > (2*width)/3) and (y > height/2)):
            rectCoords[1] = (x-distance,y-distance)
    cv2.rectangle(image, rectCoords[0], rectCoords[1], (0,255,0), 3)
    (x0,y0) = rectCoords[0]
    (x1,y1) = rectCoords[1]
    border = 3
    cropped = image[y0+border:y1-border, x0+border:x1-border]
    return cropped


def threshold_otsu(image):
    value = (5, 5)
    blur = cv2.GaussianBlur(image, value, 0)
    ret, thresholded = cv2.threshold(blur, 0, 255, 
                                    cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    return ret, thresholded 

    
def convertImage(image):
    image = cv2.medianBlur(image,5)
    greyImage = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    croppedImage = crop(greyImage)
    ret, thresholded = threshold_otsu(croppedImage)
    return thresholded




def webcam(canvas):
    window_name = "Capture"
    cam_index = 0 # Default camera is at index 0.
    cv2.namedWindow(window_name, cv2.CV_WINDOW_AUTOSIZE)
    cap = cv2.VideoCapture(cam_index) # Video capture object
    cap.open(cam_index) # Enable the camera
    canvas.trackedCenters = []
    while True:
        redLower = np.array([0,100,100]) #RGB out of 255
        redUpper = np.array([20,255,255])
        ret, frame = cap.read()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, redLower, redUpper)
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0]
        for c in cnts:
            M = cv2.moments(c)
            if M['m00'] != 0 and M['m00'] != 0:
                cx = int(M['m10']/M['m00'])
                cy = int(M['m01']/M['m00'])
                cv2.circle(frame, (cx,cy), 10, (0,255,0),-1)
                canvas.trackedCenters.append((cx,cy))
	cv2.imshow(window_name, frame)
        k = cv2.waitKey(1) & 0xFF
        
        if k == ord("c"):
            camera_capture= frame
            cv2.destroyAllWindows()
            cap.release()
            
            while True:
                editedImage = convertImage(camera_capture)
                cv2.imshow("Keep (Press 'k') or Delete (Press 'd')?", 
                                                                    editedImage)
                k = cv2.waitKey(1) & 0xFF
                if k==ord("k"):
                    file = "capture.png"
                    cv2.imwrite(file, editedImage)
                    (array, rows, cols) = getArray(file, canvas)
                    canvas.current = Drawing(canvas, array, rows, cols, file)
                    cv2.destroyAllWindows()
                    break
                if k==ord("d"):
                    canvas.current.array= np.zeros((canvas.height,canvas.width))
                    canvas.array = np.zeros((canvas.height,canvas.width))
                    cv2.destroyAllWindows()
                    break
            break
        if k == 27:
            canvas.data["image"] = None
            cv2.destroyAllWindows()
            cap.release()
            break


########### copy-paste below here ###########

def run():
    # create the root and the canvas
    root = Tk()
    root.title("C&C: Capture and Create")
    global canvas # make canvas global for button1Pressed function
    canvas = Canvas(root, width=1100, height=700)
    # Store canvas in root and in canvas itself for callbacks
    root.canvas = canvas.canvas = canvas
    # Set up canvas data and call init
    canvas.data = { }
    init(root, canvas)
    # set up events
    root.bind("<Button-1>", lambda event: mousePressed(canvas, event))
    root.bind("<Key>", lambda event: keyPressed(canvas, event))
    root.bind("<B1-Motion>", lambda event: mouseDrag( canvas, event ))
    root.bind("<ButtonRelease-1>", lambda event: mouseRelease(canvas, event))
    #timerFired(canvas)
    # and launch the app
    root.mainloop() 

run()
