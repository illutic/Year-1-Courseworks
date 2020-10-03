#REQUIRES GRAPHICS LIBRARY FOR PYTHON
from graphics import *

#Tools
STATIC_COLORS = {"r":"red", "g":"green", "b":"blue", "m":"magenta", "o":"orange", "c":"cyan"}
def getInputs():
    
    while True:
        colours=[]
        i = 0 
        
        while True:#Size Input Loop
            size=int(input("Enter Size of Window (only integers are acceptable): "))
            if (size % 2 == 0  or (size > 9 or size < 1)):
                print("Not Valid! Make sure you input one of the odd numbers(1,3,5,7,9)")
            else:
                break
                
        print("Colour List [r = red , g = green , b = blue , m = magenta , o = orange , c = cyan]")
        while i < 3 : # Colour Input Loop
            col=input('''Enter Colour #'''+ str(i+1) + ':')
            if col not in STATIC_COLORS:
                print("Not Valid, Try again.")
            else:
                colours.append(col)
                i+=1
        
        break
    return size,colours

def getCenter(pointList):

    #Gets the middle point of two points
    xCoord0= pointList[0].getX()
    xCoord1= pointList[1].getX()
    yCoord0= pointList[0].getY()
    yCoord1= pointList[1].getY()
    
    middleX = (xCoord0 + xCoord1)*0.5
    middleY = (yCoord0 + yCoord1)*0.5
    center = Point(middleX, middleY)

    return center

def checkColour(point,colours, size):
    # Checks the colour to be based on the shape of 2

    x = point.getX()
    y = point.getY()
    

    if (y == 0 or y == size-1) or (x == 0 or x == size-1):
        if (x % 2 == 0 and y % 2 == 0):
            colour = STATIC_COLORS[colours[0]]
        else:
            colour = STATIC_COLORS[colours[1]]
    else:
        colour = STATIC_COLORS[colours[2]]
    return colour

def instructions(win, size):
    txt = Text(Point(250,200), '''
    
    Instructions
    \nPress [S] to enter the Selection Mode
    \nPress [F] to change the Selected Objects to "Final Design"
    \nPress [P] to change the Selected Objects to "Penultimate Design"
    \nPress [D] to deselect all Selected Objects
    \nPress [R,G,B,M,O,C] to change the Selected Objects' colour to \n[RED,GREEN,BLUE,MAGENTA,ORANGE,CYAN] respectively
    \nTo Exit the Selection Mode click the top left black box
    \nNote:When a process is initiated (ex.changing the design)\n the program automatically deselects everything at the end of it.
    \nLast Digits: 287 ''')
    
    txt.draw(win)









#Challenge
def selectionMode(key, mode):
    if key == "s":
        return not mode
        
def startUndraw(shapeData):
    #Universal undraw()
    if isinstance(shapeData, tuple):
        startUndraw(shapeData[0])
        startUndraw(shapeData[1])
    elif isinstance(shapeData, list):
        for i in shapeData:
            startUndraw(i)
    elif isinstance(shapeData, dict):
        startUndraw(shapeData["shape"])
    else:
        shapeData.undraw()

def findObject(point, objects, obj_id = 0):
    for obj_id in range(len(objects)): 
        recOrigin = objects[obj_id]["vectorPoints"][0]
        recDestination = objects[obj_id]["vectorPoints"][1]

        #If the point is within the boundaries of an object's rectangle.
        if (point.getX()> recOrigin.getX() and point.getY()> recOrigin.getY()) and \
        (point.getX()< recDestination.getX() and point.getY()< recDestination.getY()):
            return obj_id

def changeShape(win, loc_object, shapeID):
    #Find information from object
    pointVector = loc_object["vectorPoints"]
    colour = loc_object["colour"]

    #Change Object's attributes
    if shapeID == "f":
        newShapeData = finalShape(win, "", pointVector, colour)

        loc_object["ID"] = "f" # Apply ID change to object

    elif shapeID == "p":
        newShapeData = penLogic(win,colour,pointVector)

        loc_object["ID"] = "p" # Apply ID change to object

    loc_object["shape"] = newShapeData #Pass new Shape data
    return loc_object
    
def changeColour(win, loc_object, cr):
    pointVector = loc_object["vectorPoints"]

    if loc_object["ID"] == "f":
        newShapeData = finalShape(win, "", pointVector, cr)
    elif loc_object["ID"] == "p":
        newShapeData = penLogic(win,colour, pointVector)
    loc_object["shape"] = newShapeData
    loc_object["colour"] = cr
    return loc_object
    
