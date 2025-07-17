import sqlite3
from PyQt5.QtWidgets import QMessageBox
from database import connect_db

class StudentLogic:
    def __init__(self, main_window):
        self.main_window = main_window
        self.ui = main_window.ui

        self.ui.auth_btn_student.clicked.connect(self.login_student)
        self.ui.reg_btn.clicked.connect(self.register_student)

    def show_message(self, title, text, icon=QMessageBox.Warning):
        msg = QMessageBox(self.main_window)
        msg.setIcon(icon)
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #2c003e;
                color: white;
                font: bold 12pt 'Arial';
                border: 2px solid #9900cc;}
                
            QPushButton {
                background-color: #9900cc;
                color: white;
                border-radius: 5px;
                padding: 5px 15px;}
                
            QPushButton:hover {background-color: #cc33ff;}""")

        msg.exec_()

    def login_student(self):
        personal_id = self.ui.id_input.text()
        password = self.ui.pass_input_student.text()

        if not self.is_valid_personal_id(personal_id):
            self.show_message("შეცდომა", "პირადი ნომერი უნდა შეიცავდეს მხოლოდ 11 ციფრს.")
            return

        try:
            conn = connect_db()
            cur = conn.cursor()
            cur.execute("SELECT * FROM students WHERE personal_id=? AND password=?", (personal_id, password))
            if cur.fetchone():
                self.ui.stackedWidget.setCurrentWidget(self.ui.student_profile)
            else:
                self.show_message("შეცდომა", "არასწორი მონაცემები.")
        except Exception as e:
            self.show_message("ბაზის შეცდომა", f"დაფიქსირდა ბაზის შეცდომა: {e}", QMessageBox.Critical)
        finally:
            conn.close()

    def register_student(self):
        personal_id = self.ui.id_input.text()
        password = self.ui.pass_input_student.text()

        if not self.is_valid_personal_id(personal_id):
            self.show_message("შეცდომა", "პირადი ნომერი უნდა შეიცავდეს მხოლოდ 11 ციფრს.")
            return

        if not all([personal_id, password]):
            self.show_message("შეცდომა", "ყველა ველი სავალდებულოა.")
            return

        try:
            conn = connect_db()
            cur = conn.cursor()
            cur.execute("INSERT INTO students (personal_id, password) VALUES (?, ?)", (personal_id, password))
            conn.commit()
            self.show_message("წარმატება", "სტუდენტი რეგისტრირებულია.", QMessageBox.Information)
            self.login_student()
        except sqlite3.IntegrityError:
            self.show_message("შეცდომა", "ეს პირადი ნომერი უკვე რეგისტრირებულია.")
        except Exception as e:
            self.show_message("შეცდომა", f"დაფიქსირდა შეცდომა: {e}", QMessageBox.Critical)
        finally:
            conn.close()

    def is_valid_personal_id(self, personal_id):
        return personal_id.isdigit() and len(personal_id) == 11


class Student:
    def __init__(self, name, surname, age, id, password):
        self.name = name
        self.surname = surname
        self.age = age
        self.id = id
        self.password = password

    def stud_tuple(self):
        return (self.name, self.surname, self.age, self.id, self.password)


class Students_Crud:
    def __init__(self, db="unihub_app.db"):
        self.conn = sqlite3.connect(db)
        self.cursor = self.conn.cursor()

    def Uni_list(self, student):
        IDs = self.cursor.execute(f"SELECT uni FROM choice_{student.id}").fetchall()
        s = set()
        for i in IDs:
            s.add(self.cursor.execute(f"""SELECT uni_id, places, faculty, name FROM universities
                WHERE uni_id={i[0]}""").fetchall()[0])
        for i in s:
            print(i[0], i[1], i[2], i[3])

    def insert_student(self, student: Student):
        # აქ იქნება ექსეპშენი, სტუდენტი თუ უკვე დარეგისტრირებულია
        self.cursor.execute("""INSERT OR IGNORE INTO students (name, surname, year, personal_id, password)
            VALUES (?, ?, ?, ?, ?)""", student.stud_tuple())
        self.cursor.execute(f"""CREATE TABLE IF NOT EXISTS choice_{student.id}
            (id INTEGER PRIMARY KEY AUTOINCREMENT, uni INTEGER);""")
        self.conn.commit()

    def insert_choice(self, id, uni):
        self.cursor.execute(f"INSERT OR IGNORE INTO choice_{id} (uni) VALUES(?)", uni)
        self.conn.commit()

    def remove_choice(self, id, uni):
        self.cursor.execute(f"DELETE FROM choice_{id} WHERE uni=?", uni)
        self.conn.commit()

    def remove_student(self, id):
        self.cursor.execute(f"DELETE FROM students WHERE personal_id={id}")
        self.cursor.execute(f"DROP TABLE IF EXISTS choice_{id}")
        self.conn.commit()
