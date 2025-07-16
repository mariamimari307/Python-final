from PyQt5.QtWidgets import QMessageBox
from database import connect_db

class StudentLogic:
    def __init__(self, main_window):
        self.main_window = main_window
        self.ui = main_window.ui

        self.ui.auth_btn_student.clicked.connect(self.login_student)
        self.ui.reg_btn.clicked.connect(self.register_student)

    def login_student(self):
        personal_id = self.ui.id_input.text()
        password = self.ui.pass_input_student.text()
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM students WHERE personal_id=? AND password=?", (personal_id, password))
        if cur.fetchone():
            self.ui.stackedWidget.setCurrentWidget(self.ui.student_profile)
        else:
            QMessageBox.warning(self.main_window, "შეცდომა", "არასწორი მონაცემები.")
        conn.close()

    def register_student(self):
        personal_id = self.ui.id_input.text()
        password = self.ui.pass_input_student.text()
        if not all([personal_id, password]):
            QMessageBox.warning(self.main_window, "შეცდომა", "ყველა ველი სავალდებულოა.")
            return
        conn = connect_db()
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO students (personal_id, password) VALUES (?, ?)",
                        (personal_id, password))
            conn.commit()
            QMessageBox.information(self.main_window, "წარმატება", "სტუდენტი რეგისტრირებულია.")
            self.login_student()
        except Exception as e:
            QMessageBox.warning(self.main_window, "შეცდომა", f"დაფიქსირდა შეცდომა: {e}")
        finally:
            conn.close()