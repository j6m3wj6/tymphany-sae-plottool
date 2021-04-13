from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import (QMainWindow, QApplication, QWidget, QFileDialog, QTextEdit, 
  QPushButton, QLabel, QVBoxLayout, QTreeWidget, QTreeWidgetItem, QMenuBar, QMenu)
import numpy as np, pandas as pd
import sys, os
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib import pyplot as plt
import mplcursors

class MplCanvas(FigureCanvasQTAgg):
  def __init__(self, parent=None):
    # Canvas init
    fig = Figure()
    fig.canvas.mpl_connect('button_press_event', self.onclick)
    self.ax = fig.add_subplot(111)
    self._setStyle()
    super(MplCanvas, self).__init__(fig)

  def _setStyle(self):
    # axes' style
    self.ax.set_xscale('log')
    self.ax.set_xlim([20,20000])
    self.ax.set_ylim(auto=True)
    self.ax.grid()
    self.ax.grid(which='minor', linestyle=':', linewidth='0.5', color='black')

  # handle mouse onclick event
  def onclick(self,event):
    print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
        ('double' if event.dblclick else 'single', event.button,
        event.x, event.y, event.xdata, event.ydata))

class PlotGraph(QWidget):
  """Widget for visualize data"""
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.initUI()
# User Interface
  def initUI(self):
    self._createButton()
    self._createCanvas()
    self._createTreeList()

    layout = QVBoxLayout()
    layout.addWidget(self.button1)
    layout.addWidget(self.toolbar)
    layout.addWidget(self.canvas)
    layout.addWidget(self.tree)
    self.setLayout(layout)
  
  def _createButton(self):
    self.button1 = QPushButton('Upload data')
    self.button1.clicked.connect(self.plotData)

  def _createCanvas(self):
    self.canvas = MplCanvas(self)
    self.toolbar = NavigationToolbar(self.canvas, self)

  def _createTreeList(self):
    self.tree=QTreeWidget()
    self.tree.setColumnCount(2)
    self.tree.setHeaderLabels(['Key','Value'])
    self.tree.setColumnWidth(0,150)
    self.tree.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
    self.tree.itemClicked.connect(self.printItemText)
    self.tree.expandAll()

# Functions
  def printItemText(self):
    items = self.tree.selectedItems()
    x = []
    for i in range(len(items)):
      if (items[i].parent()):
        x.append(str(items[i].parent().text(0) + ' - ' + items[i].text(0)))
      else:
        x.append(items[i].text(0))
    print (self.tree.currentIndex().row(), '. ', x)

  def appendChildonTree(self):
    root=QTreeWidgetItem(self.tree)
    root.setText(0,'Curve')
    for i in range(len(self.data.columns)):
      child=QTreeWidgetItem()
      child.setText(0,self.data.columns[i])
      child.setCheckState(0, 2)
      root.addChild(child)
    self.tree.addTopLevelItem(root)

  def get_text_file(self):
    dialog = QFileDialog()
    dialog.setFileMode(QFileDialog.AnyFile)
    dialog.setFilter(QtCore.QDir.Files)

    if dialog.exec_():
      file_name = dialog.selectedFiles()

      if file_name[0].endswith('.txt'):
        with open(file_name[0], 'r', encoding='UTF-8') as file:
          
          headers = file.readlines()[:3]
          print(headers[0])
          title = headers[0]
          curves = headers[1].split('\t\t')
          curves = [c.replace('"', '').strip() for c in curves]
          
          dtbl = pd.read_table(file_name[0],  skiprows=2)
          freq = dtbl.iloc[:, 0]
          freq = [float(f.replace(',', '').strip()) for f in freq]
          dtbl = dtbl.iloc[:, [i%2==1 for i in range(len(dtbl.columns))]]
          dtbl.columns = curves
          
          dtbl['Frequency'] = freq
          file.close()
          return dtbl
      else:
        pass

  def plotData(self):
    self.data = self.get_text_file()
    print(self.data)

    for col in self.data.columns[:-1]:
      line, = self.canvas.ax.plot(self.data["Frequency"], self.data[col], label=col)
      # self.canvas.lines.append(line)
    # mplcursors.cursor(self.canvas.ax.lines, highlight=True, highlight_kwargs=dict(linewidth=5))
    self.canvas.ax.legend(loc='lower left')
    # self.data.plot("Frequency", ax = self.canvas.ax)
    self.canvas.draw()
    self.appendChildonTree()

  
    

class MyApp(QMainWindow):
  """App's Main Window."""
  def __init__(self, parent=None):
    """Initializer."""
    super().__init__(parent)
    self.initUI()

  def initUI(self):  
    self.setWindowTitle("Python Menus & Toolbars")
    self.resize(800, 600)
    self.setCentralWidget(PlotGraph())
    self._createMenuBar()


  def _createMenuBar(self):
    menuBar = QMenuBar(self)
    # Creating menus using a QMenu object
    fileMenu = QMenu("&File", self)
    menuBar.addMenu(fileMenu)
    # Creating menus using a title
    editMenu = menuBar.addMenu("&Edit")
    helpMenu = menuBar.addMenu("&Help")
    self.setMenuBar(menuBar)



def main():
  app = QApplication(sys.argv)
  #main = PlotGraph()
  main = MyApp()
  main.show()
  sys.exit(app.exec_())

if __name__ == '__main__':
    main()

