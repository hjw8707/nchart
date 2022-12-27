import re
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as col
mpl.rcParams['pdf.fonttype'] = 42
import numpy as np

import sys

##################################################################
# Database Loading
#
# to 'dbDic' (dictionary)
##################################################################
# 1. mass table
##################################################################
f = open('./mass_1.mas20','r')
lines = f.readlines()
f.close()
del lines[:36]

keys = ['cc', 'NZ', 'N', 'Z', 'A', '', 'el', 'o', '', 'mass', 'massu', 
        'bind', '', 'bindu','', 'B', 'beta', 'betau', '', 'atm1', '', 'atm2', 'atmu']
lens = [1, 3, 5, 5, 5, 1, 3, 4, 1, 14, 12, 13, 1, 10, 1, 2, 13, 11, 1, 3, 1, 13, 12]

dbDic = {}
for line in lines:
  tempArr = []
  s = 0
  for l in lens:
   tempArr.append(line[s:s+l])
   s += l
  tempDic = {}
  for (k, v) in zip(keys, tempArr):
   if k == '': continue
   tempDic[k] = v.strip()
  dbDic[(int(tempDic['Z']),int(tempDic['N']))] = tempDic

##################################################################
# 2. S(2n), ...
##################################################################
f = open('./rct1.mas20','r')
lines = f.readlines()
f.close()
del lines[:35]

keys = ['cc', 'A', '', 'el', 'Z', '', 's2n', 's2nu', 's2p', 's2pu', 'qa', 'qau', 
        'q2b', 'q2bu', 'qep', 'qepu', 'qbn', 'qbnu' ]
lens = [ 1, 3, 1, 3, 3, 1, 12, 10, 12, 10, 12, 10, 12, 10, 12, 10, 12, 10 ]

for line in lines:
  tempArr = []
  s = 0
  for l in lens:
   tempArr.append(line[s:s+l])
   s += l
  tempDic = {}
  for (k, v) in zip(keys, tempArr):
   if k == '': continue
   tempDic[k] = v.strip()
  z = int(tempDic['Z'])
  n = int(tempDic['A']) - z
  if (z, n) in dbDic:
    for k in tempDic.keys():
      if k not in dbDic[(z,n)]:
        dbDic[(z,n)][k] = tempDic[k]

##################################################################
# 3. S(n), ...
##################################################################
f = open('./rct2_1.mas20','r')
lines = f.readlines()
f.close()
lines = lines[37:3595]

keys = ['cc', 'A', '', 'el', 'Z', '', 'sn', 'snu', 'sp', 'spu', 'q4b', 'q4bu', 
        'qda', 'qdau', 'qpa', 'qpau', 'qna', 'qnau' ]
lens = [ 1, 3, 1, 3, 3, 1, 12, 10, 12, 10, 12, 10, 12, 10, 12, 10, 12, 10 ]

for line in lines:
  tempArr = []
  s = 0
  for l in lens:
   tempArr.append(line[s:s+l])
   s += l
  tempDic = {}
  for (k, v) in zip(keys, tempArr):
   if k == '': continue
   tempDic[k] = v.strip()
  z = int(tempDic['Z'])
  n = int(tempDic['A']) - z
  if (z, n) in dbDic:
    for k in tempDic.keys():
      if k not in dbDic[(z,n)]:
        dbDic[(z,n)][k] = tempDic[k]

##################################################################
# 4. Nubase
##################################################################
f = open('./nubase_3.mas20','r')
lines = f.readlines()
f.close()
lines = lines[25:]

keys = ['A', '', 'Z', 'I', '', 'Ael', 's', '', 'mass', 'massu', 'iex', 'iexu', 
        'exo', 'iu', 'ii', 't', 'tuni', '', 'tu', 'jpi', 'year', '', 'dis', '', 'br' ]
lens = [ 3, 1, 3, 1, 3, 5, 1, 1, 13, 11, 12, 11, 2, 1, 1, 9, 2, 1, 7, 14, 2, 10, 4, 1, 90 ]

for line in lines:
  tempArr = []
  s = 0
  for l in lens:
   tempArr.append(line[s:s+l])
   s += l
  if int(tempArr[3]) != 0: continue # no isomer
  tempDic = {}
  for (k, v) in zip(keys, tempArr):
   if k == '': continue
   tempDic[k] = v.strip()
  z = int(tempDic['Z'])
  n = int(tempDic['A']) - z
  if (z, n) in dbDic:
    for k in tempDic.keys():
      if k not in dbDic[(z,n)]:
        dbDic[(z,n)][k] = tempDic[k]
        
def nuExist(z, n):
  return (z,n) in dbDic

def nuName(z, n):
  if (z,n) in dbDic:
    return '$^{'+dbDic[(z,n)]['A']+'}$'+dbDic[(z,n)]['el']
  return None  

def nuGet(z, n, item):
  if (z,n) in dbDic:
    try:
      bind = float(dbDic[(z,n)][item])
    except:
      bind = float(dbDic[(z,n)][item].replace('#','.'))
    return bind
  else:
    return None

def nuBE(z, n): return nuGet(z, n, 'bind')
def nuSn(z, n): return nuGet(z, n, 'sn')
def nuSp(z, n): return nuGet(z, n, 'sp')
def nuS2n(z, n): return nuGet(z, n, 's2n')
def nuS2p(z, n): return nuGet(z, n, 's2p')
def nuQa(z, n): return nuGet(z, n, 'qa')

