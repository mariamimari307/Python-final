import sqlite3
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem
from database import connect_db


class AdminLogic:
    def __init__(self, main_window):
        self.main_window = main_window
        self.ui = main_window.ui

        self.ui.auth_btn_admin.clicked.connect(self.login_admin)
        self.ui.add_btn_admin.clicked.connect(self.add_university)
        self.ui.del_btn_admin.clicked.connect(self.delete_university)
        self.ui.renew_btn_admin.clicked.connect(self.update_university)

        self.load_priority_table()

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
            QPushButton:hover {background-color: #cc33ff;}
        """)
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
                self.load_priority_table()
            else:
                self.show_message("შეცდომა", "არასწორი მონაცემები.")
        except Exception as e:
            self.show_message("ბაზის შეცდომა", f"შეცდომა: {e}", QMessageBox.Critical)
        finally:
            conn.close()

    def load_priority_table(self):
        try:
            conn = connect_db()
            cur = conn.cursor()
            cur.execute("SELECT uni_id, name, faculty, places FROM universities")
            rows = cur.fetchall()
            self.ui.priority_table_2.setRowCount(0)
            for row_number, row_data in enumerate(rows):
                self.ui.priority_table_2.insertRow(row_number)

                item_id = QTableWidgetItem(str(row_data[0]))    
                item_places = QTableWidgetItem(str(row_data[3]))   
                item_faculty = QTableWidgetItem(str(row_data[2]))  
                item_name = QTableWidgetItem(str(row_data[1]))      

                self.ui.priority_table_2.setItem(row_number, 0, item_id)
                self.ui.priority_table_2.setItem(row_number, 1, item_places)
                self.ui.priority_table_2.setItem(row_number, 2, item_faculty)
                self.ui.priority_table_2.setItem(row_number, 3, item_name)
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
            cur.execute(
                "INSERT INTO universities (uni_id, name, faculty, places) VALUES (?, ?, ?, ?)",
                (id, name, faculty, count)
            )
            conn.commit()
            self.show_message("წარმატება", "უნივერსიტეტი დამატებულია.", QMessageBox.Information)
            self.ui.uni_input_admin_2.clear()
            self.ui.uni_input_admin.clear()
            self.ui.faculty_input_admin.clear()
            self.ui.count_input_admin.clear()
            self.load_priority_table() 
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
                self.load_priority_table() 
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
        try:
            conn = connect_db()
            cur = conn.cursor()
            cur.execute(
                "UPDATE universities SET name=?, faculty=?, places=? WHERE uni_id=?",
                (name, faculty, count, id)
            )
            conn.commit()
            self.show_message("წარმატება", "უნივერსიტეტი განახლებულია.", QMessageBox.Information)
            self.ui.uni_input_admin_2.clear()
            self.ui.uni_input_admin.clear()
            self.ui.faculty_input_admin.clear()
            self.ui.count_input_admin.clear()
            self.load_priority_table() 
        except Exception as e:
            self.show_message("შეცდომა", f"დაფიქსირდა შეცდომა: {e}", QMessageBox.Critical)
        finally:
            conn.close()
