#!/usr/bin/python3
import random, sys, numpy, math, os

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
def l (dir):
  if dir is up:
    return left
  if dir is left:
    return down
  if dir is down:
    return right
  if dir is right:
    return up
def r (dir):
  if dir is up:
    return right
  if dir is right:
    return down
  if dir is down:
    return left
  if dir is left:
    return up

def txt (dir):
  if dir is up:
    return 'u'
  if dir is down:
    return 'd'
  if dir is left:
    return 'l'
  if dir is right:
    return 'r'
# ???
#top_left = numpy.array((-1,-1))
#top_right = numpy.array((1,-1))
#bottom_left = numpy.array((-1,1))
#bottom_right = numpy.array((1,1))
#all_corners = (top_left, top_right, bottom_left, bottom_right)
#top = object()
#bottom = object()
#left = object()
#right = object()

logging = False
backtracking = False

def walk (size):
  shape = numpy.zeros((size, size), numpy.uint)
  edge = size - 1
  end_x = 0
  end_y = edge
  if size % 2:
    #end_x = random.choice((0, edge))
    end_x = edge
  end_pos = (end_x, end_y)

  bad_states = set()
  def get_state (pos):
    bits = ['1' if x else '0' for y in shape for x in y]
    x,y = pos
    bits[y*size+x] = '1'
    num = int(''.join(bits), 2)
    return (num.to_bytes(math.ceil(num.bit_length()/8), 'big'), (x,y))


  def print_shape ():
    return trace_curve(shape, end_pos)

  def at (pos, default=None):
    x, y = pos
    if 0 <= x <= edge and 0 <= y <= edge:
      return shape[y][x]
    return default

  def edges (*pos):
    if len(pos) == 1:
      pos = pos[0]
    cur = at(pos)
    edges = []

    if logging:
      msgs = []
      rejects = False

    #if cur == 38:
      #rejects = True

    dirs = [(pos+c, c) for c in all_dirs if at(pos+c) == 0]
    forced_dirs = [((x,y),c) for (x,y),c in dirs
                   if (x,y) != end_pos and sum(1 for c2 in all_dirs
                                               if at((x,y)+c2) == 0) == 1]
    if forced_dirs:
      if len(forced_dirs) == 1:
        dirs = forced_dirs
      else:
        # Multiple forced dirs!
        dirs = []
      if logging:
        msgs.append('forced: {}'.format(dirs))
        rejects = True

    for (x,y), c in dirs:
      if logging:
        def rej (msg):
          nonlocal rejects
          msgs.append('rejected {} for {}'.format(c, msg))
          rejects = True
      c_pos = (x,y)
      if c_pos == end_pos and cur + 1 != size**2:
        if logging:
          rej('being too early')
        continue
      if x in (0, edge) and y != 0 and at(c_pos + up) == 0:
        if logging:
          rej('cutting off above')
        continue
      if y == 0 and at(c_pos + left) == 0:
        if logging:
          rej('cutting off top left')
        continue
      if (y == edge and x not in (0, edge) and
          ((end_x == 0 and at(c_pos + right) == 0) or
           (end_x == edge and at(c_pos + left) == 0))):
        if logging:
          rej('cutting off side')
        continue
      f = c_pos + c
      if (at(c_pos + l(c), 0) == 0 and at(c_pos + r(c), 0) == 0 and
          (at(f,0) != 0 or at(f + l(c),0) != 0 or at(f + r(c),0) != 0)):
        if logging:
          rej('creating a closed shape')
        continue
      if ((at(f,0)!=0 and at(c_pos+l(c),0)==0 and at(c_pos+r(c),0)==0) or
          (at(f+l(c),0)!= 0 and at(c_pos+l(c),0)==0 and at(f,0)==0) or
          (at(f+r(c),0)!= 0 and at(c_pos+r(c),0)==0 and at(f,0)==0)):
        if logging:
          rej('creating a closed shape (better)')
        continue
      if (y == 1 and c is right and at(pos + up) == 0 and
          at(c_pos + up) == 0):
        if logging:
          rej('creating a dead end to the left')
        continue
      if (c is down and
          ((x == 1 and at(pos + left) == 0 and at(c_pos + left == 0)) or
           (x == edge-1 and at(pos+right) == 0 and at(c_pos+right) == 0))
         ):
        if logging:
          rej('creating a dead end to above')
        continue
      if (y == edge - 1 and ((end_x == 0 and c is left) or
                             (end_x == edge and c is right)) and
          at(pos + down) == 0 and at(c_pos + down == 0)):
        if logging:
          rej('creating a dead end to the {}'.format('right' if end_x == 0
                                                     else 'left'))
        continue
      if get_state(c_pos) in bad_states:
        if logging:
          rej('being a bad state')
        continue
      edges.append(c)
      if logging:
        msgs.append('accepted edge: {}'.format(c))
      continue

    if logging and rejects:
      print('finding edges for {}:'.format(cur))
      print_shape()
      for msg in msgs:
        print(msg)
    return edges

  failed_steps = 0
  repeated_bad_steps = 0
  logged = False

  def walk (pos, seq=1):
    nonlocal failed_steps, repeated_bad_steps, logged
    x, y = pos
    shape[y][x] = seq
    if ((x,y) == end_pos and seq == size**2):
      return True

    if logged and backtracking:
      print('Backtracked to:')
      print_shape()
    dirs = edges(x,y)
    random.shuffle(dirs)

    logged = False
    for c in dirs:
      if walk(pos + c, seq + 1):
        return True

    if backtracking:
      print('FAILED! backtracking...')
    state = get_state(pos)
    if state in bad_states:
      print('Should have known this was a bad state!!')
      repeated_bad_steps += 1
    else:
      bad_states.add(state)
    if not logged:
      if backtracking:
        print('FAILED! backtracking...')
        print_shape()
      failed_steps += 1
      logged = True
    x, y = pos
    shape[y][x] = 0

  try:
    walk((0,0))
  except KeyboardInterrupt:
    pass

  print(failed_steps, 'failed paths')
  print(repeated_bad_steps, 'repeated bad steps, discovered', len(bad_states),
        'bad states')

  return print_shape()


