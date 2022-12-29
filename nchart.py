import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as patches  
import matplotlib.cm as cm
import matplotlib.colors as col
import matplotlib.image as img
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib.colors import LinearSegmentedColormap

#mpl.rcParams['pdf.fonttype'] = 42
import numpy as np
from nudb import NuDB

col1 = ['#E725A6','#EA457C','#E39A82', '#75F075', '#333333', '#F0F075', '#75DBF0', '#35E9BC', '#759EF0', '#9475F0', '#B375F0']  
col2 = ['#EA457C', '#333333','#75DBF0']  
# returning 2n, n, B-, SF, IS, A, B+, EC, p, 2p, 3p
cmap1 = LinearSegmentedColormap.from_list('my_cmap1', col1, N=11)
cmap2 = LinearSegmentedColormap.from_list('my_cmap2', col2, N=3)
scalarMap1 = cm.ScalarMappable(col.Normalize(vmin=-4.5, vmax=6.5), cmap=cmap1)
scalarMap2 = cm.ScalarMappable(col.Normalize(vmin=-1.5, vmax=1.5), cmap=cmap2)
scalarMap3 = cm.ScalarMappable(col.Normalize(vmin=0, vmax=1), cmap='viridis')
smaps = [scalarMap1, scalarMap2, scalarMap3, scalarMap3]

class nchart:
  #############################################
  # input
  z_min, z_max = 10, 20
  n_min, n_max = 10, 24

  border_width = 0.1
  font_size = 5
  
  n_value = 0 
  # 0 = major decay pattern, 
  # 1 = stable or not (n, p-rich)
  # 2 = lifetime (log)
  # 3 = binding energy
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
    self.ax = self.fig.add_axes([0,0,1,1])     
    self.ax.spines['right'].set_visible(False)
    self.ax.spines['top'].set_visible(False)
    self.ax.yaxis.set_ticks_position('left')
    self.ax.xaxis.set_ticks_position('bottom')
    self.ax.axis('off')    
    
    self.ax.set_xlim([self.x_min-1,self.x_max+1])
    self.ax.set_ylim([self.y_min-1,self.y_max+1])    

  def DrawRect(self, x, y, z, t):
    fcol = smaps[self.n_value].to_rgba(z)
    (h, s, v) = col.rgb_to_hsv(fcol[:3])
    tcol = 'w' if v < 0.5 else 'k'
    rectangle = patches.Rectangle((x-0.5,y-0.5), 1, 1, fc=fcol, ec='black', lw=self.border_width)      
    self.ax.add_patch(rectangle)
    self.ax.text(x,y,t, ha='center', va='center', fontsize=self.font_size, color=tcol)
    ###### for database check ####
    #if (y,x) in mapData.keys(): 
    #  plt.text(x,y-0.45,'%s mb' % textConvert(mapData[(y,x)]), ha='center', va='bottom', fontsize='large', color=tcol)

  def DrawAxis(self):
    self.ax.add_patch(patches.FancyArrow(self.x_min, self.y_min, 0.2*self.x_width, 0, lw = 1, head_width = 0.2, fc = 'black'))
    self.ax.add_patch(patches.FancyArrow(self.x_min, self.y_min, 0, 0.2*self.y_width, lw = 1, head_width = 0.2, fc = 'black'))
    self.ax.text(self.x_min + 0.3*self.x_width, self.y_min, 'Neutrons', ha='center', va='center')
    self.ax.text(self.x_min, self.y_min + 0.3*self.y_width, 'Protons',  ha='center', va='center', rotation='vertical')
  
  def DrawLogo(self):
    self.ax_logo = self.fig.add_axes([0.93,0.95,0.05,0.05])  
    self.ax_logo.axis(False)
    logo = img.imread('logo.png')
    self.ax_logo.imshow(logo, aspect='equal')
    #, extent=(self.x_max-0.5, self.x_max+0.5, self.y_max-0.5, self.y_max+0.5), zorder=-1)
  
  def DrawLegend(self):
    self.ax_leg = self.fig.add_axes([0.0,0.8,0.2,0.2])
    self.ax_leg.axis(False)
    self.ax_leg.invert_yaxis()
    rectangle = patches.Rectangle((0-0.5, 0-0.5), 0.5, 0.5, fc='black', ec='black', lw=self.border_width)      
    self.ax_leg.add_patch(rectangle)
    rectangle = patches.Rectangle((0-0.5, 1-0.5), 0.5, 0.5, fc='black', ec='black', lw=self.border_width)      
    self.ax_leg.add_patch(rectangle)    
    self.ax_leg.text(3,0,'test', ha='center', va='center', fontsize=5)
    self.ax_leg.set_xlim([-1, 5])
    self.ax_leg.set_ylim([5, -1])        
    
  def DrawChart(self):
    self.SetParameters()
    self.SetAxis()
    self.DrawAxis()
    self.DrawLogo()
    self.DrawLegend()
    drawList = []
    drawValue = []
    fun_value = [self.nu.GetMajorDecayChannelNum, self.nu.GetStableOrNotNum, self.nu.GetLogTime, self.nu.GetBE]
    for z in range(self.z_min,self.z_max):
      for n in range(self.n_min,self.n_max):
        if self.nu.IsExist(z,n): # and (z,n) in mapData.keys(): 
          drawList.append((z, n))
          drawValue.append(fun_value[self.n_value](z,n))
    drawValue = np.array(drawValue)

    if self.n_value > 1:
      drawValue = (drawValue[:] - drawValue[:].min())/(drawValue[:].max() - drawValue[:].min())
    for (z, n), c in zip(drawList, drawValue):
      self.DrawRect(n, z, c, self.nu.GetName(z,n))

    if not self.flagExt:
      #plt.show()
      #fig.savefig('output.eps', format='eps')  
      self.fig.savefig('output.png', format='png')  
    
    
if __name__=="__main__":
  print("Run the test functions for nchart")
  nc = nchart()
  nc.DrawChart()