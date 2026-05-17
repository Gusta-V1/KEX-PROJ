"""
Triangular mesh / braid pattern drawn with Python turtle.

The image shows N horizontal lines that each travel straight, then
diagonal-up or diagonal-down through a central "weave" zone, then
straight again.  The diagonals interleave to form a diamond/braid mesh.

Strategy
--------
Each line is drawn as a polyline with up to five segments:
  1. Horizontal run from the left edge to the weave entry point
  2. 45-degree diagonal going UP  (toward the apex)
  3. Short 45-degree diagonal going DOWN (through a crossing)
  4. 45-degree diagonal going UP again  (out of the crossing)
     ... this repeats for every diamond column in the weave zone ...
  5. Horizontal run to the right edge

Looking at the image more carefully:
- There are ~9 lines total.
- Lines enter the weave zone at staggered x-positions (lower lines enter later).
- Inside the weave zone each line alternates between going diagonally up
  and diagonally down, producing the diamond lattice.
- The pattern is symmetric left-right.
- The bottom line has the widest weave; upper lines have narrower weaves.
"""

import turtle


# ── canvas / style ──────────────────────────────────────────────────────────
WIDTH, HEIGHT = 1400, 650
turtle.setup(WIDTH, HEIGHT)
turtle.bgcolor("white")
turtle.title("Triangular Mesh")
turtle.tracer(0, 0)          # draw instantly

t = turtle.Turtle()
t.hideturtle()
t.speed(0)
t.pensize(2)
t.color("black")

# ── geometry parameters ──────────────────────────────────────────────────────
N_LINES      = 2            # total horizontal lines
LINE_SPACING = 55           # vertical gap between lines (px)
DIAG_UNIT    = LINE_SPACING # one diagonal step = one line-spacing (45°)

# The weave zone is centred horizontally.
# The bottom line fans out the widest; each higher line fans out one
# unit less on each side.
CANVAS_LEFT  = -WIDTH  // 2 + 30
CANVAS_RIGHT =  WIDTH  // 2 - 30

# Y positions: top line first
top_y = (N_LINES - 1) / 2 * LINE_SPACING
ys = [top_y - i * LINE_SPACING for i in range(N_LINES)]

# Centre x of the whole pattern
CX = 0

# How many diamond columns does the *bottom* line span?
# From the image: the apex is 1 diamond wide at the top, widening by
# 1 column per extra line.  Bottom line (index 8) → 8 diamonds wide.
# Each diamond is 2*DIAG_UNIT wide (up then down).


def draw_line(row_index):
    """
    Draw one line of the mesh.

    row_index: 0 = top line, N_LINES-1 = bottom line.

    The top line is almost straight (very small weave).
    The bottom line has the widest weave.
    """
    y = ys[row_index]

    # Number of up/down zigzag legs inside the weave zone.
    # Top line (row 0): 2 legs (one up, one down)  → 1 diamond
    # Each additional row adds 2 more legs.
    n_legs = 2 * (row_index + 1)   # always even

    # Total horizontal width consumed by the weave zone
    weave_width = n_legs * DIAG_UNIT   # each leg advances DIAG_UNIT horizontally

    weave_left  = CX - weave_width / 2
    weave_right = CX + weave_width / 2

    # ── collect waypoints ────────────────────────────────────────────────
    pts = []

    # 1. Start at left canvas edge, same y
    pts.append((CANVAS_LEFT, y))

    # 2. Go horizontally to weave entry
    pts.append((weave_left, y))

    # 3. Zigzag through the weave
    # The first diagonal goes UP (toward the apex).
    x = weave_left
    direction = +1   # +1 = going up, -1 = going down
    for _ in range(n_legs):
        x     += DIAG_UNIT
        new_y  = y + direction * DIAG_UNIT
        pts.append((x, new_y))
        direction *= -1   # alternate

    # After the zigzag we should be back at y  (even number of legs)
    # 4. Horizontal to right canvas edge
    pts.append((CANVAS_RIGHT, y))

    # ── draw ─────────────────────────────────────────────────────────────
    t.penup()
    t.goto(pts[0])
    t.pendown()
    for p in pts[1:]:
        t.goto(p)


# Draw all lines
for i in range(N_LINES):
    draw_line(i)

turtle.update()
turtle.done()
