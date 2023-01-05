import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as patches  
import matplotlib.cm as cm
import matplotlib.colors as col
import matplotlib.image as img
from matplotlib.textpath import TextPath
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.transforms as trans

#mpl.rcParams['pdf.fonttype'] = 42
import numpy as np
from nudb import NuDB

col1 = ['#E725A6','#EA457C','#E39A82', '#75F075', '#333333', '#F0F075', '#75DBF0', '#35E9BC', '#759EF0', '#9475F0', '#B375F0'] 
leg1 = [r'$2n$', r'$n$', r'$\beta -$', 'Fission', 'Stable', r'$\alpha$', r'$\beta +$', r'$e$-capture', r'$p$', r'$2p$', r'$3p$']
col2 = ['#EA457C', '#333333','#75DBF0']
leg2 = [r'$n$-rich', 'Stable', r'$p$-rich']
# returning 2n, n, B-, SF, IS, A, B+, EC, p, 2p, 3p
cmap1 = LinearSegmentedColormap.from_list('my_cmap1', col1, N=11)
cmap2 = LinearSegmentedColormap.from_list('my_cmap2', col2, N=3)
scalarMap1 = cm.ScalarMappable(col.Normalize(vmin=-4.5, vmax=6.5), cmap=cmap1)
scalarMap2 = cm.ScalarMappable(col.Normalize(vmin=-1.5, vmax=1.5), cmap=cmap2)
scalarMap3 = cm.ScalarMappable(col.Normalize(vmin=0, vmax=1), cmap='viridis')
smaps = [scalarMap1, scalarMap2, scalarMap3, scalarMap3, scalarMap3, scalarMap3]

def VectorText(ax, x, y, t, size, tcol, ha='center', va='center', rotation=None):
  path1 = TextPath((0, 0), t, size=size)
  x0, y0 = np.amin(np.array(path1.vertices), axis=0)
  x1, y1 = np.amax(np.array(path1.vertices), axis=0)
  tr2d = trans.Affine2D()
  if ha == 'center':  x_tr = -(x1-x0)/2
  elif ha == 'right': x_tr = -(x1-x0)
  else:               x_tr = 0
  if va == 'center':  y_tr = -(y1-y0)/2
  elif va == 'right': y_tr = -(y1-y0)
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
  z_min, z_max = 10, 20
  n_min, n_max = 10, 24

  border_width = 0.1
  font_size = 0.3
  
  flag_name = True
  flag_value = False
  flag_axis = True
  flag_logo = True
  
  bg_color = '#ffffff'
  
  n_value = 0 
  # 0 = major decay pattern, 
  # 1 = stable or not (n, p-rich)
  # 2 = lifetime (log)
  # 3 = binding energy
  # 4 = Sn
  # 5 = Sp
  #############################################

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

  def ConvText(self, val):
    s = '%.0e' % val
    d = int(s[0])
    c = int(s[-3:])
    return '%1dx10$^{%1d}$' % (d, c)

  def SetParameters(self):
    self.x_min, self.x_max = self.n_min - 1, self.n_max + 1
    self.y_min, self.y_max = self.z_min - 1, self.z_max + 1
    self.x_width = self.x_max - self.x_min
    self.y_width = self.y_max - self.y_min

  def SetAxis(self):
    self.fig.set_facecolor(self.bg_color)
        
    self.ax = self.fig.add_axes([0,0,1,1])
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
    print(self.ax_leg.yaxis_inverted())
      
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
    if self.n_value < 2: self.DrawLegend()
    else:                self.DrawColorBar()
    drawList = []
    drawValue = []
    drawStrValue = []
    fun_value = [self.nu.GetMajorDecayChannelNum, self.nu.GetStableOrNotNum, self.nu.GetLogTime, self.nu.GetBE, self.nu.GetSn, self.nu.GetSp]
    fun_strvalue = [self.nu.GetMajorDecayChannel, self.nu.GetMajorDecayChannel, self.nu.GetStringTime, self.nu.GetBE, self.nu.GetSn, self.nu.GetSp]
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
                      
    drawValue = np.array(drawValue)
    drawValue = np.where(drawValue == None, np.NaN, drawValue)
    
    if self.n_value > 1:
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

                      
    for (z, n), c, cs in zip(drawList, drawValue, drawStrValue):
      self.DrawRect(n, z, c, self.nu.GetName(z,n), cs)

    if not self.flagExt:
      plt.show()
      #fig.savefig('output.eps', format='eps')  
      #self.fig.savefig('output.png', format='png')  
    
    
if __name__=="__main__":
  print("Run the test functions for nchart") 
  nc = nchart()
  nc.DrawChart()