# -*- coding: utf-8 -*-
import iFruitFly_Testing_weka as ITW

# Form implementation generated from reading ui file 'input.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import ntpath 
import os

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):

        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.setWindowModality(QtCore.Qt.WindowModal)
        MainWindow.resize(800, 529)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("table.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setEnabled(True)
        self.tabWidget.setTabPosition(QtGui.QTabWidget.North)
        self.tabWidget.setTabShape(QtGui.QTabWidget.Rounded)
        self.tabWidget.setDocumentMode(False)
        self.tabWidget.setTabsClosable(False)
        self.tabWidget.setMovable(False)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tabTesting = QtGui.QWidget()
        self.tabTesting.setObjectName(_fromUtf8("tabTesting"))
        self.gridLayout_3 = QtGui.QGridLayout(self.tabTesting)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.btnProcess = QtGui.QPushButton(self.tabTesting)
        self.btnProcess.setObjectName(_fromUtf8("btnProcess"))
        self.gridLayout_2.addWidget(self.btnProcess, 4, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 1, 3, 1, 1)
        self.imgProcess = QtGui.QLabel(self.tabTesting)
        self.imgProcess.setFrameShape(QtGui.QFrame.StyledPanel)
        self.imgProcess.setFrameShadow(QtGui.QFrame.Sunken)
        self.imgProcess.setLineWidth(2)
        self.imgProcess.setText(_fromUtf8(""))
        self.imgProcess.setPixmap(QtGui.QPixmap(_fromUtf8(":/img/preview.jpeg")))
        self.imgProcess.setScaledContents(True)
        self.imgProcess.setAlignment(QtCore.Qt.AlignCenter)
        self.imgProcess.setObjectName(_fromUtf8("imgProcess"))
        self.gridLayout_2.addWidget(self.imgProcess, 1, 5, 1, 3)
        self.OutputFolder = QtGui.QPushButton(self.tabTesting)
        self.OutputFolder.setObjectName(_fromUtf8("OutputFolder"))
        self.gridLayout_2.addWidget(self.OutputFolder, 4, 6, 1, 1)
        self.Output = QtGui.QPushButton(self.tabTesting)
        self.Output.setObjectName(_fromUtf8("Output"))
        self.gridLayout_2.addWidget(self.Output, 4, 5, 1, 1)
        self.imgPreview = QtGui.QLabel(self.tabTesting)
        self.imgPreview.setFrameShape(QtGui.QFrame.StyledPanel)
        self.imgPreview.setFrameShadow(QtGui.QFrame.Sunken)
        self.imgPreview.setLineWidth(2)
        self.imgPreview.setText(_fromUtf8(""))
        self.imgPreview.setPixmap(QtGui.QPixmap(_fromUtf8(":/img/preview.jpeg")))
        self.imgPreview.setScaledContents(True)
        self.imgPreview.setAlignment(QtCore.Qt.AlignCenter)
        self.imgPreview.setObjectName(_fromUtf8("imgPreview"))
        self.gridLayout_2.addWidget(self.imgPreview, 1, 0, 1, 3)
        self.btnBrowse = QtGui.QPushButton(self.tabTesting)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.btnBrowse.setFont(font)
        self.btnBrowse.setObjectName(_fromUtf8("btnBrowse"))
        self.gridLayout_2.addWidget(self.btnBrowse, 4, 0, 1, 1)
        self.progressBar = QtGui.QProgressBar(self.tabTesting)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.gridLayout_2.addWidget(self.progressBar, 5, 1, 1, 2)
        self.label_3 = QtGui.QLabel(self.tabTesting)
        self.label_3.setTextFormat(QtCore.Qt.RichText)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout_2.addWidget(self.label_3, 5, 0, 1, 1)
        self.labeLAnomaly = QtGui.QLabel(self.tabTesting)
        self.labeLAnomaly.setText(_fromUtf8(""))
        self.labeLAnomaly.setObjectName(_fromUtf8("labeLAnomaly"))
        self.gridLayout_2.addWidget(self.labeLAnomaly, 4, 7, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout_2, 1, 1, 1, 1)
        self.label = QtGui.QLabel(self.tabTesting)
        self.label.setFrameShape(QtGui.QFrame.NoFrame)
        self.label.setTextFormat(QtCore.Qt.RichText)
        self.label.setScaledContents(False)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setWordWrap(True)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout_3.addWidget(self.label, 0, 1, 1, 1)
        self.tabWidget.addTab(self.tabTesting, _fromUtf8(""))
        self.horizontalLayout.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionChoose_Model_File = QtGui.QAction(MainWindow)
        self.actionChoose_Model_File.setObjectName(_fromUtf8("actionChoose_Model_File"))

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.btnBrowse.clicked.connect(self.browse_picture)

        self.btnProcess.clicked.connect(self.process_image)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Table Recognition", None))
        self.btnProcess.setText(_translate("MainWindow", "Process", None))
        self.OutputFolder.setText(_translate("MainWindow", "Output Folder", None))
        self.Output.setText(_translate("MainWindow", "Output", None))
        self.btnBrowse.setText(_translate("MainWindow", "Browse", None))
        self.label_3.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-weight:600; color:#ff0000;\">Progress</span></p></body></html>", None))
        self.label.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:16pt; font-weight:600; color:#060606;\">iFruitFly Detector</span></p></body></html>", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabTesting), _translate("MainWindow", "Detector", None))
        self.actionChoose_Model_File.setText(_translate("MainWindow", "Select Model File", None))
 
    def browse_picture(self):
        self.image = QtGui.QFileDialog.getOpenFileName(None,'OpenFile','c:\\',"Image file(*.png *.jpg)")
        #self.progressBar.setValue(0)
        self.image = str(self.image)
        self.labeLAnomaly.setStyleSheet("QLabel {background-color:red;color:white;}")
        self.file_name = ntpath.basename(self.image)
        self.file_name, ext=os.path.splitext(self.file_name)
        self.file_path = ntpath.dirname(self.image)
        self.write_path = ntpath.expanduser('~\\Documents\\Document Analysis')

        # creating write path if not exists 
        if not os.path.exists(self.write_path):
            os.makedirs(self.write_path)
        if self.image:
            self.imgPreview.setPixmap(QtGui.QPixmap(self.image).
                                           scaled(self.imgPreview.width(),
                                                  self.imgPreview.height()))

    def process_image(self):
      #self.imgProcess.setPixmap(QtGui.QPixmap(self.image).
      #                                     scaled(self.imgProcess.width(),
      #                                            self.imgProcess.height()))
      self.labeLAnomaly.setStyleSheet("QLabel {background-color:green;color:black;}")
      prefix = self.write_path + "\\" + self.file_name
      model_file = "J:\iFruitFly\Python Scripts\Model 1\\model.model"
      permanent_dir = "C:\\ifruitfly_junk"
      dir = "C:\\Users\\Abdullah_A\\Documents\\ifruitfly_temp"

      if not os.path.exists(permanent_dir):
            os.makedirs(permanent_dir)
      if self.image:
          self.imgPreview.setPixmap(QtGui.QPixmap(self.image).scaled(self.imgPreview.width(), self.imgPreview.height()))
      if not os.path.exists(self.write_path):
            os.makedirs(self.write_path)
      if self.image:
          self.imgPreview.setPixmap(QtGui.QPixmap(self.image).scaled(self.imgPreview.width(), self.imgPreview.height()))
      #python_wrapper(mImage, prefix, file_name, pre_prefix, dir, permanent_dir, model)      
      ITW.python_wrapper(self.file_path + "//" + self.file_name, prefix, self.file_name, self.write_path, dir, permanent_dir, model_file)


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

