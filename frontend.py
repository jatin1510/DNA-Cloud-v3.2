# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'frontend.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets, QAction

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1117, 815)

        self.main_widget = MainUI()
        self.setCentralWidget(self.main_widget)

        self.statusBar()  # for showing status bar in application
        # for showing menu items like FILE,ABOUT etc..
        menubar = self.menuBar()

        # Actions for File menu
        self.encodeAction = QAction("&Encode", self)
        self.encodeAction.setShortcut("Ctrl+E")
        self.encodeAction.setStatusTip("Encode file to DNA")
        self.encodeAction.triggered.connect(self.encodeFile)

        self.decodeAction = QAction("&Decode", self)
        self.decodeAction.setShortcut("Ctrl+D")
        self.decodeAction.setStatusTip("Decode file from DNA")
        self.decodeAction.triggered.connect(self.decodeFile)

        exitAction = QAction("&Exit", self)
        exitAction.setShortcut("Ctrl+Q")
        exitAction.setStatusTip("Exit application")
        exitAction.triggered.connect(QApplication.quit)

        # File menu creation
        fileMenu = menubar.addMenu("&Files")
        fileMenu.addAction(self.encodeAction)
        fileMenu.addAction(self.decodeAction)
        fileMenu.addAction(exitAction)

        # Actions for Tools menu
        self.storageEstimatorAction = QAction("&Storage Estimator", self)
        self.storageEstimatorAction.setStatusTip(
            "Estimates approximate encoded file size required on disk "
        )
        self.storageEstimatorAction.triggered.connect(self.showMemoryEstimator)

        self.costEstimatorAction = QAction("&Cost Estimator", self)
        self.costEstimatorAction.setStatusTip(
            "Predicts approximate cost to encode in DNA"
        )
        self.costEstimatorAction.triggered.connect(self.showCostEstimator)

        # 	self.barcodeGeneratorAction = QAction('&Generate Barcode',self)
        # 	self.barcodeGeneratorAction.setStatusTip('Generate Barcode')
        # 	self.barcodeGeneratorAction.triggered.connect(self.showBarcode)

        # Tools menu creation
        toolsMenu = menubar.addMenu("&Tools")
        toolsMenu.addAction(self.storageEstimatorAction)
        toolsMenu.addAction(self.costEstimatorAction)
        # 	toolsMenu.addAction(self.barcodeGeneratorAction)

        # Actions for Follow us
        self.Gupta_Lab = QAction("&Gupta Lab", self)
        self.Gupta_Lab.setStatusTip("Gupta Lab")
        self.Gupta_Lab.triggered.connect(self.showGupta_Lab)

        self.Twitter = QAction("&Twitter", self)
        self.Twitter.setStatusTip("Twitter")
        self.Twitter.triggered.connect(self.showTwitter)

        self.Gupta_Lab_GitHub = QAction("&GitHub", self)
        self.Gupta_Lab_GitHub.setStatusTip("Gupta Lab Github")
        self.Gupta_Lab_GitHub.triggered.connect(self.showGupta_Lab_GitHub)

        self.Youtube_Channel = QAction("&YouTube", self)
        self.Youtube_Channel.setStatusTip("Youtube Channel")
        self.Youtube_Channel.triggered.connect(self.showYoutube_Channel)

        self.LinkedIn = QAction("&LinkedIn", self)
        self.LinkedIn.setStatusTip("LinkedIn")
        self.LinkedIn.triggered.connect(self.showLinkedIn)

        # About Follow us
        AboutFollowUs = menubar.addMenu("&Follow Us")
        AboutFollowUs.addAction(self.Gupta_Lab)
        AboutFollowUs.addAction(self.Gupta_Lab_GitHub)
        AboutFollowUs.addAction(self.LinkedIn)
        AboutFollowUs.addAction(self.Twitter)
        AboutFollowUs.addAction(self.Youtube_Channel)

        # Actions for Contact us
        self.Email_Id = QAction("&Email Id", self)
        self.Email_Id.setStatusTip("Email Id")
        self.Email_Id.triggered.connect(self.showEmail_Id)

        self.Gupta_Lab1 = QAction("&Gupta Lab", self)
        self.Gupta_Lab1.setStatusTip("Gupta Lab Contact page")
        self.Gupta_Lab1.triggered.connect(self.showGupta_Lab1)

        # About Contact us
        AboutContactUs = menubar.addMenu("&Contact Us")
        AboutContactUs.addAction(self.Email_Id)
        AboutContactUs.addAction(self.Gupta_Lab1)

        # Actions for help menubar
        self.User_Manual = QAction("&User Manual", self)
        self.User_Manual.setStatusTip("User Manual")
        self.User_Manual.triggered.connect(self.showUser_Manual)

        self.Product_Demo = QAction("&Product Demo", self)
        self.Product_Demo.setStatusTip("Product Demo")
        self.Product_Demo.triggered.connect(self.showProduct_Demo)

        self.Product_Feedback = QAction("&Product Feedback", self)
        self.Product_Feedback.setStatusTip("Product Feedback")
        self.Product_Feedback.triggered.connect(self.showProduct_Feedback)

        self.Credits = QAction("&Credits", self)
        self.Credits.setStatusTip("Credits")
        self.Credits.triggered.connect(self.showCredits)

        self.About_Us = QAction("&About Us", self)
        self.About_Us.setStatusTip("About Us")
        self.About_Us.triggered.connect(self.showAbout_Us)

        # About Help
        AboutHelp = menubar.addMenu("&Help")
        AboutHelp.addAction(self.User_Manual)
        AboutHelp.addAction(self.Product_Demo)
        AboutHelp.addAction(self.Product_Feedback)
        AboutHelp.addAction(self.Credits)
        AboutHelp.addSeparator()
        AboutHelp.addAction(self.About_Us)

        # Actions for About menu
        self.versionAction = QAction("&Version", self)
        self.versionAction.setStatusTip("Version info")
        self.versionAction.triggered.connect(self.showVersion)

        # About menu creation
        AboutMenu = menubar.addMenu("&About")
        AboutMenu.addAction(self.versionAction)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setGeometry(QtCore.QRect(580, 50, 531, 311))
        self.frame_2.setAutoFillBackground(True)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame_2.setObjectName("frame_2")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setGeometry(QtCore.QRect(21, 551, 91, 31))
        self.plainTextEdit.setReadOnly(True)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.plainTextEdit_2 = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit_2.setGeometry(QtCore.QRect(21, 591, 141, 31))
        self.plainTextEdit_2.setReadOnly(True)
        self.plainTextEdit_2.setObjectName("plainTextEdit_2")
        self.plainTextEdit_3 = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit_3.setGeometry(QtCore.QRect(21, 631, 141, 31))
        self.plainTextEdit_3.setReadOnly(True)
        self.plainTextEdit_3.setObjectName("plainTextEdit_3")
        self.plainTextEdit_4 = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit_4.setGeometry(QtCore.QRect(21, 671, 91, 31))
        self.plainTextEdit_4.setReadOnly(True)
        self.plainTextEdit_4.setObjectName("plainTextEdit_4")
        self.plainTextEdit_5 = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit_5.setGeometry(QtCore.QRect(121, 551, 421, 31))
        self.plainTextEdit_5.setReadOnly(True)
        self.plainTextEdit_5.setObjectName("plainTextEdit_5")
        self.plainTextEdit_6 = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit_6.setGeometry(QtCore.QRect(121, 671, 421, 31))
        self.plainTextEdit_6.setObjectName("plainTextEdit_6")
        self.plainTextEdit_7 = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit_7.setGeometry(QtCore.QRect(171, 591, 371, 31))
        self.plainTextEdit_7.setReadOnly(True)
        self.plainTextEdit_7.setObjectName("plainTextEdit_7")
        self.plainTextEdit_8 = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit_8.setGeometry(QtCore.QRect(171, 631, 371, 31))
        self.plainTextEdit_8.setReadOnly(True)
        self.plainTextEdit_8.setObjectName("plainTextEdit_8")
        self.frame_3 = QtWidgets.QFrame(self.centralwidget)
        self.frame_3.setGeometry(QtCore.QRect(10, 540, 541, 171))
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(130, 410, 401, 31))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.plainTextEdit_9 = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit_9.setGeometry(QtCore.QRect(20, 410, 104, 31))
        self.plainTextEdit_9.setReadOnly(True)
        self.plainTextEdit_9.setObjectName("plainTextEdit_9")
        self.plainTextEdit_10 = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit_10.setGeometry(QtCore.QRect(581, 631, 141, 31))
        self.plainTextEdit_10.setReadOnly(True)
        self.plainTextEdit_10.setObjectName("plainTextEdit_10")
        self.plainTextEdit_11 = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit_11.setGeometry(QtCore.QRect(681, 551, 421, 31))
        self.plainTextEdit_11.setReadOnly(True)
        self.plainTextEdit_11.setObjectName("plainTextEdit_11")
        self.plainTextEdit_12 = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit_12.setGeometry(QtCore.QRect(581, 591, 141, 31))
        self.plainTextEdit_12.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.plainTextEdit_12.setReadOnly(True)
        self.plainTextEdit_12.setObjectName("plainTextEdit_12")
        self.plainTextEdit_13 = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit_13.setGeometry(QtCore.QRect(731, 631, 371, 31))
        self.plainTextEdit_13.setReadOnly(True)
        self.plainTextEdit_13.setObjectName("plainTextEdit_13")
        self.plainTextEdit_14 = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit_14.setGeometry(QtCore.QRect(681, 671, 421, 31))
        self.plainTextEdit_14.setObjectName("plainTextEdit_14")
        self.frame_4 = QtWidgets.QFrame(self.centralwidget)
        self.frame_4.setGeometry(QtCore.QRect(570, 540, 541, 171))
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.plainTextEdit_15 = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit_15.setGeometry(QtCore.QRect(581, 551, 91, 31))
        self.plainTextEdit_15.setReadOnly(True)
        self.plainTextEdit_15.setObjectName("plainTextEdit_15")
        self.plainTextEdit_16 = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit_16.setGeometry(QtCore.QRect(580, 410, 104, 31))
        self.plainTextEdit_16.setReadOnly(True)
        self.plainTextEdit_16.setObjectName("plainTextEdit_16")
        self.plainTextEdit_17 = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit_17.setGeometry(QtCore.QRect(581, 671, 91, 31))
        self.plainTextEdit_17.setReadOnly(True)
        self.plainTextEdit_17.setObjectName("plainTextEdit_17")
        self.plainTextEdit_18 = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit_18.setGeometry(QtCore.QRect(731, 591, 371, 31))
        self.plainTextEdit_18.setReadOnly(True)
        self.plainTextEdit_18.setObjectName("plainTextEdit_18")
        self.progressBar_2 = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar_2.setGeometry(QtCore.QRect(690, 410, 401, 31))
        self.progressBar_2.setProperty("value", 24)
        self.progressBar_2.setObjectName("progressBar_2")
        self.plainTextEdit_21 = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit_21.setGeometry(QtCore.QRect(150, 10, 231, 31))
        self.plainTextEdit_21.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.plainTextEdit_21.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.plainTextEdit_21.setTabChangesFocus(False)
        self.plainTextEdit_21.setLineWrapMode(QtWidgets.QPlainTextEdit.WidgetWidth)
        self.plainTextEdit_21.setReadOnly(True)
        self.plainTextEdit_21.setBackgroundVisible(True)
        self.plainTextEdit_21.setObjectName("plainTextEdit_21")
        self.plainTextEdit_20 = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit_20.setGeometry(QtCore.QRect(710, 10, 231, 31))
        self.plainTextEdit_20.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.plainTextEdit_20.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.plainTextEdit_20.setTabChangesFocus(False)
        self.plainTextEdit_20.setLineWrapMode(QtWidgets.QPlainTextEdit.WidgetWidth)
        self.plainTextEdit_20.setReadOnly(True)
        self.plainTextEdit_20.setBackgroundVisible(True)
        self.plainTextEdit_20.setObjectName("plainTextEdit_20")
        self.frame_5 = QtWidgets.QFrame(self.centralwidget)
        self.frame_5.setGeometry(QtCore.QRect(10, 50, 531, 311))
        self.frame_5.setAutoFillBackground(True)
        self.frame_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame_5.setObjectName("frame_5")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(170, 470, 201, 51))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(740, 470, 201, 51))
        self.pushButton_2.setObjectName("pushButton_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1117, 26))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.plainTextEdit.setPlainText(_translate("MainWindow", "File Name"))
        self.plainTextEdit_2.setPlainText(_translate("MainWindow", "Size of DNA String"))
        self.plainTextEdit_3.setPlainText(_translate("MainWindow", "Number of Chunks"))
        self.plainTextEdit_4.setPlainText(_translate("MainWindow", "Comment"))
        self.plainTextEdit_9.setPlainText(_translate("MainWindow", "Progress:"))
        self.plainTextEdit_10.setPlainText(_translate("MainWindow", "Number of Chunks"))
        self.plainTextEdit_12.setPlainText(_translate("MainWindow", "Size of DNA String"))
        self.plainTextEdit_15.setPlainText(_translate("MainWindow", "File Name"))
        self.plainTextEdit_16.setPlainText(_translate("MainWindow", "Progress:"))
        self.plainTextEdit_17.setPlainText(_translate("MainWindow", "Comment"))
        self.plainTextEdit_21.setPlainText(_translate("MainWindow", "Drag and Drop a file to be encoded"))
        self.plainTextEdit_20.setPlainText(_translate("MainWindow", "Drag and Drop a file to be decoded"))
        self.pushButton.setText(_translate("MainWindow", "Select the file to be encoded"))
        self.pushButton_2.setText(_translate("MainWindow", "Select the file to be decoded"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())