#%%
import numpy as np

from dataclasses import dataclass
@dataclass
class Point:
   x: float
   y: float

def drawPoints(Nmode):
  xpoints = []
  ypoints = []
  hspace = 10
  vspace = 10

  xpoints.append(0) #Left side xpoints
  for i in range(Nmode-1):
      xpoints.append(i*hspace)

  xbpoints = xpoints.copy() + [(max(xpoints)+(i+1)*hspace) for i in range(len(xpoints))]

  xbpoints = xbpoints[2:-2]

  for i in range(Nmode):
      ypoints.append(i*vspace)

  ybpoints = np.zeros(len(xbpoints)).tolist()

  rPoints = []
  for xpoint in xpoints:
      rPoints.append(((max(xpoints) + hspace/2) - xpoint)*2 + xpoint)

  rightPoints = []
  leftPoints = []
  botPoints = []
  for i in range(len(xpoints)):
      leftPoints.append(Point(xpoints[i],ypoints[i]))
      rightPoints.append(Point(rPoints[i],ypoints[i]))

  for i in range(len(xbpoints)):
      botPoints.append(Point(xbpoints[i],ybpoints[i]))


  return leftPoints, botPoints, rightPoints[::-1]
# %%

def drawTriangularMesh(Nmode):
    import turtle
    leftPoints, botPoints, rightPoints = drawPoints(Nmode)

    all_points = leftPoints + botPoints + rightPoints
    xs = [p.x for p in all_points]
    ys = [p.y for p in all_points]

    margin = 30

    screen = turtle.Screen()
    width = screen._root.winfo_screenwidth()
    height = screen._root.winfo_screenheight()

    print('Drawing resolution: ',width, 'x',height)


    turtle.setup(height, height)
    turtle.setworldcoordinates(
        min(xs) - margin,
        min(ys) - margin,
        max(xs) + margin,
        max(ys) + margin,
    )

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


    t.goto(leftPoints[0].x,leftPoints[0].y)
    t.pendown()
    t.goto(rightPoints[0].x,rightPoints[0].y)
    t.penup()

    toBotPoints = botPoints[::2]
    for i in range(len(toBotPoints)):
        t.goto(leftPoints[i+1].x,leftPoints[i+1].y)
        t.pendown()
        t.goto(toBotPoints[i].x,toBotPoints[i].y)
        t.penup()

    t.goto(leftPoints[-1].x,leftPoints[-1].y)
    t.pendown()
    t.goto(rightPoints[-1].x,rightPoints[-1].y)
    t.penup()

    fromBotPoints = botPoints[1::2]
    for i in range(len(toBotPoints)):
        t.goto(fromBotPoints[i].x,fromBotPoints[i].y)
        t.pendown()
        t.goto(rightPoints[i+1].x,rightPoints[i+1].y)
        t.penup()

    #connecta bots
    for i in range(len(toBotPoints)):
        t.goto(toBotPoints[i].x,toBotPoints[i].y)
        t.pendown()
        t.goto(fromBotPoints[i].x,fromBotPoints[i].y)
        t.penup()

    modeDist = 10 * 2.5

    gotoLeft = leftPoints[0].x-modeDist
    gotoRight = rightPoints[-1].x+modeDist

    for i in range(len(leftPoints)):
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
drawTriangularMesh(8)