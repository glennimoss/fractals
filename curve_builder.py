import random, pprint

shape = [[0,0,0,0,0],
         [0,0,0,0,0],
         [0,0,0,0,0],
         [0,0,0,0,0],
         [0,0,0,0,0]]

def walk (pos, seq=1):
  #print('walk {}'.format(pos))
  x, y = pos
  shape[y][x] = seq
  if (pos != (0,0) and x in (0,len(shape) - 1) and (y in (0, len(shape) - 1)) and
      seq == len(shape)**2):
    return True


  dirs = [(-1,0), (1,0), (0,-1), (0,1)]
  random.shuffle(dirs)

  for c in dirs:
    x, y = (sum(z) for z in zip(pos, c))

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

tiles = {((-1,0),(-1,0)): '━',
         ((-1,0),(0,-1)): '┛',
         ((-1,0),(0,1)):  '┓',
         ((1,0),(1,0)):   '━',
         ((1,0),(0,-1)):  '┗',
         ((1,0),(0,1)):   '┏',
         ((0,-1),(-1,0)): '┛',
         ((0,-1),(1,0)):  '┗',
         ((0,-1),(0,-1)): '┃',
         ((0,1),(-1,0)):  '┓',
         ((0,1),(1,0)):   '┏',
         ((0,1),(0,1)):   '┃',
        }
print(tiles)
def walkprint (pos=(0,0), prev_dir=(0,-1)):
  ox, oy = pos
  cur = shape[oy][ox]
  for c in  ((-1,0), (1,0), (0,-1), (0,1)):
    x, y = (sum(z) for z in zip(pos, c))

    try:
      if x < 0 or y < 0:
        continue
      if shape[y][x] == cur + 1:
        shape[oy][ox] = tiles[(prev_dir, c)]
        walkprint((x,y), c)
        break
    except IndexError:
      pass


walkprint()
for row in shape:
  for c in row:
    print(c, end='')
  print()
