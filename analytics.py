import sqlite3
from tkinter import *
from tkinter import ttk


class Analytics:
    def __init__(self, root):
        self.root = root
        self.root.title("Analytics Dashboard")
        self.root.geometry("900x600")
        self.root.configure(bg="#f5f7fa")

        title = Label(self.root, text="Analytics Dashboard",
                      font=("Arial", 22, "bold"),
                      bg="#f5f7fa", fg="#2c3e50")
        title.pack(pady=20)

        # ===== Top Cards Frame =====
        card_frame = Frame(self.root, bg="#f5f7fa")
        card_frame.pack(pady=10)

        self.total_students = self.get_total_students()
        self.total_attendance = self.get_total_attendance()

        self.create_card(card_frame, "Total Students", self.total_students, 0)
        self.create_card(card_frame, "Total Attendance", self.total_attendance, 1)

        # ===== Table Frame =====
        table_frame = Frame(self.root, bg="white", bd=2, relief=RIDGE)
        table_frame.pack(pady=20, padx=20, fill=BOTH, expand=True)

        Label(table_frame, text="Attendance Records",
              font=("Arial", 16, "bold"),
              bg="white").pack(pady=10)

        columns = ("ID", "Name", "Date", "Time")

        self.table = ttk.Treeview(table_frame, columns=columns, show="headings")

        for col in columns:
            self.table.heading(col, text=col)
            self.table.column(col, anchor=CENTER)

        self.table.pack(fill=BOTH, expand=True)

        # ===== Individual Student Report =====
        report_frame = Frame(self.root, bg="#f5f7fa")
        report_frame.pack(pady=10)

        Label(report_frame, text="Student ID:", bg="#f5f7fa").grid(row=0, column=0, padx=5)

        self.report_id = Entry(report_frame)
        self.report_id.grid(row=0, column=1, padx=5)

        Button(report_frame, text="Show Report",
            command=self.show_report,
            bg="blue", fg="white").grid(row=0, column=2, padx=10)

        # Delete Section

        delete_frame = Frame(self.root, bg="#f5f7fa")
        delete_frame.pack(pady=10)

        Label(delete_frame, text="Student ID:", bg="#f5f7fa").grid(row=0, column=0, padx=5)

        self.delete_id = Entry(delete_frame)
        self.delete_id.grid(row=0, column=1, padx=5)

        Label(delete_frame, text="Date (YYYY-MM-DD):", bg="#f5f7fa").grid(row=1, column=0, padx=5)

        self.delete_date = Entry(delete_frame)
        
        self.delete_date.grid(row=1, column=1, padx=5)

        Button(delete_frame, text="Delete Attendance",
            command=self.delete_attendance,
            bg="red", fg="white").grid(row=0, column=2, padx=10)

        self.load_attendance()

    # ===== Card UI =====
    def create_card(self, parent, title, value, col):
        card = Frame(parent, bg="white", bd=2, relief=RIDGE, width=200, height=100)
        card.grid(row=0, column=col, padx=20)

        Label(card, text=title, font=("Arial", 12, "bold"),
              bg="white").pack(pady=10)

        Label(card, text=str(value), font=("Arial", 20, "bold"),
              fg="#27ae60", bg="white").pack()

    # ===== DB Functions =====


    def get_total_students(self):
        conn = sqlite3.connect("face_attendance.db")
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM students")
        count = cursor.fetchone()[0]
        conn.close()
        return count

    def get_total_attendance(self):
        conn = sqlite3.connect("face_attendance.db")
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM attendance")
        count = cursor.fetchone()[0]
        conn.close()
        return count

    def load_attendance(self):
        conn = sqlite3.connect("face_attendance.db")
        cursor = conn.cursor()

        cursor.execute("SELECT student_id, name, date, time FROM attendance ORDER BY date DESC")

        rows = cursor.fetchall()
        conn.close()

        for row in rows:
            self.table.insert("", END, values=row)

    def delete_attendance(self):

        import db
        from tkinter import messagebox

        student_id = self.delete_id.get().strip()
        date = self.delete_date.get().strip() if hasattr(self, 'delete_date') else None

        if not student_id:
            messagebox.showerror("Error", "Enter Student ID")
            return

        if date:
            db.delete_attendance_by_date(student_id, date)
            messagebox.showinfo("Success", f"Attendance deleted for {student_id} on {date}")
        else:
            db.delete_attendance(student_id)
            messagebox.showinfo("Success", f"All attendance deleted for {student_id}")

        # Refresh table
        for row in self.table.get_children():
            self.table.delete(row)

        self.load_attendance()

    
    def show_report(self):
        student_id = self.search_var.get()

        if not student_id:
            from tkinter import messagebox
            messagebox.showerror("Error", "Enter Student ID")
            return

        import sqlite3
        conn = sqlite3.connect("face_attendance.db")
        cursor = conn.cursor()

        cursor.execute("""
            SELECT student_id, name, date, time 
            FROM attendance 
            WHERE student_id=?
        """, (student_id,))

        rows = cursor.fetchall()
        conn.close()

        # CLEAR TABLE
        for item in self.table.get_children():
            self.table.delete(item)

        # INSERT NEW DATA
        for row in rows:
            self.table.insert("", "end", values=row)

        if not rows:
            from tkinter import messagebox
            messagebox.showinfo("Result", "No attendance found")


# Run standalone
if __name__ == "__main__":
    root = Tk()
    app = Analytics(root)
    root.mainloop()