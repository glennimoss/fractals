#!/usr/bin/python3
import random, pprint

shape_size = 3

def make_shape (size):
  return [[0 for x in range(size)] for y in range(size)]

shape = make_shape(shape_size)

def add (pos, dir):
   return (sum(z) for z in zip(pos, dir))

def walk (pos, seq=1):
  x, y = pos
  shape[y][x] = seq
  if ((x == shape_size - 1) and (y in (0, shape_size - 1))
      and seq == shape_size**2):
    return True

  dirs = [(-1,0), (1,0), (0,-1), (0,1)]
  random.shuffle(dirs)

  for c in dirs:
    x, y = add(pos, c)

    try:
      if x < 0 or y < 0 or shape[y][x]:
        continue
    except IndexError:
      continue

    if walk((x,y), seq+1):
      return True

  x, y = pos
  shape[y][x] = 0


#import pdb;pdb.set_trace()
walk((0,0))
print('Found shape')

pprint.pprint(shape)
curve = make_shape(shape_size)

def get_tile (old, new, tiles={(-2,0):  '━',
                               (-1,-1): '┛',
                               (-1,1):  '┓',
                               (1,-1):  '┗',
                               (1,1):   '┏',
                               (0,-2):  '┃',
                              }):
  return tiles[tuple(a ^ b for a, b in zip(old, new))]

def next_dir (pos):
  ox, oy = pos
  cur = shape[oy][ox]
  for c in  ((-1,0), (1,0), (0,-1), (0,1)):
    x, y = add(pos, c)

    try:
      if x < 0 or y < 0:
        continue
      if shape[y][x] == cur + 1:
        return c
    except IndexError:
      pass
  return None


def trace_curve ():
  x, y = 0, 0
  if shape[0][-1] == shape_size**2:
    enter_dir = (-1,0)
    exit_dir = (1,0)
  else:
    enter_dir = (0, -1)
    exit_dir = (0,1)
  prev_dir = enter_dir

  while True:
    dir = next_dir((x,y))
    if not dir:
      break
    curve[y][x] = get_tile(prev_dir, dir)

    x, y = add((x,y), dir)
    prev_dir = tuple(-d for d in dir)

    dir = next_dir((x,y))

  curve[y][x] = get_tile(prev_dir, exit_dir)

  return enter_dir, exit_dir

shape_vector = trace_curve()
print(shape_vector)

for row in curve:
  for c in row:
    print(c, end='')
  print()