def timeUnit(x):
  return {'s': 1., 'ms': 1E-3, 'us': 1E-6, 'ns': 1E-9, 'ps': 1E-12, 
          'fs': 1E-15, 'as': 1E-18, 'zs': 1E-21, 'ys': 1E-24, 
          'm': 60., 'h': 3600., 'd': 86400., 
          'y': 3.1536E7, 'ky': 3.1536E10, 'My': 3.1536E13, 'Gy': 3.1536E16, 
          'Ty': 3.1536E19, 'Py': 3.1536E22, 'Ey': 3.1536E25, 'Zy': 3.1536E28,
          'Yy': 3.1536E31}.get(x, 0)

tStbl = 1E40
tUnstbl = 1E-40

def nuTime(z, n):
  if (z,n) in dbDic:
    t = dbDic[(z,n)]['t']
    tuni = dbDic[(z,n)]['tuni']
    if tuni == '':
      if t == 'stbl': return tStbl
      else:           return tUnstbl
    fac = timeUnit(tuni)
    try:
      tfl = float(t)
    except:
      tfl = float(t.replace('#', '.').replace('>', '').replace('<','').replace('~',''))
    return tfl * fac
  else:
    return None

def nuLogTime(z, n):
  return np.log10(nuTime(z,n))

def nuMajorDecayChannel(z, n):
  if (z,n) in dbDic:
    br = dbDic[(z,n)]['br']
    return re.split('[ =~><]', br)[0]
  else:
    return None

def decayChannel(x):
  return {'2n': -4, 'n': -3, 'B-': -2, 'SF': -1, 'IS': 0, 
          'A': 1, 'B+': 2, 'EC': 3, 'p': 4, '2p':5, '3p':6}.get(x, -20)

def stableOrNot(x):
  return {'2n': -1, 'n': -1, 'B-': -1, 'SF': -1, 'IS': 0, 
          'A': 0, 'B+': 1, 'EC': 1, 'p': 1, '2p':1, '3p':1}.get(x, -20)

def nuMajorDecayChannelNum(z, n):
  return decayChannel(nuMajorDecayChannel(z,n))

def nuMajorStableOrNotNum(z, n):
  return stableOrNot(nuMajorDecayChannel(z,n))
  
scalarMap = cm.ScalarMappable(col.Normalize(vmin=0, vmax=1), 'Paired')

z_min = 10
n_min = 10
z_max = 20
n_max = 24
#z_max = 44
#n_max = 44

(z_low, z_upp) = (z_min, z_max + 1)
(n_low, n_upp) = (n_min, n_max + 1)

def textConvert(val):
    s = '%.0e' % val
    d = int(s[0])
    c = int(s[-3:])
    return '%1dx10$^{%1d}$' % (d, c)

def drawRect(x, y, z, t, data):
  #fcol = scalarMap.to_rgba(z)
  if (y,x) not in mapData.keys():
    colors = ['#bbbbff', '#666666', '#ffbbbb' ]
  else:
    colors = ['#5555ff', '#111111', '#ff5555' ]

  fcol = col.to_rgba(colors[z+1])  
  (h, s, v) = col.rgb_to_hsv(fcol[:3])
  tcol = 'w' if h > 0.5 else 'k'
  if z == 0: tcol = 'w'

  if (y,x) in mapData.keys() and z == 1:
    rectangle = plt.Rectangle((x-0.5,y-0.5), 1, 1, fc=fcol, ec='red', lw=5)    
  elif (y,x) in mapData.keys() and z == -1:
    rectangle = plt.Rectangle((x-0.5,y-0.5), 1, 1, fc=fcol, ec='red', lw=5)        
  else:
    rectangle = plt.Rectangle((x-0.5,y-0.5), 1, 1, fc=fcol, ec='black', lw=0.1)      
  plt.gca().add_patch(rectangle)
  plt.text(x,y,t, ha='center', va='center', fontsize=20, color=tcol)
  ###### for database check ####
  if (y,x) in mapData.keys(): 
    plt.text(x,y-0.45,'%s mb' % textConvert(mapData[(y,x)]), ha='center', va='bottom', fontsize='large', color=tcol)

def loadData(filename):
    f = open(filename,'r')
    lines = f.readlines()
    f.close()
    tempDic = {}   
    for line in lines:
        words = line.split()   
        tempDic[(int(words[0]),int(words[1]))] = float(words[3])
    return tempDic


fig = plt.figure(figsize=(n_max, z_max))
ax = plt.subplot()
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.yaxis.set_ticks_position('left')
ax.xaxis.set_ticks_position('bottom')
ax.axis('off')



drawList = []
drawValue = []
mapData = loadData('he3_30mev.txt')
for z in range(z_low,z_upp):
  for n in range(n_low,n_upp):
#    if nuExist(z,n): 
    if nuExist(z,n): # and (z,n) in mapData.keys(): 
      drawList.append((z, n))
#      drawValue.append(nuBE(z,n))
#      drawValue.append(nuLogTime(z,n))
#      drawValue.append(nuMajorDecayChannelNum(z,n))
      drawValue.append(nuMajorStableOrNotNum(z,n))
drawValue = np.array(drawValue)

#drawValue = (drawValue[:] - drawValue[:].min())/(drawValue[:].max() - drawValue[:].min())
for (z, n), c in zip(drawList, drawValue):
  drawRect(n, z, c, nuName(z,n), mapData)

for (z, n), c in zip(drawList, drawValue):
    if (z,n) in mapData.keys() and c != 0:
        drawRect(n, z, c, nuName(z,n), mapData)


ax.set_xlim([n_low-1,n_upp+1])
ax.set_ylim([z_low-1,z_upp+1])

#plt.show()
#fig.savefig('output.eps', format='eps')  
fig.savefig('output.png', format='png')  