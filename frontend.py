"""
##########################################################################################
Improvised Version: DNA Cloud 4.0.0
Developers: Devarshi Joshi, Arpan Shingala
Mentor: Prof. Manish K Gupta
Website: www.guptalab.org/dnacloud
This file is the Main GUI file that is to be launched via command - python MainFrame.py.
This file will run on python 3.10.5
##########################################################################################
"""

NULL = 0
import sys
from PyQt5.QtWidgets import *
import os
import io
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from collections import deque
import GoldmanEncoding
import GoldmanDecoding
import golayEncoding
import GolayDecode
import EstimationUI
import webbrowser
import QRCode
from PyQt5 import QtCore, QtGui, QtWidgets

def Error(errorMessage):
    msg = QMessageBox()
    msg.setWindowTitle("Error")
    msg.setText(errorMessage)
    msg.setIcon(QMessageBox.Critical)
    x = msg.exec_()
        
# Takes input comment from user for file being encoded
def TakeComment():
    main_window = QMainWindow()

    text, ok = QInputDialog.getText(main_window, 'Comment Box', 'Enter a comment:')

    if ok and text.strip():
        return text
    else:
        QMessageBox.warning(main_window, 'Warning', 'Please enter a non-empty value.', QMessageBox.Ok)
        return None

# This object carries out encoding action of certain type

class EncodeThread(QThread):
    # Used for indication how much percentage of action completed
    signalStatus = pyqtSignal(str)

    def __init__(self, fileName, typeOfAction, parent=None):
        super(EncodeThread, self).__init__(parent)
        self.fileName = fileName
        # 0 for encodeGoldman , 1 for encodeGolay , 2 for decodeGoldman , 3 for decodeGolay
        self.typeOfAction = typeOfAction

    def run(self):
        if self.typeOfAction == 0:  # Goldman Encoding
            GoldmanEncoding.encodeFile(self.fileName, self.signalStatus)
        elif self.typeOfAction == 1:   # Golay Encoding
            golayEncoding.encodeFile(self.fileName, self.signalStatus)
        self.signalStatus.emit('Idle.')  # Indicating action is finished

# This object carries out decoding action of certain type

class DecodeThread(QThread):
    # Used for indication how much percentage of action completed
    signalStatus = pyqtSignal(str)

    def __init__(self, fileName, typeOfAction, parent=None):
        super(DecodeThread, self).__init__(parent)
        self.fileName = fileName
        # 0 for encodeGoldman , 1 for encodeGolay , 2 for decodeGoldman , 3 for decodeGolay
        self.typeOfAction = typeOfAction
        self.parent = parent

    def run(self):
        if self.typeOfAction == 2:    # Goldman Decoding
            GoldmanDecoding.decodeFile(self.fileName, self.signalStatus)
        elif self.typeOfAction == 3:   # Golay Decoding
            GolayDecode.decodeFile(self.fileName, self.signalStatus)
        # print("error")
        self.signalStatus.emit('Idle.')  # Indicating action is finished

# This object shows dialouge box for selecting encoding type
class EncodeSelection(QDialog):
    def __init__(self, parent=None):
        super(EncodeSelection, self).__init__(parent)
        self.setWindowTitle("Encode")
        self.initUI()

    def initUI(self):
        self.selectionComboBox = QComboBox()
        encodings = ['Goldman', 'Golay']
        self.selectionComboBox.addItems(encodings)

        # OK and Cancel buttons
        self.buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        layout = QVBoxLayout(self)
        layout.addWidget(self.selectionComboBox)
        layout.addWidget(self.buttons)
        self.setLayout(layout)

        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)


# This object shows dialouge box for selecting decoding type
class DecodeSelection(QDialog):
    def __init__(self, parent=None):
        super(DecodeSelection, self).__init__(parent)
        self.setWindowTitle("Decode")
        self.initUI()

    def initUI(self):
        self.selectionComboBox = QComboBox()
        encodings = ['Goldman', 'Golay']
        self.selectionComboBox.addItems(encodings)

        # OK and Cancel buttons
        self.buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        layout = QVBoxLayout(self)
        layout.addWidget(self.selectionComboBox)
        layout.addWidget(self.buttons)
        self.setLayout(layout)

        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)


