import sqlite3
from datetime import datetime

DB_NAME = "face_attendance.db"

# ================= DATABASE CONNECTION =================
def get_connection():
    return sqlite3.connect(DB_NAME)


# ================= CREATE TABLES =================
def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    # Student Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        roll TEXT,
        class TEXT
    )
    """)

    # Attendance Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS attendance (
        id Text PRIMARY KEY ,
        student_id INTEGER,
        name TEXT,
        date TEXT,
        time TEXT,
        UNIQUE(student_id, date)
    )
    """)



    # Schedule Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS schedule (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject TEXT,
        date TEXT,
        start_time TEXT,
        end_time TEXT
    )
    """)


    conn.commit()
    conn.close()
# ================= ADD STUDENT =================
def add_student(student_id, name, roll, student_class):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT OR REPLACE INTO students (id, name, roll, class)
    VALUES (?, ?, ?, ?)
    """, (student_id, name, roll, student_class))

    conn.commit()
    conn.close()


# ================= GET ALL STUDENTS =================
def get_all_students():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()

    conn.close()
    return rows




# ================= DELETE STUDENT =================
def delete_student(student_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM students WHERE id=?", (student_id,))
    conn.commit()
    conn.close()


# ================= MARK ATTENDANCE =================
def mark_attendance(student_id, name):
    conn = get_connection()
    cursor = conn.cursor()

    now = datetime.now()
    date_today = now.strftime("%Y-%m-%d")
    time_now = now.strftime("%H:%M:%S")

    try:
        cursor.execute("""
        INSERT INTO attendance (student_id, name, date, time)
        VALUES (?, ?, ?, ?)
        """, (student_id, name, date_today, time_now))
    except:
        # Ignore duplicate attendance
        pass

    conn.commit()
    conn.close()


# ================= GET ATTENDANCE =================
def get_attendance():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM attendance")
    rows = cursor.fetchall()

    conn.close()
    return rows


def get_student(student_id):
    conn = sqlite3.connect("face_attendance.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students WHERE id=?", (student_id,))
    data = cursor.fetchone()

    conn.close()
    return data


def delete_attendance(student_id):
    import sqlite3
    conn = sqlite3.connect("face_attendance.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM attendance WHERE student_id=?", (student_id,))

    conn.commit()
    conn.close()


def delete_attendance_by_date(student_id, date):
    import sqlite3
    conn = sqlite3.connect("face_attendance.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM attendance WHERE student_id=? AND date=?", (student_id, date))

    conn.commit()
    conn.close()


def delete_student(student_id):
    import sqlite3
    conn = sqlite3.connect("face_attendance.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM students WHERE id=?", (student_id,))

    conn.commit()
    conn.close()

def get_total_classes():
    import sqlite3
    conn = sqlite3.connect("face_attendance.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM schedule")
    total = cursor.fetchone()[0]

    conn.close()
    return total

def insert_default_schedule():
    import sqlite3
    from datetime import datetime, timedelta

    conn = sqlite3.connect("face_attendance.db")
    cursor = conn.cursor()

    # Clear old schedule (optional but safe for testing)
    cursor.execute("DELETE FROM schedule")

    start_date = datetime.now()

    for i in range(5):  # 5 days
        day = (start_date + timedelta(days=i)).strftime("%Y-%m-%d")

        # First class (10:00 - 11:00)
        cursor.execute("""
        INSERT INTO schedule (subject, date, start_time, end_time)
        VALUES (?, ?, ?, ?)
        """, ("Subject 1", day, "10:00", "11:00"))

        # Second class (15:00 - 16:00)
        cursor.execute("""
        INSERT INTO schedule (subject, date, start_time, end_time)
        VALUES (?, ?, ?, ?)
        """, ("Subject 2", day, "15:00", "16:00"))

    conn.commit()
    conn.close()

    print("✅ Schedule created: 5 days, 2 classes/day")