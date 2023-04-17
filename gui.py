import sys
import matplotlib
matplotlib.use('Qt5Agg')

from typing import List
from nchart import nchart

from PyQt6 import QtCore, QtWidgets, QtGui

from matplotlib.backends import backend_qtagg
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=4, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        #self.axes = fig.add_subplot(111, frameon = False)
        self.nc = nchart(self.fig)    
        super(MplCanvas, self).__init__(self.fig)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle('nchart')
        
        # Create the maptlotlib FigureCanvas object,
        # which defines a single set of axes as self.axes.
        self.sc = MplCanvas(self, width=6, height=6, dpi=100)
        #sc.axes.plot([0,1,2,3,4], [10,1,20,3,40])
        # Create toolbar, passing canvas as first parament, parent (self, the MainWindow) as second.
        toolbar = NavigationToolbar(self.sc, self)
        self.bg_col = QtGui.QColor('#FFFFFF')
        
        self.mg_ln_col = QtGui.QColor('#FF26A5')
        self.mg_ft_col = QtGui.QColor('#000000')

        self.n_hl = 4
        self.hl_bd_col: List[QtGui.QColor] = []
        self.hl_bg_col: List[QtGui.QColor] = []
        self.hl_flname: List[str] = []
        for i in range(self.n_hl):
            self.hl_bd_col.append(QtGui.QColor('#000000'))
            self.hl_bg_col.append(QtGui.QColor('#FFFFFF'))
            self.hl_flname.append('')
        self.hl_bg_col = [ QtGui.QColor('#ff5255'), QtGui.QColor('#ffef74'), QtGui.QColor('#4a71ff'), QtGui.QColor('#aaff7f') ]

        self.bg_border_col = QtGui.QColor('#000000')
        self.bgfilename = 'background.txt'
        self.bg_bg1_col = QtGui.QColor('#DDDDDD')
        self.bg_bg2_col = QtGui.QColor('#DDDDDD')
        self.hl_flname[0] = 'C:/Users/IBS/iCloudDrive/Work/codes/nchart/hl_na.txt'
        self.hl_flname[1] = 'C:/Users/IBS/iCloudDrive/Work/codes/nchart/hl_nr.txt'
        self.hl_flname[2] = 'C:/Users/IBS/iCloudDrive/Work/codes/nchart/hl_ns.txt'
        self.hl_flname[3] = 'C:/Users/IBS/iCloudDrive/Work/codes/nchart/hl_nt.txt'
        
        self.minZSB = QtWidgets.QSpinBox(); self.minZSB.setValue(0) ; self.minZSB.setRange(0,120)
        self.maxZSB = QtWidgets.QSpinBox(); self.maxZSB.setValue(20); self.maxZSB.setRange(0,120)
        self.minNSB = QtWidgets.QSpinBox(); self.minNSB.setValue(0) ; self.minNSB.setRange(0,300)
        self.maxNSB = QtWidgets.QSpinBox(); self.maxNSB.setValue(40); self.maxNSB.setRange(0,300)
        self.sortCB = QtWidgets.QComboBox(); self.sortCB.addItems(["Major Decay", "Stability", "Lifetime", "Binding E", "Sn", "Sp", "No Color"]); self.sortCB.setCurrentIndex(1)
        self.nameCB = QtWidgets.QCheckBox('names'); self.nameCB.setChecked(False)
        self.valueCB = QtWidgets.QCheckBox('values'); self.valueCB.setChecked(False)
        self.axisCB = QtWidgets.QCheckBox('axis'); self.axisCB.setChecked(False)
        self.logoCB = QtWidgets.QCheckBox('logo'); self.logoCB.setChecked(False)
        self.legCB = QtWidgets.QCheckBox('legend'); self.legCB.setChecked(False)
        self.fontSizeSB = QtWidgets.QDoubleSpinBox(); self.fontSizeSB.setValue(0.3); self.fontSizeSB.setRange(0,1); self.fontSizeSB.setSingleStep(0.05)
        self.colorPB = QtWidgets.QPushButton(); #self.colorPB.setDisabled(True); self.colorPB.setDown(True);#self.colorPB.setFlat(True); 
        self.colorPB.setStyleSheet('QPushButton { background-color: %s; }' % self.bg_col.name())
        self.colorPB.clicked.connect(lambda: self.showColorDialog(self.bg_col, self.colorPB))
        self.borderWidthSB = QtWidgets.QDoubleSpinBox(); self.borderWidthSB.setValue(0); self.borderWidthSB.setRange(0,10); self.borderWidthSB.setSingleStep(0.1)

        self.magicCB = QtWidgets.QCheckBox('Magic #'); self.magicCB.setChecked(True)
        self.magicWidthSB = QtWidgets.QDoubleSpinBox(); self.magicWidthSB.setValue(0.5); self.magicWidthSB.setRange(0,10); self.magicWidthSB.setSingleStep(0.1)
        self.magicLineColorPB = QtWidgets.QPushButton(); self.magicLineColorPB.setStyleSheet('QPushButton { background-color: %s; }' % self.mg_ln_col.name())
        self.magicLineColorPB.clicked.connect(lambda: self.showColorDialog(self.mg_ln_col, self.magicLineColorPB))
        self.magicFontColorPB = QtWidgets.QPushButton(); self.magicFontColorPB.setStyleSheet('QPushButton { background-color: %s; }' % self.mg_ft_col.name())
        self.magicFontColorPB.clicked.connect(lambda: self.showColorDialog(self.mg_ft_col, self.magicFontColorPB))        
        self.magicFontSizeSB = QtWidgets.QDoubleSpinBox(); self.magicFontSizeSB.setValue(2); self.magicFontSizeSB.setRange(0,10); self.magicFontSizeSB.setSingleStep(0.05)

        self.hlFlagCB: List[QtWidgets.QCheckBox] = []
        self.hlfileLE: List[QtWidgets.QLineEdit] = []
        self.hlfilePB: List[QtWidgets.QPushButton] = []
        self.hlfileclPB: List[QtWidgets.QPushButton] = []
        self.hlNameCB: List[QtWidgets.QCheckBox] = []
        self.hlFontSizeSB: List[QtWidgets.QDoubleSpinBox] = []
        self.hlBorderWidthSB: List[QtWidgets.QDoubleSpinBox] = []
        self.hlBorderColorPB: List[QtWidgets.QPushButton] = []
        self.hlBGColorPB: List[QtWidgets.QPushButton] = []
        self.hlBGAlphaSB: List[QtWidgets.QDoubleSpinBox] = []
        for i in range(self.n_hl):
            self.hlFlagCB.append(QtWidgets.QCheckBox('Highlights %d' % (i+1))); self.hlFlagCB[i].setChecked(True)
            self.hlfileLE.append(QtWidgets.QLineEdit()); self.hlfileLE[i].setModified(False); self.hlfileLE[i].setText(self.hl_flname[i])
            self.hlfilePB.append(QtWidgets.QPushButton('Load')); self.hlfilePB[i].clicked.connect(lambda state, x=i: self.showHLFileDialog(x))
            self.hlfileclPB.append(QtWidgets.QPushButton('Clear')); self.hlfileclPB[i].clicked.connect(lambda state, x=i: self.hlfileClear(x))
            self.hlNameCB.append(QtWidgets.QCheckBox('names')); self.hlNameCB[i].setChecked(False)
            self.hlFontSizeSB.append(QtWidgets.QDoubleSpinBox()); self.hlFontSizeSB[i].setValue(0.); self.hlFontSizeSB[i].setRange(0,1); self.hlFontSizeSB[i].setSingleStep(0.05)
            self.hlBorderWidthSB.append(QtWidgets.QDoubleSpinBox()); self.hlBorderWidthSB[i].setValue(0); self.hlBorderWidthSB[i].setRange(0,10); self.hlBorderWidthSB[i].setSingleStep(0.1)
            self.hlBorderColorPB.append(QtWidgets.QPushButton()); self.hlBorderColorPB[i].setStyleSheet('QPushButton { background-color: %s; }' % self.hl_bd_col[i].name())
            self.hlBorderColorPB[i].clicked.connect(lambda state, x=i: self.showColorDialog(self.hl_bd_col[x], self.hlBorderColorPB[x]))        
            self.hlBGColorPB.append(QtWidgets.QPushButton()); self.hlBGColorPB[i].setStyleSheet('QPushButton { background-color: %s; }' % self.hl_bg_col[i].name())
            self.hlBGColorPB[i].clicked.connect(lambda state, x=i: self.showColorDialog(self.hl_bg_col[x], self.hlBGColorPB[x]))         
            self.hlBGAlphaSB.append(QtWidgets.QDoubleSpinBox()); self.hlBGAlphaSB[i].setValue(1); self.hlBGAlphaSB[i].setRange(0,1); self.hlBGAlphaSB[i].setSingleStep(0.1)

        self.bgfileLE = QtWidgets.QLineEdit(); self.bgfileLE.setModified(False); self.bgfileLE.setText(self.bgfilename)
        self.bgfilePB = QtWidgets.QPushButton('Load'); self.bgfilePB.clicked.connect(self.showBGFileDialog)
        self.bgfileclPB = QtWidgets.QPushButton('Clear'); self.bgfileclPB.clicked.connect(self.bgfileClear)
        self.bgBorderWidthSB = QtWidgets.QDoubleSpinBox(); self.bgBorderWidthSB.setValue(0.0); self.bgBorderWidthSB.setRange(0,10); self.bgBorderWidthSB.setSingleStep(0.1)
        self.bgBorderColorPB = QtWidgets.QPushButton(); self.bgBorderColorPB.setStyleSheet('QPushButton { background-color: %s; }' % self.bg_border_col.name())
        self.bgBorderColorPB.clicked.connect(lambda: self.showColorDialog(self.bg_border_col, self.bgBorderColorPB))        
        self.bgBG1ColorPB = QtWidgets.QPushButton(); self.bgBG1ColorPB.setStyleSheet('QPushButton { background-color: %s; }' % self.bg_bg1_col.name())
        self.bgBG1ColorPB.clicked.connect(lambda: self.showColorDialog(self.bg_bg1_col, self.bgBG1ColorPB))  
        self.bgBG2ColorPB = QtWidgets.QPushButton(); self.bgBG2ColorPB.setStyleSheet('QPushButton { background-color: %s; }' % self.bg_bg2_col.name())
        self.bgBG2ColorPB.clicked.connect(lambda: self.showColorDialog(self.bg_bg2_col, self.bgBG2ColorPB))    
        self.bgBGAlphaSB = QtWidgets.QDoubleSpinBox(); self.bgBGAlphaSB.setValue(1); self.bgBGAlphaSB.setRange(0,1); self.bgBGAlphaSB.setSingleStep(0.1)

        setLayout1 = QtWidgets.QHBoxLayout()
        setLayout1.addWidget(QtWidgets.QLabel("Min. Z"))
        setLayout1.addWidget(self.minZSB)
        setLayout1.addWidget(QtWidgets.QLabel("Max. Z"))     
        setLayout1.addWidget(self.maxZSB)
        setLayout1.addWidget(QtWidgets.QLabel("Min. N"))        
        setLayout1.addWidget(self.minNSB)
        setLayout1.addWidget(QtWidgets.QLabel("Max. N"))        
        setLayout1.addWidget(self.maxNSB)

        setLayout2 = QtWidgets.QHBoxLayout()
        setLayout2.addWidget(QtWidgets.QLabel("Coloring"))            
        setLayout2.addWidget(self.sortCB)
        setLayout2.addWidget(self.nameCB)
        setLayout2.addWidget(self.valueCB)
        setLayout2.addWidget(self.axisCB)
        setLayout2.addWidget(self.logoCB)
        setLayout2.addWidget(self.legCB)
                
        setLayout3 = QtWidgets.QHBoxLayout()
        setLayout3.addWidget(QtWidgets.QLabel("Font Size"))            
        setLayout3.addWidget(self.fontSizeSB)
        setLayout3.addWidget(QtWidgets.QLabel("Border Width"))            
        setLayout3.addWidget(self.borderWidthSB)
        setLayout3.addWidget(QtWidgets.QLabel("BG Color"))                
        setLayout3.addWidget(self.colorPB)

        setLayout4 = QtWidgets.QHBoxLayout()
        setLayout4.addWidget(self.magicCB)
        setLayout4.addWidget(QtWidgets.QLabel("Line Color"))             
        setLayout4.addWidget(self.magicLineColorPB)
        setLayout4.addWidget(QtWidgets.QLabel("Line Width"))            
        setLayout4.addWidget(self.magicWidthSB)
        setLayout4.addWidget(QtWidgets.QLabel("Font Color"))             
        setLayout4.addWidget(self.magicFontColorPB)        
        setLayout4.addWidget(QtWidgets.QLabel("Font Size"))                
        setLayout4.addWidget(self.magicFontSizeSB)

        hlLayouts: List[QtWidgets.QHBoxLayout] = []
        for i in range(self.n_hl):
            hlLayouts.append(QtWidgets.QHBoxLayout())
            hlLayouts[i].addWidget(self.hlFlagCB[i])         
            hlLayouts[i].addWidget(self.hlfileLE[i])
            hlLayouts[i].addWidget(self.hlfilePB[i])
            hlLayouts[i].addWidget(self.hlfileclPB[i])
            hlLayouts[i].addWidget(self.hlNameCB[i])
            hlLayouts[i].addWidget(QtWidgets.QLabel("Font Size"))            
            hlLayouts[i].addWidget(self.hlFontSizeSB[i])
            hlLayouts[i].addWidget(QtWidgets.QLabel("Border Width"))            
            hlLayouts[i].addWidget(self.hlBorderWidthSB[i])        
            hlLayouts[i].addWidget(QtWidgets.QLabel("Border Color"))                
            hlLayouts[i].addWidget(self.hlBorderColorPB[i])
            hlLayouts[i].addWidget(QtWidgets.QLabel("Cell Color"))     
            hlLayouts[i].addWidget(self.hlBGColorPB[i])
            hlLayouts[i].addWidget(QtWidgets.QLabel("Opacity")) 
            hlLayouts[i].addWidget(self.hlBGAlphaSB[i])

        setLayout5 = QtWidgets.QHBoxLayout()
        setLayout5.addWidget(QtWidgets.QLabel("Background"))            
        setLayout5.addWidget(self.bgfileLE)
        setLayout5.addWidget(self.bgfilePB)
        setLayout5.addWidget(self.bgfileclPB)
        setLayout5.addWidget(QtWidgets.QLabel("Border Width"))            
        setLayout5.addWidget(self.bgBorderWidthSB)        
        setLayout5.addWidget(QtWidgets.QLabel("Border Color"))                
        setLayout5.addWidget(self.bgBorderColorPB)
        setLayout5.addWidget(QtWidgets.QLabel("Cell Color 1"))     
        setLayout5.addWidget(self.bgBG1ColorPB)
        setLayout5.addWidget(QtWidgets.QLabel("Cell Color 2"))     
        setLayout5.addWidget(self.bgBG2ColorPB)        
        setLayout5.addWidget(QtWidgets.QLabel("Opacity")) 
        setLayout5.addWidget(self.bgBGAlphaSB)

        setLayout = QtWidgets.QVBoxLayout()
        setLayout.addLayout(setLayout1)
        setLayout.addLayout(setLayout2)
        setLayout.addLayout(setLayout3)
        setLayout.addLayout(setLayout4)
        for layout in hlLayouts:
            setLayout.addLayout(layout)
        setLayout.addLayout(setLayout5)

        refButton = QtWidgets.QPushButton("&Refresh", self)
        refButton.clicked.connect(self.refresh)
        exitButton = QtWidgets.QPushButton("E&xit", self)
        exitButton.clicked.connect(sys.exit)
        
        buttonLayout = QtWidgets.QHBoxLayout()
        buttonLayout.addWidget(refButton)
        buttonLayout.addWidget(exitButton)
        
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addLayout(setLayout)
        layout.addLayout(buttonLayout)
        layout.addWidget(self.sc)

        # Create a placeholder widget to hold our toolbar and canvas.
        widget = QtWidgets.QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.show()
        self.refresh()
        

    def refresh(self):
        self.sc.fig.clear()
        
        self.sc.nc.z_min = self.minZSB.value()
        self.sc.nc.z_max = self.maxZSB.value()
        self.sc.nc.n_min = self.minNSB.value()
        self.sc.nc.n_max = self.maxNSB.value()
        
        self.sc.nc.flag_name = self.nameCB.isChecked()
        self.sc.nc.flag_value = self.valueCB.isChecked()
        self.sc.nc.flag_axis = self.axisCB.isChecked()
        self.sc.nc.flag_logo = self.logoCB.isChecked()
        self.sc.nc.flag_leg  = self.legCB.isChecked()
        self.sc.nc.n_value = self.sortCB.currentIndex()
        
        self.sc.nc.font_size = self.fontSizeSB.value()
        self.sc.nc.border_width = self.borderWidthSB.value()
        self.sc.nc.bg_color = self.bg_col.name(QtGui.QColor.NameFormat.HexRgb)

        self.sc.nc.flag_magic = self.magicCB.isChecked()
        self.sc.nc.wid_mg = self.magicWidthSB.value()
        self.sc.nc.ln_col_mg = self.mg_ln_col.getRgbF()
        self.sc.nc.ft_col_mg = self.mg_ft_col.getRgbF()
        self.sc.nc.txt_mg = self.magicFontSizeSB.value()

        for i in range(self.n_hl):
            self.sc.nc.fl_hl[i] = self.hlFlagCB[i].isChecked()
            self.sc.nc.ClearHighlights(self.sc.nc.hl[i])
            if self.hl_flname[i]: 
                self.sc.nc.LoadHighlights(self.hl_flname[i], self.sc.nc.hl[i])           
            self.sc.nc.fl_name_hl[i] = self.hlNameCB[i].isChecked()
            self.sc.nc.bd_wid_hl[i]  = self.hlBorderWidthSB[i].value()
            self.sc.nc.ft_siz_hl[i]  = self.hlFontSizeSB[i].value()
            self.sc.nc.bd_col_hl[i]  = self.hl_bd_col[i].name(QtGui.QColor.NameFormat.HexRgb)
            self.hl_bg_col[i].setAlphaF(self.hlBGAlphaSB[i].value())
            self.sc.nc.bg_col_hl[i]  = self.hl_bg_col[i].getRgbF()

        self.sc.nc.ClearBackground()
        if self.bgfilename: self.sc.nc.LoadBackground(self.bgfilename)
            
        self.sc.nc.border_width_bg = self.bgBorderWidthSB.value()
        self.sc.nc.border_color_bg = self.bg_border_col.name(QtGui.QColor.NameFormat.HexRgb)

        self.bg_bg1_col.setAlphaF(self.bgBGAlphaSB.value())
        self.bg_bg2_col.setAlphaF(self.bgBGAlphaSB.value())
        self.sc.nc.bg1_col_bg = self.bg_bg1_col.getRgbF()
        self.sc.nc.bg2_col_bg = self.bg_bg2_col.getRgbF()

        self.sc.nc.DrawChart()
        self.sc.draw()

    def showColorDialog(self, col_saved: QtGui.QColor, wid: QtWidgets.QPushButton):
        col = QtWidgets.QColorDialog.getColor()
        if not col.isValid(): return
        col_saved.setRgb(*col.getRgb())
        wid.setStyleSheet('QPushButton { background-color: %s }' % col.name())

    def showHLFileDialog(self, i):
        fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', './')
        if fname[0]:
            self.hl_flname[i] = fname[0]
            self.hlfileLE[i].setText(self.hl_flname[i])
            
    def hlfileClear(self, i):
        self.hl_flname[i] = ''
        self.hlfileLE[i].setText(self.hl_flname[i])
        
    def showBGFileDialog(self):
        fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', './')
        if fname[0]:
            self.bgfilename = fname[0]
            self.bgfileLE.setText(self.bgfilename)
            
    def bgfileClear(self):
        self.bgfilename = ''
        self.bgfileLE.setText(self.bgfilename)
        
app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
app.exec()
