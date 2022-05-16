from tkinter import *
#ex1
def readShapes(fileName):
    #creates a new array called shape
    shape = []
    #opens the file and reads the lines
    file = open(fileName)
    Shapes = file.readlines()
    for line in Shapes:
        #creating dictionary
        ShapeDictionary = {}
        #splitting the lines up into attributes
        attributes = line.split()
        bounds = []
        #taking the bounds out of the list of attributes
        for i in range(1,5):
            bounds.append(int(attributes[i]))
        #assigning each attribute a field name in the Shape Dictionary
        ShapeDictionary['bounds'] = bounds
        ShapeDictionary['kind'] = attributes[0]
        ShapeDictionary['fill'] = attributes[5].strip()
        shape.append(ShapeDictionary)                     
    return shape

#ex2
#width = 0 added, otherwise triangle would have outline.
def drawOnCanvas(canvas,shape):
    #list of checks to find what kind of shape and fill it is
    if shape["kind"] == 'rect':
        if shape["fill"] == "True":
            #drawing rectangle
            canvas.create_rectangle(shape['bounds'],fill = 'black', width = 0)
        else:
            canvas.create_rectangle(shape['bounds'],fill = 'white', width = 0)
    elif shape["kind"] == 'tri':
        #assigning the triangle bounds to variables to make easier to have each individual co ordinate
        x0 = shape['bounds'][0]
        y0 = shape['bounds'][1]
        x1 = shape['bounds'][2]
        y1 = shape['bounds'][3]
        if shape["fill"] == "True":
            #drawing triangles or "polygons"
            canvas.create_polygon(x0,y0,x0,y1,x1,y0,fill = 'black', width = 0)
        else:
            canvas.create_polygon(x0,y0,x0,y1,x1,y0,fill = 'white', width = 0)

#ex3
#tried to use bounds[0] = bounds[0] + trans, CONCATENATION ERROR
#[:] added because only 2 shapes were being drawn at a time.
def translate(shape, xtrans):
    bounds = shape['bounds'][:]
    #allows the bounds to be individually manipulated
    bounds[0] += xtrans
    bounds[2] += xtrans
    TranslatedShape = {'bounds':bounds,'kind':shape["kind"],'fill':shape["fill"]}
    return TranslatedShape

#ex4
def reflectV(shape, xVal):
    bounds = shape['bounds'][:]
    bounds[0] = xVal*2 - bounds[0]
    bounds[2] = xVal*2 - bounds[2]
    ReflectedShapeX = {'bounds':bounds,'kind':shape["kind"],'fill':shape["fill"]}
    return ReflectedShapeX

#ex5
def reflectH(shape, yVal):
    bounds = shape['bounds'][:]
    bounds[1] = yVal*2 - bounds[1]
    bounds[3] = yVal*2 - bounds[3]
    ReflectedShapeY = {'bounds':bounds,'kind':shape["kind"],'fill':shape["fill"]}
    return ReflectedShapeY

#ex6
def rotate(shape, centreX, centreY):
    FlippedShape = reflectV(shape,centreX)
    RotatedShape = reflectH(FlippedShape,centreY)
    return RotatedShape

#ex7
def glideReflect(shape,xVal,yVal):
    TranslatedShape = translate(shape,xVal)
    GlideShape = reflectH(TranslatedShape,yVal)
    return GlideShape

#ex8
#sub routines to make "makeFrieze" easier to follow
def UsedReflectV(shapes,xVal):
    NewShapes = []
    for shape in shapes:
        NewShapes.append(reflectV(shape,xVal))
    for shape in NewShapes:
        shapes.append(shape)
    return shapes

def UsedReflectH(shapes,yVal):
    NewShapes = []
    for shape in shapes:
        NewShapes.append(reflectH(shape,yVal))
    for shape in NewShapes:
        shapes.append(shape)
    return shapes

def UsedGlideReflect(shapes,xVal,yVal):
    NewShapes = []
    for shape in shapes:
        NewShapes.append(glideReflect(shape,xVal,yVal))
    for shape in NewShapes:
        shapes.append(shape)
    return shapes

def UsedRotate(shapes, xVal, yVal):
    NewShapes = []
    for shape in shapes:
        NewShapes.append(rotate(shape,xVal,yVal))
    for shape in NewShapes:
        shapes.append(shape)
    return shapes

def Repeat(shapes, repeatLength, nbrRepeats, canvas):
        for shape in shapes:
            for i in range(nbrRepeats):
                 drawOnCanvas(canvas, translate(shape, repeatLength*i))
                 
def makeFrieze(fileName, friezeGroup, repeatLength, height, nbrRepeats):
    FriezeShapes = readShapes(fileName)
    canvas = Canvas(root,width = repeatLength*nbrRepeats, height = height,bg = "white")
    #background made white because white objects were unintentionally visable
    canvas.pack()
    
    if friezeGroup == 1:
        Repeat(FriezeShapes,repeatLength,nbrRepeats,canvas)
        
    elif friezeGroup == 2:
        FriezeShapes = UsedGlideReflect(FriezeShapes,repeatLength//2, height//2)
        Repeat(FriezeShapes,repeatLength,nbrRepeats,canvas)
        
    elif friezeGroup == 3:
        FriezeShapes = UsedReflectV(FriezeShapes, repeatLength//2)
        Repeat(FriezeShapes,repeatLength,nbrRepeats,canvas)
        
    elif friezeGroup == 4:
        FriezeShapes = UsedRotate(FriezeShapes, repeatLength//2, height//2)
        Repeat(FriezeShapes,repeatLength,nbrRepeats,canvas)
        
    elif friezeGroup == 5:
        FriezeShapes = UsedReflectV(FriezeShapes, repeatLength//4)
        FriezeShapes = UsedGlideReflect(FriezeShapes, repeatLength//2, height//2)
        Repeat(FriezeShapes,repeatLength,nbrRepeats,canvas)
        
    elif friezeGroup == 6:
        FriezeShapes = UsedReflectH(FriezeShapes, height//2)
        Repeat(FriezeShapes,repeatLength,nbrRepeats,canvas)
        
    elif friezeGroup == 7:
        FriezeShapes = UsedReflectV(FriezeShapes, repeatLength//2)
        FriezeShapes = UsedReflectH(FriezeShapes, height//2)
        Repeat(FriezeShapes,repeatLength,nbrRepeats,canvas)
                        
root = Tk()                             
    
def Menu():
    print("""
Frieze Group Options
--------------------
1. hop
2. step
3. sidle
4. spinning hop
5. spinning sidle
6. jump
7. spinning jump
""")
       
Menu()
filename = input("Enter the file name:")
friezeGroup = int(input("Enter Frieze Group:"))
repeatLength = int(input("Enter repeat length:"))
height = int(input("Enter Height:"))
nbrRepeats = int(input("Enter number of patterns wanted:"))


makeFrieze(filename,friezeGroup,repeatLength,height,nbrRepeats)
                                    
root.mainloop()
        
