import os
import cv2
from tkinter import *
from tkinter import ttk, messagebox
import db


class Student:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Management")
        self.root.geometry("900x600")

        db.create_tables()

        # Variables
        self.var_id = StringVar()
        self.var_name = StringVar()
        self.var_roll = StringVar()
        self.var_class = StringVar()

        # Title
        Label(self.root, text="Student Management System",
              font=("Arial", 20, "bold")).pack(pady=10)

        # Form Frame
        form = Frame(self.root)
        form.pack(pady=20)

        Label(form, text="ID").grid(row=0, column=0, padx=10, pady=5)
        Entry(form, textvariable=self.var_id).grid(row=0, column=1)

        Label(form, text="Name").grid(row=1, column=0, padx=10, pady=5)
        Entry(form, textvariable=self.var_name).grid(row=1, column=1)

        Label(form, text="Roll").grid(row=2, column=0, padx=10, pady=5)
        Entry(form, textvariable=self.var_roll).grid(row=2, column=1)

        Label(form, text="Class").grid(row=3, column=0, padx=10, pady=5)
        Entry(form, textvariable=self.var_class).grid(row=3, column=1)

        # Buttons
        Button(form, text="Add", command=self.add_data, bg="green", fg="white").grid(row=4, column=0, pady=10)
        Button(form, text="Delete", command=self.delete_data, bg="red", fg="white").grid(row=4, column=1)

        Button(self.root, text="Capture Face Dataset", command=self.generate_dataset,
               bg="blue", fg="white").pack(pady=10)
        
        # ===== Search Section =====
        search_frame = Frame(self.root, bg="white")
        search_frame.pack(pady=10)

        Label(search_frame, text="Search ID:", bg="white").grid(row=0, column=0, padx=5)

        self.search_var = StringVar()
        Entry(search_frame, textvariable=self.search_var).grid(row=0, column=1, padx=5)

        Button(search_frame, text="Search",
            command=self.search_student,
            bg="blue", fg="white").grid(row=0, column=2, padx=5)

        # Table
        self.table = ttk.Treeview(self.root, columns=("ID", "Name", "Roll", "Class"), show="headings")
        for col in ("ID", "Name", "Roll", "Class"):
            self.table.heading(col, text=col)


        self.table.pack(fill=BOTH, expand=1)

        self.load_data()

    # ================= ADD =================
    def add_data(self):
        if not self.var_id.get() or not self.var_name.get():
            messagebox.showerror("Error", "ID and Name required")
            return

        db.add_student(
            self.var_id.get(),
            self.var_name.get(),
            self.var_roll.get(),
            self.var_class.get()
        )

        self.load_data()
        messagebox.showinfo("Success", "Student Added")

    # ================= LOAD =================
    def load_data(self):
        for row in self.table.get_children():
            self.table.delete(row)

        for row in db.get_all_students():
            self.table.insert("", END, values=row)

    # ================= DELETE =================
    # def delete_data(self):
    #     selected = self.table.focus()
    #     if not selected:
    #         return

    #     values = self.table.item(selected, "values")
    #     db.delete_student(values[0])

    #     self.load_data()

    def delete_data(self):
        import db
        import os
        from tkinter import messagebox

        student_id = self.var_id.get()

        if not student_id:
            messagebox.showerror("Error", "Select student first")
            return

        confirm = messagebox.askyesno("Confirm Delete",
                                 "Delete student and ALL related data?")

        if not confirm:
            return

        # Delete student
        db.delete_student(student_id)

        # Delete attendance
        db.delete_attendance(student_id)

        # Delete images
        data_path = "data"
        for file in os.listdir(data_path):
            if file.startswith(f"user.{student_id}."):
                os.remove(os.path.join(data_path, file))

        messagebox.showinfo("Success", "Student deleted successfully")
    # Optional: refresh table if needed

    
    # ================= DATASET =================
    def generate_dataset(self):
        if not self.var_id.get():
            messagebox.showerror("Error", "Enter Student ID first")
            return

        face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

        def face_cropped(img):
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_classifier.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                return img[y:y+h, x:x+w]
            return None

        cap = cv2.VideoCapture(0)
        img_id = 0

        if not os.path.exists("data"):
            os.makedirs("data")

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            face = face_cropped(frame)
            if face is not None:
                img_id += 1
                face = cv2.resize(face, (450, 450))
                face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)

                file_path = f"data/user.{self.var_id.get()}.{img_id}.jpg"
                cv2.imwrite(file_path, face)

                cv2.putText(face, str(img_id), (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

                cv2.imshow("Capturing Faces", face)

            if cv2.waitKey(1) == 13 or img_id == 50:
                break

        cap.release()
        cv2.destroyAllWindows()

        messagebox.showinfo("Done", "Dataset Captured Successfully")

    def search_student(self):
        student_id = self.search_var.get()

        if not student_id:
            messagebox.showerror("Error", "Enter ID to search")
            return

        data = db.get_student(student_id)

        if data:
            self.var_id.set(data[0])      # ✅ FIXED
            self.var_name.set(data[1])
            self.var_roll.set(data[2])
            self.var_class.set(data[3])
        else:
            messagebox.showerror("Error", "Student not found")



# Run standalone
if __name__ == "__main__":
    root = Tk()
    app = Student(root)
    root.mainloop()