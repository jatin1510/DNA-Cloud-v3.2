"""
##########################################################################################
Improvised Version: DNA Cloud 3.2
Developers: Jaimin Satani, Jatin Ranpariya, Devarshi Joshi, Arpan Singhala, Chaitri Gudhka, Mukund Ladani, Nikhil Vaghasiya
Mentor: Prof. Manish K Gupta
Website: www.guptalab.org/dnacloud
This file is the Main GUI file that is to be launched via command - python MainFrame.py.
This file will run on python 3.10.5
##########################################################################################
Author: Aayush Kapadia,Suparshva Mehta
Project: DNA Cloud 3
Graduate Mentor: Dixita Limbachya
Mentor: Prof. Manish K Gupta
Website: www.guptalab.org/dnacloud
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
import BarCode
import re
import time
import Error_Detection_Correction

# Generalize Error 
    
def Error(errorMessage):
    msg = QMessageBox()
    msg.setWindowTitle("Error")
    msg.setText(errorMessage)
    msg.setIcon(QMessageBox.Critical)
    x = msg.exec_()

def show_success_popup():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setWindowTitle('Success')
    msg.setText('Operation successful!')
    msg.exec_()
        
class ShadowButton(QPushButton):
    def __init__(self, text, parent=None):
        super(ShadowButton, self).__init__(text, parent)
        self._shadowOffset = 2
        self._shadowColor = QColor(50, 50, 50, 50)
        self._baseColor = QColor(30, 144, 255)  # Dodger Blue

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw the button with a gradient color
        grad = QLinearGradient(0, 0, 0, self.height())
        grad.setColorAt(0, self._baseColor)
        grad.setColorAt(1, QColor(0, 0, 205))  # Medium Blue
        painter.setBrush(grad)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(0, 0, self.width(), self.height(), 8, 8)

        # Draw button text
        painter.setPen(Qt.white)
        painter.drawText(self.rect(), Qt.AlignCenter, self.text())

        # Draw button shadow
        painter.setBrush(self._shadowColor)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(self._shadowOffset, self._shadowOffset, self.width() - 4, self.height() - 4, 8, 8)

    def setColor(self, color):
        if self._baseColor != color:
            self._baseColor = color
            self.update()

    def color(self):
        return self._baseColor

    def setShadowOffset(self, offset):
        if self._shadowOffset != offset:
            self._shadowOffset = offset
            self.update()

    def shadowOffset(self):
        return self._shadowOffset

    color_ = pyqtProperty(QColor, color, setColor)
    shadowOffset_ = pyqtProperty(int, shadowOffset, setShadowOffset)

class InputDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Contact Details')
        self.setGeometry(225, 400, 500, 300)  # Increase window size

        # Remove Help button
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)

        title_font = QFont()
        title_font.setBold(True)
        title_font.setPointSize(16)

        self.name_label = QLabel('Name:')
        self.name_label.setStyleSheet('color: #000000; font-size: 16px; font-weight: bold;')

        label_font = QFont()
        label_font.setPointSize(14)

        self.name_label.setFont(label_font)
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText('Enter your name')

        self.email_label = QLabel('Email:')
        self.email_label.setStyleSheet('color: #000000; font-size: 16px; font-weight: bold;')
        self.email_label.setFont(label_font)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText('Enter your email')

        self.mobile_label = QLabel('Mobile Number:')
        self.mobile_label.setStyleSheet('color: #000000; font-size: 16px; font-weight: bold;')
        self.mobile_label.setFont(label_font)

        self.mobile_input = QLineEdit()
        self.mobile_input.setPlaceholderText('Enter your mobile number')

        submit_button = ShadowButton('Submit')
        submit_button.clicked.connect(self.on_submit)

        # Create a form layout
        form_layout = QFormLayout()
        form_layout.addRow(self.name_label, self.name_input)
        form_layout.addRow(self.email_label, self.email_input)
        form_layout.addRow(self.mobile_label, self.mobile_input)

        main_layout = QVBoxLayout(self)
        main_layout.addLayout(form_layout)
        main_layout.addWidget(submit_button)

        # Apply a more colorful stylesheet
        self.setStyleSheet('''
            QDialog {
                background-color: #f0f0f0;
                color: #333;
            }
            QLineEdit {
                background-color: #ffffff;
                color: #333;
                border: 2px solid #1e90ff;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
            }
        ''')

    def on_submit(self):
        name = self.name_input.text().strip()
        email = self.email_input.text().strip()
        mobile = self.mobile_input.text().strip()

        # Validate email using a simple regular expression
        email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
        if not email_pattern.fullmatch(email):
            self.show_warning('Please enter a valid email address.')
            return

        # Validate mobile number using a simple pattern (10 digits)
        mobile_pattern = re.compile(r'^\d{10}$')
        if not mobile_pattern.fullmatch(mobile):
            self.show_warning('Please enter a valid 10-digit mobile number.')
            return

        if name and email and mobile:
            self.result = (name, email, mobile)
            self.accept()
        else:
            self.show_warning('Please enter values for all fields.')

    def show_warning(self, message):
        QMessageBox.warning(self, 'Warning', message, QMessageBox.Ok)

def TakeComment():
    dialog = InputDialog()
    result = dialog.exec_()

    if result == QDialog.Accepted:
        return dialog.result
    else:
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
def getActionType(typeOfAction,fileName = None, parent=None):
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
        # dialog = DecodeSelection(parent)
        # result = dialog.exec_()
        myFile = io.open(fileName, "r")
        _ = myFile.readline()
        _ = myFile.readline()
        try:
            line = myFile.readline()
            decodingType = line[9:-1]
            print(decodingType)
            # decodingType = str(dialog.selectionComboBox.currentText())
            if decodingType == 'Goldman':
                return 2
            elif decodingType == 'Golay':
                return 3
            return -1
        except:
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
        
        actionType = getActionType(self.actionType,linkToFile)
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
            input_details = TakeComment()
            if(input_details):
                encodedData = BarCode.hash_to_13_digits(input_details[2] + str(time.time()))
                QRCode.generateQR("File name: " + os.path.basename(fileName) + "\nName: " + input_details[0] + "\nEmail: " + input_details[1] + "\nMobile Number: " + input_details[2] + "\nSample ID: " + encodedData, fileNameWithoutExtension)
                BarCode.generateBarcode(str(encodedData), fileNameWithoutExtension)

                self.thread = EncodeThread(fileName, encodingType)
            else:
                return
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
    def __init__(self, parent=None):
        super(MainUI, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.encodeUI = ActionUI(self, 'E')
        self.decodeUI = ActionUI(self, 'D')

        layout = QHBoxLayout()
        layout.addWidget(self.encodeUI, 1)
        layout.addWidget(self.decodeUI, 1)
        self.setLayout(layout)


# This object represents main GUI of application will all menus like FILE,ABOUT etc...
class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle('DNA 3.2')
        self.setWindowIcon(QIcon("DNA_icon-8.png"))
        self.initUI()

    def initUI(self):
        self.main_widget = MainUI()
        self.setCentralWidget(self.main_widget)

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
        self.clusterAction = QAction('&Clustering error correction', self)
        # self.clusterAction.setShortcut('Ctrl')
        self.clusterAction.setStatusTip('Clustering error correcting code')
        self.clusterAction.triggered.connect(self.cluster)

    #	self.barcodeGeneratorAction = QAction('&Generate Barcode',self)
    #	self.barcodeGeneratorAction.setStatusTip('Generate Barcode')
    #	self.barcodeGeneratorAction.triggered.connect(self.showBarcode)

    # Tools menu creation
        toolsMenu = menubar.addMenu('&Tools')
        toolsMenu.addAction(self.storageEstimatorAction)
        toolsMenu.addAction(self.costEstimatorAction)
    #	toolsMenu.addAction(self.barcodeGeneratorAction)
        toolsMenu.addAction(self.clusterAction)

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

        self.statusBar().showMessage(
            "Drag and drop on left to encode file or on right to decode file")
        self.setStyleSheet("background-color: rgb(238,203,178)")

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

    def cluster(self):
        openfile = QFileDialog.getOpenFileName(self)[0]
        x = Error_Detection_Correction.Cluster(openfile)
        if(x.clusterFun() == 1):
            show_success_popup()
        else:
            Error("Error occured!!")

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
            "https://drive.google.com/drive/folders/1iNodqe0ZBzkXpIeKAwVlgVoffA-3vuRJ?usp=sharing", new=2)

    def showProduct_Demo(self):
        webbrowser.open(
            "https://drive.google.com/drive/folders/1iNodqe0ZBzkXpIeKAwVlgVoffA-3vuRJ?usp=sharing", new=2)

    def showProduct_Feedback(self):
        webbrowser.open("https://forms.gle/jTY8FcgKeWrosqZ1A", new=2)

    def showCredits(self):
        webbrowser.open(
            "https://drive.google.com/drive/folders/1iNodqe0ZBzkXpIeKAwVlgVoffA-3vuRJ?usp=sharing", new=2)

    def showAbout_Us(self):
        webbrowser.open(
            "https://www.guptalab.org/dnacloud/", new=2)


app = QApplication(sys.argv)
dna3Win = MainWindow()
dna3Win.showMaximized()
app.exec_()