# Selects one of the type of encoding/decoding (Golay or Goldman)
def getActionType(typeOfAction, parent=None):
    if typeOfAction == 'E':   # Encoding Action
        dialog = EncodeSelection(parent)
        result = dialog.exec_()
        if(result == 1):
            encodingType = str(dialog.selectionComboBox.currentText())
            if encodingType == 'Goldman':
                return 0
            elif encodingType == 'Golay':
                return 1
            return -1
        else:
            return -1
    else:
        dialog = DecodeSelection(parent)
        result = dialog.exec_()
        if(result == 1):
            decodingType = str(dialog.selectionComboBox.currentText())
            if decodingType == 'Goldman':
                return 2
            elif decodingType == 'Golay':
                return 3
            return -1
        else:
            return -1


# Used for identifying any action
class ActionIdentifierTuple():
    def __init__(self, progressBar, fileName, encodingType):
        self.progressBar = progressBar
        self.fileName = fileName
        self.encodingType = encodingType
    
# The Main GUI of any action
class ActionUI(QFrame):

    def __init__(self, parent, actionType):
        QFrame.__init__(self, parent)
        self.actionType = actionType   # 'E' for encoding , 'D' for decoding
        self.noOfFiles = 0
        self.processQueue = deque()
        self.running = False
        self.initUI()

    def initUI(self):
        self.layout = QGridLayout()
        self.layout.setAlignment(Qt.AlignTop)
        self.setLayout(self.layout)

        self.setAcceptDrops(True)
        self.setAutoFillBackground(False)
        self.setStyleSheet(
            "background-color: rgb(255,250,250); margin:5px; border:1px solid rgb(0, 0, 0);")

    # This is called when any drag and drop event begins
    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls:
            e.accept()
        else:
            e.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(Qt.CopyAction)
            event.accept()
            for url in event.mimeData().urls():
                linkToFile = str(url.toLocalFile())
                if os.path.isdir(linkToFile):
                    print('Folder Not Supported Yet')
                    continue
                self.addLink(linkToFile)
        else:
            event.ignore()

    def addLink(self, linkToFile):
        if not os.path.isfile(linkToFile):
            return
        
        reverseFilename = linkToFile[::-1]
        indexDot = reverseFilename.find('.')
        if indexDot == -1:
            return
        
        actionType = getActionType(self.actionType)
        if actionType > 1 and linkToFile[-1*indexDot:] != "dnac":
            Error("File is not in .dnac format!!")
            return

        textView = QLabel(linkToFile)
        textView.setStyleSheet(
            "background-color: rgb(255,255,255); margin:5px; border:0px solid rgb(0, 0, 0);")
        scroll = QScrollArea()
        scroll.setWidget(textView)
        scroll.setWidgetResizable(True)
        scroll.setFixedWidth(250)
        scroll.setFixedHeight(40)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.progress = QProgressBar(self)
        self.progress.setValue(0)
        self.progress.setAlignment(Qt.AlignCenter)

        self.layout.addWidget(scroll, self.noOfFiles, 0)
        self.layout.addWidget(self.progress, self.noOfFiles, 1)

        self.noOfFiles = self.noOfFiles + 1
        self.addAction(self.progress, linkToFile,
                       actionType)

    def addAction(self, progressBar, fileName, encodingType):
        if len(self.processQueue) == 0:
            self.processQueue.append(ActionIdentifierTuple(
                progressBar, fileName, encodingType))
            self.startAction()
        else:
            self.processQueue.append(ActionIdentifierTuple(
                progressBar, fileName, encodingType))

    def startAction(self):
        fileName = self.processQueue[0].fileName
        encodingType = self.processQueue[0].encodingType

        if (encodingType <= 1):

            indexDot = fileName.rfind('.')
            fileNameWithoutExtension = fileName[:indexDot]
            input_comment = TakeComment()
            
            QRCode.generateQR("File name: " + fileName + "\nComment: " + input_comment, fileNameWithoutExtension)
            
            self.thread = EncodeThread(fileName, encodingType)
        else:
            self.thread = DecodeThread(fileName, encodingType)
        self.thread.signalStatus.connect(self.updateStatus)
        self.thread.start()

    def updateStatus(self, status):
        if status != 'Idle.':
            self.processQueue[0].progressBar.setValue(int(status))
        else:
            self.thread.wait()
            self.processQueue.popleft()
            if len(self.processQueue):
                self.startAction()

