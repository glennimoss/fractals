#!/usr/bin/python3
import random, sys, numpy

up = numpy.array((0,-1))
down = numpy.array((0,1))
left = numpy.array((-1,0))
right = numpy.array((1,0))
all_dirs = (up, down, left, right)
for d in all_dirs:
  d.flags.writeable = False
def inv (dir):
  if dir is up:
    return down
  if dir is down:
    return up
  if dir is left:
    return right
  if dir is right:
    return left

top_left = numpy.array((-1,-1))
top_right = numpy.array((1,-1))
bottom_left = numpy.array((-1,1))
bottom_right = numpy.array((1,1))
all_corners = (top_left, top_right, bottom_left, bottom_right)


def walk (size):
  shape = numpy.zeros((size, size), numpy.uint)
  edge = size - 1
  end_x = 0
  end_y = edge
  if size % 2:
    end_x = random.choice((0, edge))
  end_pos = (end_x, end_y)
  #print("today's end_pos is", end_pos)


  def edges (*pos, lax=False):
    if len(pos) == 1:
      pos = pos[0]
    x, y = pos
    cur = shape[y][x]
    edges = []

    #if not lax:
      #print('finding edges:')
      #print(shape)
    for c in all_dirs:
      try:
        x, y = pos + c
        if x >= 0 and y >= 0 and shape[y][x] == 0:
          if not lax:
            if (x,y) == end_pos and cur + 1 != size**2:
              #print('rejected', c, 'for being too early')
              continue
            if x in (0, edge) and y != 0 and shape[y-1][x] == 0:
              #print('rejected', c, 'for cutting off above')
              continue
            if y == 0 and shape[y][x-1] == 0:
              #print('rejected', c,' for cutting off top left')
              continue
            if (y == edge and x not in (0, edge) and
                ((end_x == 0 and shape[y][x+1] == 0) or
                 (end_x == edge and shape[y][x-1] == 0))):
              #print('rejected', c, 'for cutting off side')
              continue
          edges.append(c)
          #if not lax:
            #print('accepted edge:', c)
          continue
      except IndexError:
        pass
    return edges

  failed_steps = 0

  def walk (pos, seq=1):
    nonlocal failed_steps
    x, y = pos
    shape[y][x] = seq
    if ((x,y) == end_pos and seq == size**2):
      return True

    dirs = edges(x,y)
    if len(dirs) > 1:
      forced_dirs = [c for c in dirs if len(edges(pos + c, lax=True)) == 1]
      #print(dirs, forced_dirs)
      if len(forced_dirs) > 1:
        # Multiple forced edges... abort now!
        dirs = []
      elif forced_dirs:
        dirs = forced_dirs
    random.shuffle(dirs)

    for c in dirs:
      if walk(pos + c, seq + 1):
        return True

    #print('FAILED! backtracking...')
    failed_steps += 1
    x, y = pos
    shape[y][x] = 0

  walk((0,0))
  print(failed_steps, 'failed steps')

  return shape


def get_tile (old, new, tiles={(1,0):   '━',
                               (-1,-1): '┏',
                               (-1,1):  '┗',
                               (1,-1):  '┓',
                               (1,1):   '┛',
                               (0,1):   '┃',
                              }):
  a, b = old - new + old * new
  return tiles[a,b]

#def get_turn (old, new, tiles={(-2,0):  '━',
                               #(-1,-1): '┛',
                               #(-1,1):  '┓',
                               #(1,-1):  '┗',
                               #(1,1):   '┏',
                               #(0,-2):  '┃',
                              #}):

  #left, right : '' (-1,0)+(1,0) = (0,0).prod() = 0
  #up, down: '' (-1,0)+(1,0) = (0,0).prod() = 0
  #up, left: '-' (0,-1)+(-1,0) = (-1,-1).prod() = 1
  #up, right: '+' (0,-1)+(1,0) = (1,-1).prod() = -1
  #down, left: '+' (0,1)+(-1,0) = (-1,1).prod() = -1
  #down, right: '-' (0,1)+(1,0) = (1,1).prod() = 1
  #left, up: '+' (-1,0)+(0,-1) = (-1,-1).prod() = 1
  #left, down: '-'
  #right, up: '-'
  #right, down: '+'




  a, b = old ^ new
  return tiles[a,b]

def next_dir (*pos):
  x, y = pos
  cur = shape[y][x]
  for c in  all_dirs:
    x, y = pos + c

    try:
      if x < 0 or y < 0:
        continue
      if shape[y][x] == cur + 1:
        return c
    except IndexError:
      pass
  return None


def trace_curve (shape):
  x, y = 0, 0
  prev_dir = down
  script = ''

  curve = [['' for x in range(len(shape))] for y in range(len(shape))]
  while True:
    dir = next_dir(x,y)
    if dir is None:
      break
    curve[y][x] = get_tile(prev_dir, dir)

    x, y = (x,y) + dir
    prev_dir = dir

    dir = next_dir(x,y)

  curve[y][x] = get_tile(prev_dir, down)

  #if shape[-1][-1] == shape_size**2:
    #return bottom_right
  #return bottom_left

  return curve


if __name__ == '__main__':
  shape_size = int(sys.argv[1]) if len(sys.argv) > 1 else 3
  shape = walk(shape_size)
  print(shape)
  #shape =  numpy.array([[(x*(1 - 2*(y%2)) + 1 - (y%2) + (y + y%2)*5) for x in range(5)] for y in range(5)])
  curve = trace_curve(shape)

  for row in curve:
    for c in row:
      print(c, end='')
    print()
