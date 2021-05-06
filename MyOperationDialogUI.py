# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI_OperationDialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class Ui_Dialog(object):
###
	def __init__(self, parent=None, Dialog = None, treeDict = None):

		self.initUI(Dialog, treeDict)
###
	def initUI(self, Dialog = None, treeDict = None):
		# Dialog.setWindowTitle("Operation Window")
		Dialog.resize(800, 600)
		self.label = QLabel()
		self.label_2 = QLabel()
		self.lineEdit = QLineEdit()
		self.textEdit = QTextEdit()
		self.pushButton = QPushButton()
		self.treeWidget = QTreeWidget()
		
		widget_main = QWidget()
		widget_main.resize(750,650)
		vboxlayout_main = QVBoxLayout()
		vboxlayout_main.addWidget(self.treeWidget)
		vboxlayout_main.addWidget(self.label)
		vboxlayout_main.addWidget(self.lineEdit)
		vboxlayout_main.addWidget(self.label_2)
		vboxlayout_main.addWidget(self.textEdit)
		vboxlayout_main.addWidget(self.pushButton)


		# self.widget.setGeometry(QtCore.QRect(550, 370, 239, 25))
		self.horizontalLayout = QHBoxLayout()
		self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
		self.buttonBox = QDialogButtonBox()
		self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
		self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
		self.horizontalLayout.addWidget(self.buttonBox)
		self.buttonBox_2 = QDialogButtonBox()
		self.buttonBox_2.setStandardButtons(QDialogButtonBox.Apply)
		self.horizontalLayout.addWidget(self.buttonBox_2)

		vboxlayout_main.addLayout(self.horizontalLayout)
		widget_main.setLayout(vboxlayout_main)
		widget_main.setParent(Dialog)

		self.buttonBox.accepted.connect(Dialog.accept)
		self.buttonBox.rejected.connect(Dialog.reject)
		QtCore.QMetaObject.connectSlotsByName(Dialog)

		self.treeWidget.setColumnCount(2)
		self.treeWidget.setHeaderLabels(['Label','Note'])
		self.treeWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)
		self.setUpTree(treeDict)


	def setUpTree(self, treeDict):
		for f in treeDict.keys():
			_file = treeDict[f]
			fileroot = QTreeWidgetItem(self.treeWidget)
			fileroot.setText(0, f)
			for testRoot in _file.values():
				fileroot.addChild(testRoot.clone())			
			self.treeWidget.addTopLevelItem(fileroot)
		self.treeWidget.expandAll()