# This object represents main UI which is collection of all actions (Here encoding window + decoding window)
class MainUI(QWidget):
    def __init__(self, MainWindow, parent=None):
        super(MainUI, self).__init__()
        self.initUI()
        MainWindow.setObjectName("DNACloud - v4.0.0")
        MainWindow.resize(1120, 750)
        MainWindow.setMinimumSize(QtCore.QSize(1120, 750))
        MainWindow.setMaximumSize(QtCore.QSize(1120, 750))
        MainWindow.setBackgroundRole(QtGui.QPalette.Midlight)
        MainWindow.setAutoFillBackground(True)
        # MainWindow.setStyleSheet("background-color: rgb(238, 203, 178);")
        MainWindow.setStyleSheet("background-color: rgb(0, 203, 178);")

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
        self.frame_2.raise_()
        self.frame_3.raise_()
        self.progressBar.raise_()
        self.plainTextEdit_9.raise_()
        self.frame_4.raise_()
        self.plainTextEdit_16.raise_()
        self.progressBar_2.raise_()
        self.plainTextEdit_21.raise_()
        self.plainTextEdit_20.raise_()
        self.frame_5.raise_()
        self.pushButton.raise_()
        self.pushButton_2.raise_()
        self.plainTextEdit.raise_()
        self.plainTextEdit_6.raise_()
        self.plainTextEdit_4.raise_()
        self.plainTextEdit_8.raise_()
        self.plainTextEdit_7.raise_()
        self.plainTextEdit_2.raise_()
        self.plainTextEdit_3.raise_()
        self.plainTextEdit_5.raise_()
        self.plainTextEdit_18.raise_()
        self.plainTextEdit_10.raise_()
        self.plainTextEdit_11.raise_()
        self.plainTextEdit_13.raise_()
        self.plainTextEdit_17.raise_()
        self.plainTextEdit_14.raise_()
        self.plainTextEdit_15.raise_()
        self.plainTextEdit_12.raise_()

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "DNACloud - v4.0.0"))
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
        # self.menuFile.setTitle(_translate("MainWindow", "File"))


    def initUI(self):
        self.encodeUI = ActionUI(self, 'E')
        self.decodeUI = ActionUI(self, 'D')

        layout = QHBoxLayout()
        layout.addWidget(self.encodeUI, 1)
        layout.addWidget(self.decodeUI, 1)

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle('DNA 4.0.0')
        self.setWindowIcon(QIcon("DNA_icon-8.png"))
        self.initUI()

    def initUI(self):
        self.main_widget = MainUI(self)
        self.setCentralWidget(self.main_widget)

        # self.resize(1120, 750)
        # self.setMinimumSize(QtCore.QSize(1120, 750))
        # self.setMaximumSize(QtCore.QSize(1120, 750))
        # self.setBackgroundRole(QtGui.QPalette.Midlight)
        # self.setAutoFillBackground(True)
        # self.setStyleSheet("background-color: rgb(238, 203, 178);")

        self.statusBar()   # for showing status bar in application
        # for showing menu items like FILE,ABOUT etc..
        menubar = self.menuBar()

        # Actions for File menu
        self.encodeAction = QAction('&Encode', self)
        self.encodeAction.setShortcut('Ctrl+E')
        self.encodeAction.setStatusTip('Encode file to DNA')
        self.encodeAction.triggered.connect(self.encodeFile)

        self.decodeAction = QAction('&Decode', self)
        self.decodeAction.setShortcut('Ctrl+D')
        self.decodeAction.setStatusTip('Decode file from DNA')
        self.decodeAction.triggered.connect(self.decodeFile)

        exitAction = QAction('&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(QApplication.quit)

        # File menu creation
        fileMenu = menubar.addMenu('&Files')
        fileMenu.addAction(self.encodeAction)
        fileMenu.addAction(self.decodeAction)
        fileMenu.addAction(exitAction)

        # Actions for Tools menu
        self.storageEstimatorAction = QAction('&Storage Estimator', self)
        self.storageEstimatorAction.setStatusTip(
            'Estimates approximate encoded file size required on disk ')
        self.storageEstimatorAction.triggered.connect(self.showMemoryEstimator)

        self.costEstimatorAction = QAction('&Cost Estimator', self)
        self.costEstimatorAction.setStatusTip(
            'Predicts approximate cost to encode in DNA')
        self.costEstimatorAction.triggered.connect(self.showCostEstimator)

    #	self.barcodeGeneratorAction = QAction('&Generate Barcode',self)
    #	self.barcodeGeneratorAction.setStatusTip('Generate Barcode')
    #	self.barcodeGeneratorAction.triggered.connect(self.showBarcode)

    # Tools menu creation
        toolsMenu = menubar.addMenu('&Tools')
        toolsMenu.addAction(self.storageEstimatorAction)
        toolsMenu.addAction(self.costEstimatorAction)
    #	toolsMenu.addAction(self.barcodeGeneratorAction)

        # Actions for Follow us
        self.Gupta_Lab = QAction('&Gupta Lab', self)
        self.Gupta_Lab.setStatusTip('Gupta Lab')
        self.Gupta_Lab.triggered.connect(self.showGupta_Lab)

        self.Twitter = QAction('&Twitter', self)
        self.Twitter.setStatusTip('Twitter')
        self.Twitter.triggered.connect(self.showTwitter)

        self.Gupta_Lab_GitHub = QAction('&GitHub', self)
        self.Gupta_Lab_GitHub.setStatusTip('Gupta Lab Github')
        self.Gupta_Lab_GitHub.triggered.connect(self.showGupta_Lab_GitHub)

        self.Youtube_Channel = QAction('&YouTube', self)
        self.Youtube_Channel.setStatusTip('Youtube Channel')
        self.Youtube_Channel.triggered.connect(self.showYoutube_Channel)

        self.LinkedIn = QAction('&LinkedIn', self)
        self.LinkedIn.setStatusTip('LinkedIn')
        self.LinkedIn.triggered.connect(self.showLinkedIn)

        # About Follow us
        AboutFollowUs = menubar.addMenu('&Follow Us')
        AboutFollowUs.addAction(self.Gupta_Lab)
        AboutFollowUs.addAction(self.Gupta_Lab_GitHub)
        AboutFollowUs.addAction(self.LinkedIn)
        AboutFollowUs.addAction(self.Twitter)
        AboutFollowUs.addAction(self.Youtube_Channel)

        # Actions for Contact us
        self.Email_Id = QAction('&Email Id', self)
        self.Email_Id.setStatusTip('Email Id')
        self.Email_Id.triggered.connect(self.showEmail_Id)

        self.Gupta_Lab1 = QAction('&Gupta Lab', self)
        self.Gupta_Lab1.setStatusTip('Gupta Lab Contact page')
        self.Gupta_Lab1.triggered.connect(self.showGupta_Lab1)

        # About Contact us
        AboutContactUs = menubar.addMenu('&Contact Us')
        AboutContactUs.addAction(self.Email_Id)
        AboutContactUs.addAction(self.Gupta_Lab1)

        # Actions for help menubar
        self.User_Manual = QAction('&User Manual', self)
        self.User_Manual.setStatusTip('User Manual')
        self.User_Manual.triggered.connect(self.showUser_Manual)

        self.Product_Demo = QAction('&Product Demo', self)
        self.Product_Demo.setStatusTip('Product Demo')
        self.Product_Demo.triggered.connect(self.showProduct_Demo)

        self.Product_Feedback = QAction('&Product Feedback', self)
        self.Product_Feedback.setStatusTip('Product Feedback')
        self.Product_Feedback.triggered.connect(self.showProduct_Feedback)

        self.Credits = QAction('&Credits', self)
        self.Credits.setStatusTip('Credits')
        self.Credits.triggered.connect(self.showCredits)

        self.About_Us = QAction('&About Us', self)
        self.About_Us.setStatusTip('About Us')
        self.About_Us.triggered.connect(self.showAbout_Us)

        # About Help
        AboutHelp = menubar.addMenu('&Help')
        AboutHelp.addAction(self.User_Manual)
        AboutHelp.addAction(self.Product_Demo)
        AboutHelp.addAction(self.Product_Feedback)
        AboutHelp.addAction(self.Credits)
        AboutHelp.addSeparator()
        AboutHelp.addAction(self.About_Us)

        # Actions for About menu
        self.versionAction = QAction('&Version', self)
        self.versionAction.setStatusTip('Version info')
        self.versionAction.triggered.connect(self.showVersion)

        # About menu creation
        AboutMenu = menubar.addMenu('&About')
        AboutMenu.addAction(self.versionAction)

        # self.statusBar().showMessage(
        #     "Drag and drop on left to encode file or on right to decode file")
        # self.setStyleSheet("background-color: rgb(238,203,178)")

    def getEncodeActionUI(self):
        return self.main_widget.encodeUI

    def getDecodeActionUI(self):
        return self.main_widget.decodeUI

    def encodeFile(self):
        openfile = QFileDialog.getOpenFileName(self)[0]
        encodeAction = self.getEncodeActionUI()
        encodeAction.addLink(str(openfile))

    def decodeFile(self):
        openfile = QFileDialog.getOpenFileName(self)[0]
        decodeAction = self.getDecodeActionUI()
        decodeAction.addLink(str(openfile))

    # def showBarcode(self) :  # Not supported Yet
    #	return

    def showMemoryEstimator(self):
        est = EstimationUI.MemoryEstimation(self)
        est.exec_()

    def showCostEstimator(self):
        est = EstimationUI.CostEstimation(self)
        est.exec_()

    def showVersion(self):
        est = EstimationUI.Version(self)
        est.exec_()

    def showGupta_Lab(self):
        webbrowser.open("https://guptalab.org/", new=2)

    def showTwitter(self):
        webbrowser.open("https://twitter.com/guptalab", new=2)

    def showGupta_Lab_GitHub(self):
        webbrowser.open("https://github.com/guptalab/", new=2)

    def showYoutube_Channel(self):
        webbrowser.open("https://www.youtube.com/c/ManishGuptamankg", new=2)

    def showLinkedIn(self):
        webbrowser.open("https://www.linkedin.com/company/guptalab/", new=2)

    def showEmail_Id(self):
        est = EstimationUI.Email_Id(self)
        est.exec_()

    def showGupta_Lab1(self):
        webbrowser.open("https://www.guptalab.org/mainweb/contact.html", new=2)

    def showUser_Manual(self):
        webbrowser.open(
            "https://drive.google.com/file/d/1qWt68foUxf_lI9YLCyL2qR66Sj39AXej/view", new=2)

    def showProduct_Demo(self):
        NULL

    def showProduct_Feedback(self):
        webbrowser.open("https://forms.gle/jTY8FcgKeWrosqZ1A", new=2)

    def showCredits(self):
        webbrowser.open(
            "https://drive.google.com/file/d/1JRzBQjYBU8yQJHs5Ik9Dg9YIxAHmaaB8/view", new=2)

    def showAbout_Us(self):
        webbrowser.open(
            "https://drive.google.com/file/d/1LSCGnnHnLynDtoSff9n7kCLrhymhSCD7/view", new=2)


# app = QApplication(sys.argv)
# MainWindow = QtWidgets.QMainWindow()
# dna3Win = MainWindow() 
# dna3Win.showMaximized()
# app.exec_()

app = QApplication(sys.argv)
dna3Win = MainWindow()
dna3Win.show()
app.exec_()
