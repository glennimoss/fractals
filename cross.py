import numpy as np, math

u = np.array([0,-1,1])
d = np.array([0,1,1])
l = np.array([-1,0,1])
r = np.array([1,0,1])

u = np.array([0,1])
d = np.array([0,-1])
l = np.array([-1,0])
r = np.array([1,0])

mag = lambda v: math.sqrt(np.dot(v,v))
def calc (v,h,d):
  c = np.cross((v+h), d)
  return int(c * mag(v+h+d))

def signed (a,b):
  return a[0]*b[1] - a[1]*b[0]

for sv, v in (('u',u),('d',d)):
  for sh, h in (('l',l),('r',r)):
    for sd, z in (('u',u),('d',d),('l',l),('r',r)):
      print('(', sv, '+', sh, ') x', sd,'=',calc(v,h,z))
      #print('(', sv, '+', sh, '+', sd,') =',mag(v+h+z))

