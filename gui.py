import sys
import matplotlib
matplotlib.use('Qt5Agg')

from nchart import nchart

from PyQt6 import QtCore, QtWidgets, QtGui

from matplotlib.backends import backend_qtagg
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=5, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        print(self.fig.get_size_inches())
        print(self.fig.get_constrained_layout())
        print(self.fig.get_tight_layout())
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

        self.minZSB = QtWidgets.QSpinBox(); self.minZSB.setValue(0) ; self.minZSB.setRange(0,120)
        self.maxZSB = QtWidgets.QSpinBox(); self.maxZSB.setValue(10); self.maxZSB.setRange(0,120)
        self.minNSB = QtWidgets.QSpinBox(); self.minNSB.setValue(0) ; self.minNSB.setRange(0,300)
        self.maxNSB = QtWidgets.QSpinBox(); self.maxNSB.setValue(10); self.maxNSB.setRange(0,300)
        self.sortCB = QtWidgets.QComboBox(); self.sortCB.addItems(["Major Decay", "Stability", "Lifetime", "Binding E", "Sn", "Sp"]); self.sortCB.setCurrentIndex(0)
        self.nameCB = QtWidgets.QCheckBox('names'); self.nameCB.setChecked(True)
        self.valueCB = QtWidgets.QCheckBox('values'); self.valueCB.setChecked(True)
        self.axisCB = QtWidgets.QCheckBox('axis'); self.axisCB.setChecked(True)
        self.logoCB = QtWidgets.QCheckBox('logo'); self.logoCB.setChecked(True)
        self.fontSizeSB = QtWidgets.QDoubleSpinBox(); self.fontSizeSB.setValue(0.3); self.fontSizeSB.setRange(0,1); self.fontSizeSB.setSingleStep(0.1)
        self.colorPB = QtWidgets.QPushButton(); #self.colorPB.setDisabled(True); self.colorPB.setDown(True);#self.colorPB.setFlat(True); 
        self.colorPB.setStyleSheet('QPushButton { background-color: %s; }' % self.bg_col.name())
        self.colorPB.clicked.connect(self.showBGColorDialog)
        self.borderWidthSB = QtWidgets.QDoubleSpinBox(); self.borderWidthSB.setValue(0.1); self.borderWidthSB.setRange(0,10); self.borderWidthSB.setSingleStep(0.1)
                
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
                
        setLayout3 = QtWidgets.QHBoxLayout()
        setLayout3.addWidget(QtWidgets.QLabel("Font Size"))            
        setLayout3.addWidget(self.fontSizeSB)
        setLayout3.addWidget(QtWidgets.QLabel("Border Width"))            
        setLayout3.addWidget(self.borderWidthSB)
        setLayout3.addWidget(QtWidgets.QLabel("BG Color"))                
        setLayout3.addWidget(self.colorPB)
                
        setLayout = QtWidgets.QVBoxLayout()
        setLayout.addLayout(setLayout1)
        setLayout.addLayout(setLayout2)
        setLayout.addLayout(setLayout3)
        
        refButton = QtWidgets.QPushButton("&Refresh", self)
        refButton.clicked.connect(self.refresh)
        exitButton = QtWidgets.QPushButton("E&xit", self)
        exitButton.clicked.connect(exit)
        
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
        self.sc.nc.n_value = self.sortCB.currentIndex()
        
        self.sc.nc.font_size = self.fontSizeSB.value()
        self.sc.nc.border_width = self.borderWidthSB.value()
        self.sc.nc.bg_color = self.bg_col.name(QtGui.QColor.NameFormat.HexRgb)

        self.sc.nc.DrawChart()
        self.sc.draw()

    def showBGColorDialog(self):
        col = QtWidgets.QColorDialog.getColor()

        if col.isValid():
            self.bg_col = col
            self.colorPB.setStyleSheet('QPushButton { background-color: %s }' % self.bg_col.name())
            
app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
app.exec()