import matplotlib.pyplot as plt
import matplotlib.patches as patches  
import matplotlib.cm as cm
import matplotlib.colors as col
import matplotlib.image as img
import matplotlib.lines as lin
from matplotlib.textpath import TextPath
from matplotlib.font_manager import FontProperties
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.transforms as trans

#mpl.rcParams['pdf.fonttype'] = 42
import numpy as np
from nudb import NuDB
import re
import time
from typing import List

col1 = ['#E725A6','#EA457C','#E39A82', '#75F075', '#333333', '#F0F075', '#75DBF0', '#35E9BC', '#759EF0', '#9475F0', '#B375F0'] 
leg1 = [r'$2n$', r'$n$', r'$\beta -$', 'Fission', 'Stable', r'$\alpha$', r'$\beta +$', r'$e$-capture', r'$p$', r'$2p$', r'$3p$']
col2 = ['#C6F2FB', '#333333','#FFAEC9', '#EEEEEE']
leg2 = [r'$n$-rich', 'Stable', r'$p$-rich', 'p-unstable']
# returning 2n, n, B-, SF, IS, A, B+, EC, p, 2p, 3p
cmap1 = LinearSegmentedColormap.from_list('my_cmap1', col1, N=11)
cmap2 = LinearSegmentedColormap.from_list('my_cmap2', col2, N=4)
scalarMap1 = cm.ScalarMappable(col.Normalize(vmin=-4.5, vmax=6.5), cmap=cmap1)
scalarMap2 = cm.ScalarMappable(col.Normalize(vmin=-1.5, vmax=2.5), cmap=cmap2)
scalarMap3 = cm.ScalarMappable(col.Normalize(vmin=0, vmax=1), cmap='viridis')
scalarMap4 = cm.ScalarMappable(col.Normalize(vmin=0, vmax=1), cmap='binary')
smaps = [scalarMap1, scalarMap2, scalarMap3, scalarMap3, scalarMap3, scalarMap3, scalarMap4]

def VectorText(ax, x, y, t, size, tcol, ha='center', va='center', rotation=None, w='normal', f='DejaVu Sans'):
  fp = FontProperties(family=f, weight=w)
  path1 = TextPath((0, 0), t, prop=fp, size=size)
  x0, y0 = np.amin(np.array(path1.vertices), axis=0)
  x1, y1 = np.amax(np.array(path1.vertices), axis=0)
  tr2d = trans.Affine2D()
  if ha == 'center':  x_tr = -(x1-x0)/2
  elif ha == 'right': x_tr = -(x1-x0)
  else:               x_tr = 0
  if va == 'center':  y_tr = -(y1-y0)/2
  elif va == 'bottom': y_tr = -(y1-y0)
  else:               y_tr = 0
  if rotation == 'vertical': rot = 90
  else: rot = 0
  if ax.yaxis_inverted(): y_scale = -1
  else: y_scale = 1
  
  tr = tr2d.translate(x_tr, y_tr).rotate_deg(rot).scale(1,y_scale).translate(x, y) + ax.transData
  p1 = patches.PathPatch(path1, fc=tcol, lw=0, alpha=1, transform=tr)      
  ax.add_patch(p1)