def get_tile (old, new, tiles={(1,0):   '━',
                               (-1,-1): '┏',
                               (-1,1):  '┗',
                               (1,-1):  '┓',
                               (1,1):   '┛',
                               (0,1):   '┃',
                              }):
  a, b = old - new + old * new
  return tiles[(a,b)]

def get_cap (dir, tiles={(-1,0): '╺',
                         (1,0):  '╸',
                         (0,-1): '╻',
                         (0,1):  '╹'
                        }):
  a,b = dir
  return tiles[(a,b)]


def get_turn (old, new):
  if old is new:
    return ''
  if l(old) is new:
    return '+'
  if r(old) is new:
    return '-'
  return '++'

magnitude = lambda v: math.sqrt(numpy.dot(v,v))
prev_sub = 0
def get_sub (corner, prev_dir, dir, type2=False, maps={-2: '+A-',
                                                       -1: 'A',
                                                       1: 'B',
                                                       2: '-B+'}):
  global prev_sub
  v,h = corner
  c = numpy.cross(v+h, prev_dir)
  prev = int(c * magnitude(v+h+prev_dir))
  c = numpy.cross(v+h, dir)
  next = int(c * magnitude(v+h+dir))
  turn = get_turn(prev_dir, dir)

  if type2 and abs(next) == 2:
    raise ValueError("This shape doesn't work!")

  if prev != next and next == prev_sub:
    sub = maps[prev] + turn
    prev_sub = prev
  else:
    sub = turn + maps[next]
    prev_sub = next

  #print('(', txt(v), ',', txt(h), ') p =', txt(prev_dir), ', n =', txt(dir),
        #turn, prev, next, sub)
  return sub

def next_corner_type1 (corner, dir):
  v,h = corner
  if dir is left or dir is right:
    dv,dh = v,inv(dir)
  else:
    dv,dh = inv(dir),h
  if dir is h:
    dv = inv(dv)
  elif dir is v:
    dh = inv(dh)
  return (dv,dh)

def next_corner_type2 (corner, dir):
  v,h = corner
  if dir is left or dir is right:
    return (inv(v),h)
  return (v,inv(h))

def trace_curve (shape, end_pos):
  x, y = 0, 0
  prev_dir = down
  script = ''
  corner = (up,left)
  dir = down
  end_x, end_y = end_pos

  if end_x == 0:
    type2 = False
    next_corner = next_corner_type1
  else:
    type2 = True
    next_corner = next_corner_type2

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

  # A is top,left to bottom,left
  # B is top,left to top,right
  curve = [['·' for x in range(len(shape))] for y in range(len(shape))]
  while True:
    dir = next_dir(x,y)
    if dir is None:
      #script += get_turn(prev_dir, down)
      script += get_sub(corner, prev_dir, down, type2)
      break
    curve[y][x] = get_tile(prev_dir, dir)

    #script += get_turn(prev_dir, dir)
    script += get_sub(corner, prev_dir, dir, type2)
    corner = next_corner(corner, dir)

    script += 'f'

    x, y = (x,y) + dir
    prev_dir = dir

  if (x,y) == (end_x,end_y):
    curve[y][x] = get_tile(prev_dir, down)
  else:
    curve[y][x] = get_cap(prev_dir)

  for row in curve:
    for c in row:
      print(c, end='')
    print('|')
  print('-'*shape_size)

  if end_x != 0:
    print(' '*(end_x-1), end='')
  print('*')

  # simplify
  script = script.replace('+-', '')
  script = script.replace('-+', '')

  return script

if __name__ == '__main__':
  seed = eval(sys.argv[2]) if len(sys.argv) > 2 else os.urandom(10)
  random.seed(seed)
  shape_size = int(sys.argv[1]) if len(sys.argv) > 1 else 3
  script = walk(shape_size)

  print('seed: "{!r}"'.format(seed))
  print(script)

  import space_filling_curves as sfc

  gridsize = int(sfc.size/2)
  iters = int(math.log(gridsize - 1, shape_size))
  print(iters, 'iterations')
  sfc.make_curve(sfc.top_left, shape_size - 1, script, iters, -90)