def object(points, shapeData, colour, shape_id, selected = False):
    local_object = {"vectorPoints":points, "shape":shapeData, "colour":colour, "selected":selected, "ID":shape_id}
    return local_object

def blackBox(win, size, point = None):
    rectanglePoints = [Point(0,size-0.2),Point(0.2,size)]
    rec = drawRectangle(win,"black", rectanglePoints)
    return rec

def blackBoxLogic(win, point, size):
    rectanglePoints = [Point(0,size-0.2),Point(0.2,size)]
    if point != None:
        rectangleOrigin = rectanglePoints[0]
        rectangleDestination = rectanglePoints[1]

        if (point.getX()> rectangleOrigin.getX() and point.getY()> rectangleOrigin.getY()) and \
        (point.getX()< rectangleDestination.getX() and point.getY()< rectangleDestination.getY()):
            return True
        else:
            return False












#Shapes
def drawRectangle(win, clr, rectanglePoints, outline="", thicc=1, draw=True):
    rec= Rectangle(rectanglePoints[0],rectanglePoints[1])
    rec.setFill(clr)
    rec.setOutline(outline)
    rec.setWidth(thicc)
    if draw:
        rec.draw(win)
    return rec

def penultimateShape(win, clr , rectanglePoints,step, reverse = False):

    
    #Coordinate Initialization
    xCoord0= rectanglePoints[0].getX()
    xCoord1= rectanglePoints[1].getX()
    yCoord0= rectanglePoints[0].getY()
    yCoord1= rectanglePoints[1].getY()
    center=getCenter(rectanglePoints)
    
    #circle
    circ=Circle(center, step/2)
    circ.setFill(clr)
    circ.setOutline("")
    
    #triangle
    tr1 = Point(xCoord1, yCoord0)
    tr2 = Point(xCoord1, yCoord1)
    
    if reverse:
        tr1 = Point(xCoord1-step, yCoord0)
        tr2 = Point(xCoord1-step, yCoord1)

    triangle = Polygon([tr1,center,tr2])
    triangle.setFill("whitesmoke")
    triangle.setOutline("")
    
    #Drawing
    circ.draw(win)
    triangle.draw(win)

    return circ, triangle

def penLogic(win, colour, rectanglePoints):
    step = 0.2
    x0 = rectanglePoints[0].getX()
    y0 = rectanglePoints[0].getY()
    shape=[]
    y = y0
    for i in range(5):
        x = x0
        for j in range(5):
            
            #Start at X = [0,1,2,...]
            #when that function is called at [0,1,2,...]
            #every 0.2 points a new shape is drawn
            #then all those shapes are passed on a list
            rectangleOrigin = Point(x,y)
            rectangleDestination = Point(x+step,y+step)
            rectanglePoints = [rectangleOrigin,rectangleDestination]
            
            x+=step
            
            if (i % 2 == 0 and j % 2 == 0): 
                shape.append(penultimateShape(win, colour, rectanglePoints, step))
                
            elif (i % 2 != 0 and j % 2 != 0):
                shape.append(penultimateShape(win, colour, rectanglePoints, step , True))
                
            else:
                shape.append(drawRectangle(win, colour, rectanglePoints))
        y += step
        
        
    return shape
        
def fShape(win, clr, rectanglePoints,txtCol):
    center = getCenter(rectanglePoints)
    rec = drawRectangle(win,clr,rectanglePoints,txtCol)
    txt = Text(center, "Hi!")
    txt.setTextColor(txtCol)
    txt.draw(win)
    return rec, txt
    
def finalShape(win, clr, rectanglePoints,txtCol):
    
    #same with pen shape
    shape=[]
    step = 0.2
    x0 = rectanglePoints[0].getX()
    y0 = rectanglePoints[0].getY()
    y1 = y0
    for y in range(5):
        x1 = x0
        for x in range(5):
            rectangleOrigin = Point(x1,y1)
            rectangleDestination = Point(x1+step,y1+step)
            rectanglePoints = [rectangleOrigin,rectangleDestination]
            x1+=step
            shape.append(fShape(win, clr, rectanglePoints,txtCol))
        y1+=step
    return shape












