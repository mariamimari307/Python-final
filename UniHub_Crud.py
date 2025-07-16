import sqlite3
class student:
    def __init__(self,name,surname,age,id,password):
        self.name = name
        self.surname = surname
        self.age = age
        self.id =id
        self.password = password
    def stud_tuple(self):
        return (self.name,self.surname,self.age,self.id,self.password)
# aqac egre
class Students_Crud:
    def __init__(self,db="unihub_app.db"):
        self.conn = sqlite3.connect(db)
        self.cursor = self.conn.cursor()

    def Uni_list(self,student):
        IDs = self.cursor.execute(f"SELECT uni FROM choice_{student.id}").fetchall()
        s = set()
        for i in IDs:
            s.add(self.cursor.execute(f"""SELECT uni_id,places,faculty,name FROM universities
            WHERE uni_id={i[0]}""").fetchall()[0])
        for i in s:
            print(i[0],i[1],i[2],i[3])
    def insert_student(self,student:student):
        # აქ იქნება ექსეპშენი, სტუდენტი თუ უკვე დარეგისტრირებულია
        self.cursor.execute(""" INSERT OR IGNORE INTO students (name,surname,year,personal_id,password)
        VALUES(?,?,?,?,?)
    """,student.stud_tuple())
        self.cursor.execute(f"""CREATE TABLE IF NOT EXISTS choice_{student.id}
            (id INTEGER PRIMARY KEY AUTOINCREMENT,uni INTEGER);""")
        self.conn.commit()
    def insert_choice(self,id,uni):
        self.cursor.execute(f"INSERT OR IGNORE INTO choice_{id} (uni) VALUES(?)",uni)
        self.conn.commit()
    def remove_choice(self,id,uni):
        self.cursor.execute(f"DELETE FROM choice_{id} WHERE uni=? ",uni)
        self.conn.commit()
    def remove_student(self,id):
        self.cursor.execute(f"DELETE FROM students WHERE personal_id={id}",)
        self.cursor.execute(f"DROP TABLE IF EXISTS choice_{id}")
        self.conn.commit()


# aq yvelaferi mushaobs
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









