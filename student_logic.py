import sqlite3
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtWidgets

from database import connect_db

class StudentLogic:
    def __init__(self, main_window):
        self.main_window = main_window
        self.ui = main_window.ui
        self.students_crud = Students_Crud(self.ui)

        self.ui.auth_btn_student.clicked.connect(self.login_student)
        self.ui.reg_btn.clicked.connect(self.register_student)


    def login_student(self):
        personal_id = self.ui.id_input.text()
        password = self.ui.pass_input_student.text()
        if not self.is_valid_personal_id(personal_id):
            QMessageBox.warning(self.main_window, "შეცდომა", "პირადი ნომერი უნდა შეიცავდეს 11 ციფრს.")
            return
        try:
            conn = connect_db()
            cur = conn.cursor()
            cur.execute("SELECT * FROM students WHERE personal_id=? AND password=?", (personal_id, password))
            if cur.fetchone():
                self.ui.stackedWidget.setCurrentWidget(self.ui.student_profile)
                self.ui.id_label_student_2.setText(personal_id)
                self.load_universities_to_combo()
                self.students_crud._load_choices_to_table()
                cur.execute(f"""CREATE TABLE IF NOT EXISTS choice_{personal_id} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    uni INTEGER UNIQUE
                    )""")

            else:
                QMessageBox.warning(self.main_window, "შეცდომა", "არასწორი მონაცემები.")
        except Exception as e:
            QMessageBox.critical(self.main_window, "ბაზის შეცდომა", f"დაფიქსირდა ბაზის შეცდომა: {e}")
        finally:
            conn.close()

    def register_student(self):
        personal_id = self.ui.id_input.text()
        password = self.ui.pass_input_student.text()

        if not self.is_valid_personal_id(personal_id):
            QMessageBox.warning(self.main_window, "შეცდომა", "პირადი ნომერი უნდა შეიცავდეს 11 ციფრს.")
            return
        if not all([personal_id, password]):
            QMessageBox.warning(self.main_window, "შეცდომა", "ყველა ველი სავალდებულოა.")
            return
        try:
            conn = connect_db()
            cur = conn.cursor()
            cur.execute("INSERT INTO students (personal_id, password) VALUES (?, ?)", (personal_id, password))
            conn.commit()
            QMessageBox.information(self.main_window, "წარმატება", "სტუდენტი რეგისტრირებულია.")
            self.login_student()
        except sqlite3.IntegrityError:
            QMessageBox.warning(self.main_window, "შეცდომა", "ეს პირადი ნომერი უკვე რეგისტრირებულია.")
        except Exception as e:
            QMessageBox.critical(self.main_window, "შეცდომა", f"დაფიქსირდა შეცდომა: {e}")
        finally:
            conn.close()

    def is_valid_personal_id(self, personal_id):
        return personal_id.isdigit() and len(personal_id) == 11
    
    def load_universities_to_combo(self):
        try:
            conn = connect_db()
            cur = conn.cursor()
            cur.execute("SELECT uni_id, name FROM universities")
            universities = cur.fetchall()

            self.ui.uni_combo.clear()

            for uni_id, name in universities:
                self.ui.uni_combo.addItem(f"{uni_id} ({name})", uni_id) 

        except Exception as e:
            QMessageBox.warning(self.main_window, "შეცდომა", f"უნივერსიტეტების ჩატვირთვის შეცდომა: {e}")
        finally:
            conn.close()


class Student:
    def __init__(self,id,password):
        self.id =id
        self.password = password
    def stud_tuple(self):
        return (self.id,self.password)

class Students_Crud:
    def __init__(self, ui, db="unihub_app.db"):
        self.ui = ui
        self.conn = sqlite3.connect(db)
        self.cursor = self.conn.cursor()
        
        self.ui.add_btn_student.clicked.connect(self._insert_choice) 
        self.ui.del_btn_student.clicked.connect(self._remove_choice)

    def _insert_choice(self):
        personal_id = self.ui.id_input.text() 
        index = self.ui.uni_combo.currentIndex() 
        uni_id = self.ui.uni_combo.itemData(index) 

        try:
            self.insert_choice(personal_id, (uni_id,))
            QMessageBox.information(None, "წარმატება", "დაემატა არჩევანი")
            self._load_choices_to_table()
        except Exception as e:
            QMessageBox.warning(None, "შეცდომა", str(e))

    def insert_choice(self, id, uni):
        self.cursor.execute(f"INSERT OR IGNORE INTO choice_{id} (uni) VALUES(?)", uni) 
        self.conn.commit() 

    def _load_choices_to_table(self):
        personal_id = self.ui.id_input.text()

        try:
            self.cursor.execute(f"""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name=?
            """, (f"choice_{personal_id}",))
            table_exists = self.cursor.fetchone()

            if not table_exists:
                return  

            self.ui.priority_table.setRowCount(0)

            results = self.cursor.execute(f"""
                SELECT u.uni_id, u.places, u.faculty, u.name
                FROM universities u
                JOIN choice_{personal_id} c ON u.uni_id = c.uni
                ORDER BY c.id ASC
            """).fetchall()

            for row_idx, row_data in enumerate(results):
                self.ui.priority_table.insertRow(row_idx)
                for col_idx, value in enumerate(row_data):
                    item = QtWidgets.QTableWidgetItem(str(value))
                    self.ui.priority_table.setItem(row_idx, col_idx, item)

        except Exception as e:
            QMessageBox.warning(None, "შეცდომა", f"ცხრილის განახლება ვერ მოხერხდა: {e}")

    def _remove_choice(self):
        personal_id = self.ui.id_input.text()
        row = self.ui.priority_table.currentRow()

        if row == -1:
            QMessageBox.warning(None, "შეცდომა", "აირჩიე წასაშლელი ჩანაწერი.")
            return

        uni_id_item = self.ui.priority_table.item(row, 0)   
        if uni_id_item is None:                             
            QMessageBox.warning(None, "შეცდომა", "ვერ მოიძებნა იდენტიფიკატორი.")
            return

        uni_id = uni_id_item.text()

        try:
            self.remove_choice(personal_id, (uni_id,))
            QMessageBox.information(None, "წარმატება", "წაიშალა არჩევანი.")
            self._load_choices_to_table()  
        except Exception as e:
            QMessageBox.warning(None, "შეცდომა", f"წაშლის შეცდომა: {e}")

    def remove_choice(self, id, uni):
        self.cursor.execute(f"DELETE FROM choice_{id} WHERE uni=?", uni)
        self.conn.commit()
