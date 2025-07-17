import sqlite3
from PyQt5.QtWidgets import QMessageBox
from database import connect_db
from PyQt5 import QtWidgets


class AdminLogic:
    def __init__(self, main_window):
        self.main_window = main_window
        self.ui = main_window.ui

        self.ui.auth_btn_admin.clicked.connect(self.login_admin)
        self.ui.add_btn_admin.clicked.connect(self.add_university)
        self.ui.del_btn_admin.clicked.connect(self.delete_university)
        self.ui.renew_btn_admin.clicked.connect(self.update_university)

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
                border: 2px solid #9900cc;
            }
            QPushButton {
                background-color: #9900cc;
                color: white;
                border-radius: 5px;
                padding: 5px 15px;}
                
            QPushButton:hover {background-color: #cc33ff;}""")

        msg.exec_()

    def login_admin(self):
        username = self.ui.name_input.text()
        password = self.ui.pass_input_admin.text()
        try:
            conn = connect_db()
            cur = conn.cursor()
            cur.execute("SELECT * FROM admin WHERE username=? AND password=?", (username, password))
            if cur.fetchone():
                self.ui.stackedWidget.setCurrentWidget(self.ui.admin_base)
            else:
                self.show_message("შეცდომა", "არასწორი მონაცემები.")
        except Exception as e:
            self.show_message("ბაზის შეცდომა", f"შეცდომა: {e}", QMessageBox.Critical)
        finally:
            conn.close()

    def select_university(self):
        id = self.ui.uni_input_admin_2.text()
        if not id:
            self.show_message("შეცდომა", "უნივერსიტეტის სახელი უნდა იყოს მითითებული.")
            return
        try:
            conn = connect_db()
            cur = conn.cursor()
            cur.execute("SELECT * FROM universities WHERE name=?", (id,))
            university = cur.fetchone()
            if university:
                self.ui.faculty_input_admin.setText(university[2])
                self.ui.count_input_admin.setText(str(university[5]))
            else:
                self.show_message("შეცდომა", "უნივერსიტეტი ვერ მოიძებნა.")
        except Exception as e:
            self.show_message("შეცდომა", f"ბაზასთან კავშირის პრობლემა: {e}", QMessageBox.Critical)
        finally:
            conn.close()

    def add_university(self):
        id = self.ui.uni_input_admin_2.text()
        name = self.ui.uni_input_admin.text()
        faculty = self.ui.faculty_input_admin.text()
        count = self.ui.count_input_admin.text()
        if not all([id, name, faculty, count]):
            self.show_message("შეცდომა", "ყველა ველი სავალდებულოა.")
            return
        try:
            conn = connect_db()
            cur = conn.cursor()
            cur.execute("INSERT INTO universities (uni_id,name,faculty,places) VALUES (?,?,?,?)", (id, name, faculty, count))
            conn.commit()
            self.show_message("წარმატება", "უნივერსიტეტი დამატებულია.", QMessageBox.Information)
            self.ui.uni_input_admin_2.clear()
            self.ui.uni_input_admin.clear()
            self.ui.faculty_input_admin.clear()
            self.ui.count_input_admin.clear()
        except sqlite3.IntegrityError:
            self.show_message("შეცდომა", "ასეთი ID ან დასახელება უკვე არსებობს.")
        except Exception as e:
            self.show_message("შეცდომა", f"შეცდომა დამატებისას: {e}", QMessageBox.Critical)
        finally:
            conn.close()

    def delete_university(self):
        id = self.ui.uni_input_admin_2.text()
        if not id:
            self.show_message("შეცდომა", "უნივერსიტეტის ID უნდა იყოს მითითებული.")
            return
        try:
            conn = connect_db()
            cur = conn.cursor()
            cur.execute("DELETE FROM universities WHERE uni_id=?", (id,))
            if cur.rowcount == 0:
                self.show_message("შეტყობინება", "მონაცემი ვერ მოიძებნა.", QMessageBox.Information)
            else:
                conn.commit()
                self.show_message("წარმატება", "უნივერსიტეტი წაშლილია.", QMessageBox.Information)
                self.ui.uni_input_admin_2.clear()
        except Exception as e:
            self.show_message("შეცდომა", f"წაშლის შეცდომა: {e}", QMessageBox.Critical)
        finally:
            conn.close()

    def update_university(self):
        id = self.ui.uni_input_admin_2.text()
        name = self.ui.uni_input_admin.text()
        faculty = self.ui.faculty_input_admin.text()
        count = self.ui.count_input_admin.text()
        if not all([id, name, faculty, count]):
            self.show_message("შეცდომა", "ყველა ველი სავალდებულოა.")
            return
        conn = connect_db()
        cur = conn.cursor()
        try:
            cur.execute("UPDATE universities SET name=?, faculty=?, places=? WHERE uni_id=?", (name, faculty, count, id))
            conn.commit()
            self.show_message("წარმატება", "უნივერსიტეტი განახლებულია.", QMessageBox.Information)
            self.ui.uni_input_admin.clear()
            self.ui.faculty_input_admin.clear()
            self.ui.count_input_admin.clear()
        except Exception as e:
            self.show_message("შეცდომა", f"დაფიქსირდა შეცდომა: {e}")
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