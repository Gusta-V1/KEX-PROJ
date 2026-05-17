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

    return leftPoints, botPoints, rightPoints, topPoints[::-1]

# %%

import turtle
leftPoints, botPoints, rightPoints, topPoints = drawPoints(8)

# ── canvas / style ──────────────────────────────────────────────────────────
#WIDTH, HEIGHT = 1400, 650
#turtle.setup(WIDTH, HEIGHT)
turtle.bgcolor("white")
turtle.title("Triangular Mesh")
#turtle.tracer(0, 0)          # draw instantly

t = turtle.Turtle()
t.hideturtle()
t.speed(0)
t.pensize(2)
t.color("black")
t.penup()


fromRightPoints = rightPoints[::2]
fromLeftPoints = leftPoints[1::]
toBotPoints = botPoints[::2]
toTopPoints = topPoints[::2]

for i in range(1,len(topPoints),2):
    t.goto(leftPoints[i].x,leftPoints[i].y)
    t.pendown()
    t.goto(topPoints[i].x,topPoints[i].y)
    t.penup()

rightBack = rightPoints[::-1]
for i in range(0,len(topPoints)-1,2):
    t.goto(rightBack[i+1].x,rightBack[i+1].y)
    t.pendown()
    t.goto(topPoints[i].x,topPoints[i].y)
    t.penup()

for i in range(2,len(topPoints),2):
    t.goto(leftPoints[i].x,leftPoints[i].y)
    t.pendown()
    t.goto(botPoints[i-1].x,botPoints[i-1].y)
    t.penup()

for i in range(2,len(topPoints),2):
    t.goto(rightBack[i].x,rightBack[i].y)
    t.pendown()
    t.goto(botPoints[i].x,botPoints[i].y)
    t.penup()


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

    
modeDist = 10 * 2.5

gotoLeft = leftPoints[0].x-modeDist
gotoRight = rightPoints[-1].x+modeDist

t.goto(botPoints[0].x,botPoints[0].y)
t.pendown()
t.goto(gotoLeft,botPoints[0].y)
t.penup()

t.goto(botPoints[-1].x,rightPoints[0].y)
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
# %%
