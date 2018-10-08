from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow, infromation):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1029, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.splitter = QtWidgets.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")

        self.vtk_panel = QtWidgets.QFrame(self.splitter)
        self.vtk_panel.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.vtk_panel.setFrameShadow(QtWidgets.QFrame.Raised)
        self.vtk_panel.setObjectName("vtk_panel")
        self.horizontalLayout.addWidget(self.splitter)

        self.frame = QtWidgets.QFrame(self.splitter)
        self.frame.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName("verticalLayout")

        self.label = QtWidgets.QLabel(self.frame)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)

        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)

        self.label_3 = QtWidgets.QLabel(self.frame)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)

        self.label_4 = QtWidgets.QLabel(self.frame)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)

        self.label_5 = QtWidgets.QLabel(self.frame)
        self.label_5.setObjectName("label_5")
        self.verticalLayout.addWidget(self.label_5)

        self.label_6 = QtWidgets.QLabel(self.frame)
        self.label_6.setObjectName("label_6")
        self.verticalLayout.addWidget(self.label_6)

        self.label_7 = QtWidgets.QLabel(self.frame)
        self.label_7.setObjectName("label_7")
        self.verticalLayout.addWidget(self.label_7)

        self.label_8 = QtWidgets.QLabel(self.frame)
        self.label_8.setObjectName("label_8")
        self.verticalLayout.addWidget(self.label_8)

        self.label_9 = QtWidgets.QLabel(self.frame)
        self.label_9.setObjectName("label_9")
        self.verticalLayout.addWidget(self.label_9)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1029, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        infor = {'PatientID': 'AW959532241.111.1212659242', 'PatientName': '01^AC', 'PatientBirthDate': '', 'PatientSex': 'M',
         'StudyID': '', 'StudyDate': '20080605', 'StudyTime': '111034.203000', 'InstitutionName': 'CHU de Rouen',
         'Manufacturer': 'SIEMENS'}

        self.retranslateUiwithINfor(MainWindow,infor)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "GlyphViewer: "))
        self.label.setText(_translate("MainWindow", "PatientID: "))
        self.label_2.setText(_translate("MainWindow", "PatientName: "))
        self.label_3.setText(_translate("MainWindow", "PatientBirthDate: "))
        self.label_4.setText(_translate("MainWindow", "PatientSex: "))
        self.label_5.setText(_translate("MainWindow", "StudyID: "))
        self.label_6.setText(_translate("MainWindow", "StudyDate: "))
        self.label_7.setText(_translate("MainWindow", "StudyTime: "))
        self.label_8.setText(_translate("MainWindow", "InstitutionName: "))
        self.label_9.setText(_translate("MainWindow", "Manufacturer: "))

    def retranslateUiwithINfor(self, MainWindow, information):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "GlyphViewer: "))
        self.label.setText(_translate("MainWindow", "PatientID: "+ information['PatientID']))
        self.label_2.setText(_translate("MainWindow", "PatientName: "+ information['PatientName']))
        self.label_3.setText(_translate("MainWindow", "PatientBirthDate: "+ information['PatientBirthDate']))
        self.label_4.setText(_translate("MainWindow", "PatientSex: "+ information['PatientSex']))
        self.label_5.setText(_translate("MainWindow", "StudyID: "+ information['StudyID']))
        self.label_6.setText(_translate("MainWindow", "StudyDate: "+ information['StudyDate']))
        self.label_7.setText(_translate("MainWindow", "StudyTime: "+ information['StudyTime']))
        self.label_8.setText(_translate("MainWindow", "InstitutionName: "+ information['InstitutionName']))
        self.label_9.setText(_translate("MainWindow", "Manufacturer: "+ information['Manufacturer']))


if __name__=="__main__":
    import sys
    app=QtWidgets.QApplication(sys.argv)
    widget=QtWidgets.QMainWindow()
    ui=Ui_MainWindow()
    ui.setupUi(widget)
    widget.show()
    sys.exit(app.exec_())