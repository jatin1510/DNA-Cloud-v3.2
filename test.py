import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QInputDialog, QMessageBox

def get_non_empty_input():
    app = QApplication(sys.argv)
    main_window = QMainWindow()

    text, ok = QInputDialog.getText(main_window, 'Input Dialog', 'Enter a value:')

    if ok and text.strip():
        return text
    else:
        QMessageBox.warning(main_window, 'Warning', 'Please enter a non-empty value.', QMessageBox.Ok)
        return None

if __name__ == '__main__':
    value = get_non_empty_input()
    if value is not None:
        print(f'Entered value: {value}')
