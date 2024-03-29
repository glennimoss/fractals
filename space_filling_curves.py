#!/usr/bin/python3

import turtle

size = 900

def inverse_dirs (p, _trans=str.maketrans('+-lr', '-+rl')):
  return p.translate(_trans)

def inverse_order (p):
  return ''.join(reversed(p))

inverse = inverse_dirs
#inverse = inverse_order

def make_curve (start_pos, gridsize, prog, iters, heading=-90):
  global size
  gridsize = (gridsize+1)**iters - 1
  len = int(size/gridsize)
  wlen = 2**(1/2)*len
  if len < 2:
    #raise ValueError('Grid is too small')
    len = 2
  size = len*gridsize
  posx, posy = start_pos
  turtle.hideturtle()
  turtle.speed(0)
  turtle.delay(0)
  turtle.setup(size + 20, size + 20, 0, None)
  turtle.penup()
  turtle.setpos(posx*size/2, posy*size/2)
  turtle.setheading(heading)
  turtle.pendown()

  cmds = { 'f': lambda p, i: turtle.forward(len)
         , '+': lambda p, i: turtle.left(90)
         , '-': lambda p, i: turtle.right(90)
         , 'l': lambda p, i: turtle.left(45)
         , 'r': lambda p, i: turtle.right(45)
         , 'w': lambda p, i: turtle.forward(wlen)
         , 'A': lambda p, i: exec(p, i-1)
         , 'B': lambda p, i: exec(inverse(p), i-1)
         }

  def exec (p, i):
    if i > 0:
      for cmd in p:
        cmds[cmd](p, i)

  turtle.tracer(0)
  turtle.tracer(iters*2)
  exec(prog, iters)
  turtle.update()
  turtle.exitonclick()

bottom_left = (-1, -1)
top_left = (-1, 1)

def hilbert (iters):
  make_curve(top_left, 1, '+Bf-AfA-fB+', iters)

def peano (iters):
  make_curve(top_left, 2, 'AfBfA+f+BfAfB-f-AfBfA', iters)

def evil_peano (iters):
  make_curve(top_left, 2, 'Af-A+fA+fA+fAf-Af-Af-A+fA', iters)

def moss (iters):
  prog = 'AfAf+BfBfB+f+Bf-AfA-fBf-AfAfAfA-fBfBfB+'
  make_curve(top_left, 3, prog, iters)

def hole (iters):
  prog = '+BfBf-AfAfA-fBfB+'
  make_curve(bottom_left, 2, prog, iters)

def sierp (iters):
  prog = 'Af+BfB+fA-fBf-Af+Bf-AfAfA-fB+fA-fBf-Af+BfB+fA'
  make_curve(bottom_left, 4, prog, iters)

def spiral (iters):
  prog = ('AfBfAfBfAfBf-BfAfBfAfBf-BfAfBfAfBf-BfAfBf-BfArwrB'
          'lwlAfB+fBfAfB+fBfAfBfAfB+fBfAfBfAfB+fBfAfBfAfBfA')
  make_curve(top_left, 6, prog, iters)

def spiral2 (iters):
  prog = ('AfBfAfBfAfBf-BfAfBfAfBf-BfAfBfAfBf-BfAfBf-BfAfBf-B'
         'f-Bf-B+fB+fB+fBfAfB+fBfAfB+fBfAfBfAfB+fBfAfBfAfB+fBfAfBfAfBfA')
  make_curve(top_left, 6, prog, iters)

if __name__ == '__main__':

  import sys
  globals()[sys.argv[1]](int(sys.argv[2]))