class nchart:
  #############################################
  # input
  z_min, z_max = 0, 20
  n_min, n_max = 0, 24

  border_width = 0.5
  font_size = 0.3

  flag_name = True
  flag_value = False
  flag_axis = True
  flag_logo = True
  flag_leg  = True
  flag_magic = True

  bg_color = '#ffffff'

  wid_mg = 1
  ln_col_mg = 'r'
  ft_col_mg = 'k'
  txt_mg = 2

  n_hl = 4
  fl_hl: List[bool] = []
  bd_wid_hl: List[float] = []
  bd_col_hl: List[str] = []
  ft_siz_hl: List[float] = []
  fl_name_hl: List[bool] = []
  bg_col_hl: List[str] = []
  bg_alp_hl: List[float] = []
  
  border_width_bg = 0
  border_color_bg = '#000000'
  bg1_col_bg = '#eeeeee'
  bg2_col_bg = '#dddddd'

  n_value = 0 
  # 6 = no color
  # 0 = major decay pattern, 
  # 1 = stable or not (n, p-rich)
  # 2 = lifetime (log)
  # 3 = binding energy
  # 4 = Sn
  # 5 = Sp
  #############################################

  def Zero(self, z, n): return 0
  def StrZero(self, z, n): return None
  
  def __init__(self, fig = 0): # ax should be 'axes' for matplotlib
    ###########################################
    # Load matplotlib
    if fig == 0:
      self.flagExt = False
      self.fig = plt.figure()
    else:
      self.flagExt = True
      self.fig = fig
    ###########################################
    self.nu = NuDB()  # Nuclear DB
    
    self.hl = [] # highlight array
    self.bg = [] # background array: (z, n, bound or unbound)

    #############################################
    # initialization
    for i in range(self.n_hl):
      self.fl_hl.append(True)      
      self.bd_wid_hl.append(1)
      self.bd_col_hl.append('#000000')
      self.ft_siz_hl.append(0.4)
      self.fl_name_hl.append(False)
      self.bg_col_hl.append('#ffaaaa')
      self.bg_alp_hl.append(1)
      self.hl.append([])
    #############################################

  def ConvText(self, val):
    s = '%.0e' % val
    d = int(s[0])
    c = int(s[-3:])
    return '%1dx10$^{%1d}$' % (d, c)

  def SetParameters(self):
    self.x_min, self.x_max = self.n_min - 2, self.n_max + 2
    self.y_min, self.y_max = self.z_min - 2, self.z_max + 2
    self.x_width = self.x_max - self.x_min
    self.y_width = self.y_max - self.y_min

  def SetAxis(self):
    self.fig.set_facecolor(self.bg_color)
        
    self.ax = self.fig.add_axes([0,0,1,1], aspect=1)
    self.ax.spines['right'].set_visible(False)
    self.ax.spines['top'].set_visible(False)
    self.ax.yaxis.set_ticks_position('left')
    self.ax.xaxis.set_ticks_position('bottom')
    self.ax.axis('off')    
    
    self.ax.set_xlim([self.x_min-1,self.x_max+1])
    self.ax.set_ylim([self.y_min-1,self.y_max+1])    
    
  def DrawRect(self, x, y, z, t, val = None):
    fcol = (1, 1, 1, 1) if np.isnan(z) else smaps[self.n_value].to_rgba(z)
    tcol = 'w' if col.rgb_to_hsv(fcol[:3])[2] < 0.5 else 'k'
    bcol = 'w' if col.rgb_to_hsv(self.fig.get_facecolor()[:3])[2] < 0.5 else 'k'    
    rectangle = patches.Rectangle((x-0.5,y-0.5), 1, 1, fc=fcol, ec=bcol, lw=self.border_width)      
    self.ax.add_patch(rectangle)
    if self.flag_name:  
      VectorText(self.ax, x, y, t, size=self.font_size, tcol=tcol)
    if self.flag_value and val != None and val != '': 
      VectorText(self.ax, x, y-0.3, val, size=self.font_size*2/3., tcol=tcol)
    ###### for database check ####
    #if (y,x) in mapData.keys(): 
    #  plt.text(x,y-0.45,'%s mb' % textConvert(mapData[(y,x)]), ha='center', va='bottom', fontsize='large', color=tcol)

  def DrawAxis(self):
    fcol = 'w' if col.rgb_to_hsv(self.fig.get_facecolor()[:3])[2] < 0.5 else 'k'   
    self.ax.add_patch(patches.FancyArrow(self.x_min, self.y_min, 2, 0, lw = 1, color = fcol, head_width = 0.2, fc = fcol))
    self.ax.add_patch(patches.FancyArrow(self.x_min, self.y_min, 0, 2, lw = 1, color = fcol, head_width = 0.2, fc = fcol))
    VectorText(self.ax, self.x_min + 4, self.y_min, 'Neutrons', size=0.3, tcol=fcol)
    VectorText(self.ax, self.x_min, self.y_min + 4, 'Protons', size=0.3, tcol=fcol, rotation='vertical')
  
  def DrawMagicLine(self):
    magic_n = [ 2, 8, 20, 28, 50, 82, 126 ]
    range_z = [ (1,8), (3,20), (13,41), (20,54), (49,90), (96,138), (96,138)]
    range_n = [ (1,6), (2,14), ( 8,28), (11,33), (26,50), (45, 73), (76,93) ]
    lext = 2
    for (z, rz, rn) in zip(magic_n, range_z, range_n):
      if z <= self.z_max and z >= self.z_min:
        self.ax.add_line(lin.Line2D([rz[0]-lext,rz[1]+lext], [z, z], linewidth=self.wid_mg, color=self.ln_col_mg))
        VectorText(self.ax, rz[0]-lext-0.5, z, str(z), size=self.txt_mg, tcol=self.ft_col_mg, ha='right')
      if z <= self.n_max and z >= self.n_min:
        self.ax.add_line(lin.Line2D([z, z], [rn[0]-lext,rn[1]+lext], linewidth=self.wid_mg, color=self.ln_col_mg))
        VectorText(self.ax, z, rn[0]-lext-0.5, str(z), size=self.txt_mg, tcol=self.ft_col_mg, va='bottom')

  def DrawLogo(self):
    self.ax_logo = self.fig.add_axes([0.94,0.94,0.05,0.05], aspect=1, anchor='NE')  
    self.ax_logo.axis(False)
    logo = img.imread('logo.png') if col.rgb_to_hsv(self.fig.get_facecolor()[:3])[2] < 0.5 else img.imread('logo_light.png') 
    self.ax_logo.imshow(logo, aspect='equal')
  
  def DrawLegend(self):
    self.ax_leg = self.fig.add_axes([0.0,0.8,0.2,0.2], aspect=1, anchor='NW')
    self.ax_leg.axis(False)
    self.ax_leg.set_xlim([-1, 7])
    self.ax_leg.set_ylim([7, -1])  
      
    tcol = 'w' if col.rgb_to_hsv(self.fig.get_facecolor()[:3])[2] < 0.5 else 'k'       
    if self.n_value == 0:
      for i in range(11):
        fcol = smaps[self.n_value].to_rgba(i-4)      
        rectangle = patches.Rectangle((int(i/6)*4-0.25, int(i%6)-0.25), 0.5, 0.5, fc=fcol, lw=0)      
        self.ax_leg.add_patch(rectangle)
        VectorText(self.ax_leg, int(i/6)*4+2,int(i%6),leg1[i], size=0.5, tcol=tcol)
    elif self.n_value == 1:
      for i in range(3):
        fcol = smaps[self.n_value].to_rgba(i-1)      
        rectangle = patches.Rectangle((int(i/6)*4-0.25, int(i%6)-0.25), 0.5, 0.5, fc=fcol, lw=0)      
        self.ax_leg.add_patch(rectangle)
        VectorText(self.ax_leg, int(i/6)*4+2,int(i%6),leg2[i], size=0.5, tcol=tcol)         
    
  def DrawColorBar(self):
    self.ax_cb = self.fig.add_axes([0.04,0.97,0.35,0.01])    
    self.cb = plt.colorbar(smaps[self.n_value], self.ax_cb, orientation='horizontal')
        
  def DrawChart(self):
    self.SetParameters()
    self.SetAxis()
    if self.flag_axis: self.DrawAxis()
    if self.flag_logo: self.DrawLogo()
    if self.flag_leg:
      if self.n_value < 2: self.DrawLegend()
      elif self.n_value < 6: self.DrawColorBar()
    drawList = []
    drawValue = []
    drawStrValue = []
    fun_value = [self.nu.GetMajorDecayChannelNum, self.nu.GetStableOrNotNum, self.nu.GetLogTime, self.nu.GetBE, self.nu.GetSn, self.nu.GetSp, self.Zero]
    fun_strvalue = [self.nu.GetMajorDecayChannel, self.nu.GetMajorDecayChannel, self.nu.GetStringTime, self.nu.GetBE, self.nu.GetSn, self.nu.GetSp, self.StrZero]
    t_start = time.time()
    for z in range(self.z_min,self.z_max+1):
      for n in range(self.n_min,self.n_max+1):
        if self.nu.IsExist(z,n): # and (z,n) in mapData.keys(): 
          drawList.append((z, n))
          drawValue.append(fun_value[self.n_value](z,n))
          temp = fun_strvalue[self.n_value](z,n)
          if temp == None: 
            drawStrValue.append(temp)
            continue
          if self.n_value < 2:
            temp = str(temp).strip()
            if   temp == 'IS': temp = 'Stbl'
            elif temp == 'SF': temp = 'Fis.'
            elif temp == 'EC': temp = r'$e$-cap'
            elif temp == 'B-': temp = r'$\beta$-'
            elif temp == 'B+': temp = r'$\beta$+'
            elif temp == 'A':  temp = r'$\alpha$'
            else:
              temp = '$' + temp + '$'
            #temp = temp.encode('unicode_escape').decode() # to make it raw string
          elif self.n_value == 2:
            temp = str(temp).strip()
          else:
            temp = '%3.1e' % temp
          drawStrValue.append(temp)
    print('values append time: %f' % (time.time() - t_start))
    drawValue = np.array(drawValue)
    drawValue = np.where(drawValue == None, np.NaN, drawValue)
    
    if self.n_value > 1 and self.n_value < 6:
      max = np.nanmax(drawValue)
      min = np.nanmin(drawValue)
      drawValue = (drawValue[:] - min)/(max - min)
      if self.n_value == 2: # log lifetime
        self.cb.set_ticks([0,0.5,1],labels=['Untable', '%3.1e' % 10**((min+max)/2), 'Stable'], fontsize=6)
        self.cb.set_label('Lifetime [s]', loc='left', fontsize=6)
      else:
        labels = ['B.E. [keV/u]', 'Sn [keV]', 'Sp [keV]']
        self.cb.set_ticks([0,0.5,1],labels=['%3.1e' % x for x in [min, (min+max)/2, max]], fontsize=6)
        self.cb.set_label(labels[self.n_value-3], loc='left', fontsize=6)
    
    t_start = time.time()
    for (z, n, b) in self.bg:
      if z > self.z_max or z < self.z_min: continue
      if n > self.n_max or n < self.n_min: continue
      self.DrawBackground(n, z, b)   
    print('drawing bg time: %f' % (time.time() - t_start))

    t_start = time.time()
    for (z, n), c, cs in zip(drawList, drawValue, drawStrValue):
      self.DrawRect(n, z, c, self.nu.GetName(z,n), cs)
    print('drawing rect time: %f' % (time.time() - t_start))

    t_start = time.time()
    for i in range(self.n_hl):
      if not self.fl_hl[i]: continue
      for (z, n) in self.hl[i]:
        if z > self.z_max or z < self.z_min: continue
        if n > self.n_max or n < self.n_min: continue   
        self.DrawHighlights(n, z, self.nu.GetName(z,n), 
                            self.bg_col_hl[i], self.bd_col_hl[i], self.bd_wid_hl[i], self.ft_siz_hl[i], self.fl_name_hl[i]) 
    print('drawing highlights time: %f' % (time.time() - t_start))

    if self.flag_magic:
      self.DrawMagicLine()

    if not self.flagExt:
      plt.show()
      #fig.savefig('output.eps', format='eps')  
      #self.fig.savefig('output.png', format='png')  

  def LoadHighlights(self, file, hl_nucl: List):
    f = open(file)
    lines = f.readlines()
    f.close()
    
    for line in lines:
      nucls = [x.split('#')[0].strip() for x in line.strip().split(',')]
      save_a: List[int] = []
      for nucl in nucls:
        reg_single = re.fullmatch('\d+[a-zA-Z]+', nucl)
        reg_range  = re.fullmatch('(\d+)\-(\d+)([a-zA-Z]+)', nucl)
        reg_sing_d = re.fullmatch('\d+', nucl)
        reg_rang_d = re.fullmatch('(\d+)\-(\d+)', nucl)
        reg_zna    = re.fullmatch('(\d+)\s+(\d+)\s+(\d+)', nucl)
        if reg_single: # ex: 49Ca
          zn = self.nu.GetZN(nucl)
          if zn is not None:
            for a in save_a:
              hl_nucl.append((zn[0], a - zn[0]))
            hl_nucl.append((zn[0], zn[1]))  
        elif reg_range: # ex: 100-102Nb   
          for a in range(int(reg_range.group(1)),int(reg_range.group(2))+1):
            zn = self.nu.GetZN(str(a)+reg_range.group(3))
            if zn is not None: hl_nucl.append((zn[0], zn[1]))
        elif reg_sing_d: save_a.append(int(nucl))
        elif reg_rang_d:
          for a in range(int(reg_range.group(1)),int(reg_range.group(2))+1):
            save_a.append(a)
        elif reg_zna:
          hl_nucl.append((int(reg_zna.group(1)), int(reg_zna.group(2))))

  def ClearHighlights(self, hl_nucl: List): 
    hl_nucl.clear()

  def DrawHighlights(self, x, y, t, bg_col, bd_col, bd_width, ft_size, fl_name):
    fcol = col.to_rgba(bg_col)
    tcol = 'w' if col.rgb_to_hsv(fcol[:3])[2] < 0.5 else 'k'
    rectangle = patches.Rectangle((x-0.5,y-0.5), 1, 1, fc=fcol, ec=bd_col, lw=bd_width)
    self.ax.add_patch(rectangle)
    if fl_name:  
      VectorText(self.ax, x, y, t, size=ft_size, tcol=tcol, w='heavy')

  def LoadBackground(self, file):
    f = open(file)
    lines = f.readlines()
    f.close()
    
    for i in lines:
      if i.startswith('#'): continue # comments
      ispl = i.strip().split(',')
      if ispl[2] == 'bound': 
        self.bg.append((int(ispl[0]), int(ispl[1]), 1))        
      #else:                  bound = 0
      #self.bg.append((int(ispl[0]), int(ispl[1]), bound))
    
  def ClearBackground(self): self.bg = []

  def DrawBackground(self, x, y, b):
    fcol = col.to_rgba(self.bg1_col_bg if b == 1 else self.bg2_col_bg)
    rectangle = patches.Rectangle((x-0.5,y-0.5), 1, 1, fc=fcol, ec=self.border_color_bg, lw=self.border_width_bg)
    self.ax.add_patch(rectangle)

if __name__=="__main__":
  print("Run the test functions for nchart") 
  nc = nchart()
  nc.LoadHighlights('hl.txt')
  nc.flag_name = False
  nc.n_value = 6
  nc.DrawChart()
