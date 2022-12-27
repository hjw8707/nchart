import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as patches  
import matplotlib.cm as cm
import matplotlib.colors as col
#mpl.rcParams['pdf.fonttype'] = 42
import numpy as np
from nudb import NuDB

scalarMap = cm.ScalarMappable(col.Normalize(vmin=-4, vmax=6), 'tab10')

class nchart:
  #############################################
  # input
  z_min, z_max = 10, 20
  n_min, n_max = 10, 24

  border_width = 0.1
  font_size = 5
  #############################################

  def __init__(self, ax = 0): # ax should be 'axes' for matplotlib
    ###########################################
    # Load matplotlib
    self.fig = plt.figure()
    if ax == 0:
      self.flagExt = False
      self.ax = self.fig.add_subplot()
    else:
      self.flagExt = True
      self.ax = ax
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
    self.ax.spines['right'].set_visible(False)
    self.ax.spines['top'].set_visible(False)
    self.ax.yaxis.set_ticks_position('left')
    self.ax.xaxis.set_ticks_position('bottom')
    self.ax.axis('off')    
    
    self.ax.set_xlim([self.x_min-1,self.x_max+1])
    self.ax.set_ylim([self.y_min-1,self.y_max+1])    

  def DrawRect(self, x, y, z, t):
    fcol = scalarMap.to_rgba(z)
    (h, s, v) = col.rgb_to_hsv(fcol[:3])
    tcol = 'w' if h > 0.5 else 'k'
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
    
  def DrawChart(self):
    self.SetParameters()
    self.SetAxis()
    self.DrawAxis()
    drawList = []
    drawValue = []
    for z in range(self.z_min,self.z_max):
      for n in range(self.n_min,self.n_max):
        if self.nu.IsExist(z,n): # and (z,n) in mapData.keys(): 
          drawList.append((z, n))
    #      drawValue.append(nuBE(z,n))
    #      drawValue.append(nuLogTime(z,n))
          drawValue.append(self.nu.GetMajorDecayChannelNum(z,n))
    #      drawValue.append(nuMajorStableOrNotNum(z,n))
    drawValue = np.array(drawValue)

    #drawValue = (drawValue[:] - drawValue[:].min())/(drawValue[:].max() - drawValue[:].min())
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