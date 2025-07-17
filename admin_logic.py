import sqlite3
from PyQt5.QtWidgets import QMessageBox
from database import connect_db

class AdminLogic:
    def __init__(self, main_window):
        self.main_window = main_window
        self.ui = main_window.ui

        self.ui.auth_btn_admin.clicked.connect(self.login_admin)
        self.ui.add_btn_admin.clicked.connect(self.add_university)
        

    def login_admin(self):
        username = self.ui.name_input.text()
        password = self.ui.pass_input_admin.text()
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM admin WHERE username=? AND password=?", (username, password))
        if cur.fetchone():
            self.ui.stackedWidget.setCurrentWidget(self.ui.admin_base)
        else:
            QMessageBox.warning(self.main_window, "შეცდომა", "არასწორი მონაცემები.")
        conn.close()

    def select_university(self):
        id = self.ui.uni_input_admin_2.text()
        if not id:
            QMessageBox.warning(self.main_window, "შეცდომა", "უნივერსიტეტის სახელი უნდა იყოს მითითებული.")
            return
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM universities WHERE name=?", (id,))
        university = cur.fetchone()
        if university:
            self.ui.faculty_input_admin.setText(university[2])
            self.ui.count_input_admin.setText(str(university[5]))
        else:
            QMessageBox.warning(self.main_window, "შეცდომა", "უნივერსიტეტი ვერ მოიძებნა.")
        conn.close()

    def add_university(self):
        id = self.ui.uni_input_admin_2.text()
        name = self.ui.uni_input_admin.text()
        faculty = self.ui.faculty_input_admin.text()
        count = self.ui.count_input_admin.text()
        if not all([id, name, faculty, count]):
            QMessageBox.warning(self.main_window, "შეცდომა", "ყველა ველი სავალდებულოა.")
            return
        conn = connect_db()
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO universities (uni_id,name,faculty,places) VALUES (?,?,?,?)",
                        (id, name, faculty, count))
            conn.commit()
            QMessageBox.information(self.main_window, "წარმატება", "უნივერსიტეტი დამატებულია.")
            self.ui.uni_input_admin_2.clear()
            self.ui.uni_input_admin.clear()
            self.ui.faculty_input_admin.clear()
            self.ui.count_input_admin.clear()
        except Exception as e:
            QMessageBox.warning(self.main_window, "შეცდომა", f"დაფიქსირდა შეცდომა: {e}")
        finally:
            conn.close()

    def delete_university(self):
        id = self.ui.uni_input_admin_2.text()
        if not id:
            QMessageBox.warning(self.main_window, "შეცდომა", "უნივერსიტეტის სახელი უნდა იყოს მითითებული.")
            return
        conn = connect_db()
        cur = conn.cursor()
        try:
            cur.execute("DELETE FROM universities WHERE uni_id=?", (id,))
            conn.commit()
            QMessageBox.information(self.main_window, "წარმატება", "უნივერსიტეტი წაშლილია.")
            self.ui.uni_input_admin_2.clear()
        except Exception as e:
            QMessageBox.warning(self.main_window, "შეცდომა", f"დაფიქსირდა შეცდომა: {e}")
        finally:
            conn.close()

    def update_university(self):
        id = self.ui.uni_input_admin_2.text()
        name = self.ui.uni_input_admin.text()
        faculty = self.ui.faculty_input_admin.text()
        count = self.ui.count_input_admin.text()
        if not all([id, name, faculty, count]):
            QMessageBox.warning(self.main_window, "შეცდომა", "ყველა ველი სავალდებულოა.")
            return
        conn = connect_db()
        cur = conn.cursor() 
        try:
            cur.execute("UPDATE universities SET (uni_id, name, faculty, places) = (?, ?, ?, ?) WHERE uni_id=?",(id, name, faculty, count))
            conn.commit()
            QMessageBox.information(self.main_window, "წარმატება", "უნივერსიტეტი განახლებულია.")
            self.ui.uni_input_admin.clear()
            self.ui.faculty_input_admin.clear()
            self.ui.count_input_admin.clear()
        except Exception as e:
            QMessageBox.warning(self.main_window, "შეცდომა", f"დაფიქსირდა შეცდომა: {e}")
        finally:
            conn.close()

class University_Crud:
    def __init__(self,db="unihub_app.db"):
        self.conn = sqlite3.connect(db)
        self.cursor = self.conn.cursor()
    def add_uni(self,uni):
        self.cursor.execute("""
        INSERT INTO universities (uni_id,name,faculty,credits,price,places)
        VALUES(?,?,?,?,?,?)
        """,uni)
        self.conn.commit()
    def update_uni(self,uni):
        self.cursor.execute("""
        UPDATE universities SET name=?,faculty=?,credits=?,price=?,places=?
        WHERE uni_id=?""",uni)
        self.conn.commit()
    def remove_uni(self,id):
        self.cursor.execute(f"""
        DELETE FROM universities WHERE uni_id={id}""")
        self.conn.commit()
    def Load_unis(self):
        listi = self.cursor.execute("SELECT uni_id,places,faculty,name FROM universities").fetchall()
        for i in listi:
            print(i)