#Main Function
def main(size, colours):
    #Initialization
    objectList = []
    finalX=0
    
    instWin= GraphWin("Instructions", 500,500)
    instructions(instWin, size)
    win = GraphWin("Too many Patches!",size*100,size*100)
    win.setCoords(0,0,size,size)
    step = 0.2
    
    for y in range(size):
        for x in range(size):
            if size-x-1 != finalX:
                    #draw inner shapes
                    rectangleOrigin = Point(x,y)
                    rectangleDestination = Point(x+1,y+1)
                    rectanglePoints = [rectangleOrigin,rectangleDestination] 
    
                    # Colouring Logic
                    colour = checkColour(rectangleOrigin,colours,size)
    
                    #Penultimate Shape Logic (Checks the boundaries of the shape.)
                    activeShape = penLogic(win,colour, rectanglePoints)
                    objectList.append(object(rectanglePoints, activeShape, colour, "p"))
                        
        #Draw Final Shape
        #--Final Shape Rectangle
        finalOrigin = Point(finalX,size-y-1)
        finalDestination = Point(finalX+1,size-y)
        finalPoints=[finalOrigin, finalDestination]
        #--

        finalX+=1

        colour = checkColour(finalOrigin,colours,size)
        activeShape = finalShape(win,"",finalPoints,colour)
        objectList.append(object(finalPoints, activeShape, colour, "f"))

    return win, objectList



#Phase 2 Initialization

size,colours = getInputs()        
mainWin=main(size, colours)
win = mainWin[0]
objects = mainWin[1]

drawedIDS=[]
deselection_trigger=0




#Main Loop
while True:
    click = None
    selec_key = win.getKey()
    selec_mode = False
    blackBoxDrawed = False
    desRect = None 
    selection_reset = False
     
#Selection Mode 
    while selectionMode(selec_key,selec_mode): 
        click = win.checkMouse()
        key = win.checkKey()

        if click != None:
            #Find which object is clicked
            clicked_obj = findObject(click, objects)
            
            
            #Draw Border
            if clicked_obj not in drawedIDS and clicked_obj != None:
                #Only one instance of a selection drawing is allowed
                border = drawRectangle(win,"",objects[clicked_obj]["vectorPoints"],"black",3)
                objects[clicked_obj]["selected"] = border
                drawedIDS.append(clicked_obj)
            elif clicked_obj in drawedIDS:
                startUndraw(objects[clicked_obj]["selected"]) 
                objects[clicked_obj]["selected"] = False
                drawedIDS.remove(clicked_obj)
            
        
        if blackBoxDrawed == False:
            desRect = blackBox(win,size)
            blackBoxDrawed = True

        if blackBoxLogic(win, click, size):
            #If Deselection Rectangle is clicked Deselect everything and break
            deselection_trigger=1
            desRect.undraw()
            selec_key = None
            selec_mode = True

        if key == "d":
            #Deselect
            deselection_trigger=1
    
        if key == "p":
            for obj in objects:
                if obj["selected"] != False:
                    #Undrawing Previous Data
                    startUndraw(obj["shape"])
                    desRect.undraw()
                    #Drawing
                    changeShape(win,obj, "p")
                    desRect = blackBox(win,size)
                    #Deselecting
                    selection_reset = True
  
        if key == "f":
            for obj in objects:
                if obj["selected"] != False:
                    #Undrawing Previous Data
                    startUndraw(obj["shape"])
                    desRect.undraw()
                    #Drawing
                    changeShape(win,obj,"f")
                    desRect = blackBox(win,size)
                    #Deselecting
                    selection_reset = True

        if key in STATIC_COLORS:
            for obj in objects:
                if obj["selected"] != False:
                    colour = STATIC_COLORS[key]
                    #Undrawing Previous Data
                    startUndraw(obj["shape"])
                    desRect.undraw()
                    #Drawing
                    desRect = blackBox(win,size)
                    changeColour(win,obj,colour)
                    
                    #Deselecting
                    selection_reset = True

        

        if deselection_trigger == 1:
            #Resetting
            desRect.undraw()
            desRect = blackBox(win,size)
            blackBoxDrawed = True
            
            drawedIDS=[]
            
            for obj in objects:
                if obj["selected"]!= False:
                    obj["selected"].undraw()
                obj["selected"]= False
                
            deselection_trigger = 0

        if selection_reset:
            for obj in objects:
                if obj["selected"] != False:
                    obj["selected"].undraw()
                    obj["selected"] = drawRectangle(win,"",obj["vectorPoints"],"black",3)
            selection_reset = False

        
                
    if desRect != None:
        desRect.undraw()
