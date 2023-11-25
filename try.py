import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox

class PopupExample(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Popup Example')

        self.btn_show_error = QPushButton('Show Error', self)
        self.btn_show_error.setGeometry(20, 20, 120, 40)
        self.btn_show_error.clicked.connect(self.show_error_popup)

        self.btn_show_success = QPushButton('Show Success', self)
        self.btn_show_success.setGeometry(160, 20, 120, 40)
        self.btn_show_success.clicked.connect(self.show_success_popup)

        self.show()

    def show_error_popup(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle('Error')
        msg.setText('An error occurred!')
        msg.exec_()

    def show_success_popup(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle('Success')
        msg.setText('Operation successful!')
        msg.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PopupExample()
    sys.exit(app.exec_())
