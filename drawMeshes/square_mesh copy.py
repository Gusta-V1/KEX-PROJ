#%%
import numpy as np

from dataclasses import dataclass
@dataclass
class Point:
   x: float
   y: float

def drawPoints(Nmode):
    ypoints = []
    hspace = 10
    vspace = 10

    #Left side xpoints
    xbs = []
    for i in range(1,Nmode):
        xbs.append(i*hspace)

    for i in range(Nmode):
        ypoints.append(i*vspace)

    rightx = Nmode * hspace

    rightPoints = []
    leftPoints = []
    botPoints = []
    topPoints = []

    for i in range(Nmode):
        leftPoints.append(Point(0,ypoints[i]))
        rightPoints.append(Point(rightx,ypoints[i]))

    for i in range(len(xbs)):
        botPoints.append(Point(xbs[i],0))
        topPoints.append(Point(xbs[i],max(ypoints)))

    return leftPoints, botPoints, rightPoints, topPoints[::-1], Nmode


#%%


# %%
def drawSquareMesh(Nmode):
    import turtle
    print('Nmode = ', Nmode)

    if(Nmode % 2 == 0):
        startValue = 1
        leftPoints, botPoints, rightPoints, topPoints, _ = drawPoints(Nmode)
    else:
        startValue = 0
        leftPoints, botPoints, rightPoints, topPoints, _ = drawPoints(Nmode)


    all_points = leftPoints + botPoints + rightPoints + topPoints
    xs = [p.x for p in all_points]
    ys = [p.y for p in all_points]
    margin = 20

    screen = turtle.Screen()
    width = screen._root.winfo_screenwidth()
    height = screen._root.winfo_screenheight()

    print('Drawing resolution: ',height, 'x',width)


    turtle.setup(height, height)
    turtle.setworldcoordinates(
        min(xs) - margin,
        min(ys) - margin,
        max(xs) + margin,
        max(ys) + margin,
    )

    if(Nmode % 2 == 0):
        startValue = 1
    else:
        startValue = 0

    print('startValue = ',startValue)

    # ── canvas / style ──────────────────────────────────────────────────────────
    #WIDTH, HEIGHT = 1400, 650
    #turtle.setup(WIDTH, HEIGHT)
    turtle.bgcolor("white")
    turtle.title("Triangular Mesh")
    #turtle.tracer(0, 0)          # draw instantly

    t = turtle.Turtle()
    t.hideturtle()
    t.speed(0)
    t.pensize(8)
    t.color("black")
    t.penup()



    leftBack = leftPoints[::-1]
    topBack = topPoints[::-1]
    for i in range(startValue,len(topPoints),2):
        t.goto(leftBack[i+1].x,leftBack[i+1].y)
        t.pendown()
        t.goto(topBack[i].x,topBack[i].y)
        t.penup()

    rightBack = rightPoints[::-1]
    for i in range(startValue,len(topPoints),2):
        t.goto(rightBack[i+1].x,rightBack[i+1].y)
        t.pendown()
        t.goto(topPoints[i].x,topPoints[i].y)
        t.penup()

    for i in range(2,len(leftPoints),2): #HÄÄÄÄE,2): DÅLIG
        t.goto(leftPoints[i].x,leftPoints[i].y)
        t.pendown()
        t.goto(botPoints[i-1].x,botPoints[i-1].y)
        t.penup()

    botPointsBack = botPoints[::-1]
    for i in range(2,len(rightPoints),2): #DÅÅLIG
        t.goto(rightPoints[i].x,rightPoints[i].y)
        t.pendown()
        t.goto(botPointsBack[i-1].x,botPointsBack[i-1].y)
        t.penup()

    if(startValue == 0):
        for i in range(0,len(topPoints)-1,2):
            t.goto(topPoints[i].x,topPoints[i].y)
            t.pendown()
            t.goto(topPoints[i+1].x,topPoints[i+1].y)
            t.penup()

        for i in range(1,len(botPoints)-1,2):
            t.goto(botPoints[i].x,botPoints[i].y)
            t.pendown()
            t.goto(botPoints[i+1].x,botPoints[i+1].y)
            t.penup()
    else: 

        middleX = abs(botPoints[0].x - leftPoints[0].x)/2

        t.goto(leftPoints[0].x+middleX,leftPoints[0].y)
        t.pendown()
        t.goto(rightPoints[-1].x-middleX,rightPoints[-1].y)
        t.penup()

        t.goto(leftPoints[-1].x+middleX,leftPoints[-1].y)
        t.pendown()
        t.goto(rightPoints[0].x-middleX,rightPoints[0].y)
        t.penup()


        
    modeDist = 10 * 2.5

    gotoLeft = leftPoints[0].x-modeDist
    gotoRight = rightPoints[-1].x+modeDist

    if startValue == 1:
        t.goto(rightPoints[0].x-middleX,rightPoints[0].y)
        t.pendown()
        t.goto(gotoRight,rightPoints[0].y)
        t.penup()

        t.goto(rightPoints[-1].x-middleX,rightPoints[-1].y)
        t.pendown()
        t.goto(gotoRight,rightPoints[-1].y)
        t.penup()

        t.goto(leftPoints[0].x+middleX,leftPoints[0].y)
        t.pendown()
        t.goto(gotoLeft,leftPoints[0].y)
        t.penup()

        t.goto(leftPoints[-1].x+middleX,leftPoints[-1].y)
        t.pendown()
        t.goto(gotoLeft,leftPoints[-1].y)
        t.penup()

    else:
        t.goto(botPoints[0].x,botPoints[0].y)
        t.pendown()
        t.goto(gotoLeft,botPoints[0].y)
        t.penup()

        t.goto(botPoints[-1].x,botPoints[-1].y)
        t.pendown()
        t.goto(gotoRight,botPoints[-1].y)
        t.penup()



    for i in range(1,len(leftPoints)):
        t.goto(leftPoints[i].x,leftPoints[i].y)
        t.pendown()
        t.goto(gotoLeft,leftPoints[i].y)
        t.penup()

        t.goto(rightPoints[i].x,rightPoints[i].y)
        t.pendown()
        t.goto(gotoRight,rightPoints[i].y)
        t.penup()

    turtle.done()


drawSquareMesh(8)

