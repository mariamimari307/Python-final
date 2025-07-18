import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget
from designQT5 import Ui_MainWindow
from admin_logic import AdminLogic
from student_logic import StudentLogic

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.stackedWidget.setCurrentWidget(self.ui.main)
        self.setWindowTitle("Welcome to UniHub!")
        self.center()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

        self.setStyleSheet ("""
            QWidget#centralwidget {
                background-color: qlineargradient(
                    spread:pad, x1:0, y1:0, x2:1, y2:1,
                    stop:0 #ff4da6, stop:1 #a64bf4);}

            QLabel {color: white;
                background: transparent;}

            QPushButton {
                background-color: rgba(255, 255, 255, 0.0);
                color: white;
                border: 1px solid #ffcfff;
                border-radius: 10px;
                padding: 8px 14px;
                font-weight: bold;}

            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.15);
                border: 1px solid white;}

            QPushButton:pressed {background-color: rgba(255, 255, 255, 0.25);}

            QLineEdit {
                background-color: rgba(255, 255, 255, 0.06);
                color: white;
                border: 1px solid #ffb3ff;
                border-radius: 8px;
                padding: 6px;}

            QLineEdit:focus {
                background-color: rgba(255, 255, 255, 0.12);
                border: 1px solid white;}
            
            QTableWidget {
                background-color: rgba(255, 255, 255, 0.92);  /* Light white */
                alternate-background-color: rgba(255, 255, 255, 0.85);
                gridline-color: #d6aaff;
                color: black;
                border: none;}

            QHeaderView::section {
                background-color: #ffb3f5;
                color: #3a004d;
                font-weight: bold;
                border: 1px solid #ffffff;
                padding: 4px;}

            QTableWidget::item {
                selection-background-color: #ff99e6;
                selection-color: black;}

            QFrame {background: transparent;}""")
        
        self.ui.stackedWidget.setCurrentWidget(self.ui.main)

        self.ui.admin_opt.clicked.connect(self.admin_login)
        self.ui.student_opt.clicked.connect(self.student_login)
        self.ui.admin_back.clicked.connect(self.options_page)
        self.ui.student_back.clicked.connect(self.options_page)
        self.ui.back_main_admin.clicked.connect(self.options_page)
        self.ui.back_main_student.clicked.connect(self.options_page)

        self.setStatusBar(None)

        self.admin_logic = AdminLogic(self)
        self.student_logic = StudentLogic(self)


    def admin_login(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.admin)
        self.setWindowTitle("ადმინის შესვლა")

    def student_login(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.student)
        self.setWindowTitle("აბიტურიენტის შესვლა")

    def student_page(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.student_profile)
        self.setWindowTitle("აბიტურიენტის პროფილი")

    def admin_page(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.admin_base)
        self.setWindowTitle("ადმინის კატალოგი")

    def options_page(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.main)
        self.setWindowTitle("Welcome to UniHub!")
        self.repaint()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
