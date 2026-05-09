from tkinter import *
from tkinter import messagebox


class FaceRecognitionSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Recognition Attendance System")
        self.root.geometry("900x600")
        self.root.configure(bg="#ecf0f1")

        # ===== Title =====
        title = Label(self.root,
                      text="Face Recognition Attendance System",
                      font=("Helvetica", 22, "bold"),
                      bg="#2c3e50",
                      fg="white")
        title.pack(fill=X)

        # ===== Button Frame =====
        btn_frame = Frame(self.root, bg="#ecf0f1")
        btn_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        # ===== Buttons =====
        Button(btn_frame, text="Student Management",
               command=self.open_student,
               font=("Helvetica", 14),
               bg="#3498db", fg="white",
               width=20, height=2).grid(row=0, column=0, padx=20, pady=20)

        Button(btn_frame, text="Train Model",
               command=self.open_train,
               font=("Helvetica", 14),
               bg="#2ecc71", fg="white",
               width=20, height=2).grid(row=0, column=1, padx=20, pady=20)

        Button(btn_frame, text="Face Recognition",
               command=self.open_face,
               font=("Helvetica", 14),
               bg="#e67e22", fg="white",
               width=20, height=2).grid(row=1, column=0, padx=20, pady=20)

        Button(btn_frame, text="Analytics",
               command=self.open_analytics,
               font=("Helvetica", 14),
               bg="#9b59b6", fg="white",
               width=20, height=2).grid(row=1, column=1, padx=20, pady=20)

        Button(btn_frame, text="Exit",
               command=self.root.quit,
               font=("Helvetica", 14),
               bg="#e74c3c", fg="white",
               width=20, height=2).grid(row=2, column=0, columnspan=2, pady=20)

    # ===== Open Windows =====
    def open_student(self):
        from student import Student
        new_win = Toplevel(self.root)
        Student(new_win)

    def open_train(self):
        from train import Train
        new_win = Toplevel(self.root)
        Train(new_win)

    def open_face(self):
        from face_recognition import FaceRecognition
        new_win = Toplevel(self.root)
        FaceRecognition(new_win)

    def open_analytics(self):
        from analytics import Analytics
        new_win = Toplevel(self.root)
        Analytics(new_win)


# ===== Run =====
if __name__ == "__main__":
    root = Tk()
    app = FaceRecognitionSystem(root)
    root.mainloop()