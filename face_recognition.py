import cv2
from tkinter import *
from tkinter import messagebox
import db
import json
import os


class FaceRecognition:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Recognition")
        self.root.geometry("500x300")

        Label(self.root, text="Face Recognition System",
              font=("Arial", 18, "bold")).pack(pady=20)

        Button(self.root, text="Start Recognition",
               command=self.face_recog,
               bg="green", fg="white",
               width=20, height=2).pack(pady=20)

    def load_mapping(self):
        mapping_path = os.path.join(os.getcwd(), "models", "id_mapping.json")

        if not os.path.exists(mapping_path):
            return {}

        with open(mapping_path, "r") as f:
            data = json.load(f)

        # Reverse mapping: numeric → student_id
        return {v: k for k, v in data.items()}

    def face_recog(self):
        try:
            face_cascade = cv2.CascadeClassifier(
                cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
            )

            clf = cv2.face.LBPHFaceRecognizer_create()
            clf.read("models/classifier.xml")

            mapping = self.load_mapping()

            cap = cv2.VideoCapture(0)

            while True:
                ret, img = cap.read()
                if not ret:
                    continue

                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, 1.3, 5)

                for (x, y, w, h) in faces:
                    face = gray[y:y+h, x:x+w]

                    # numeric_id, distance = clf.predict(face)

                    # confidence = int(100 * (1 / (1 + distance)))

                    numeric_id, distance = clf.predict(face)

                    confidence = int(100 * (1 - distance / 300))

                    student_id = mapping.get(numeric_id, "Unknown")

                    if student_id != "Unknown":
                        student = db.get_student(student_id)
                        if student:
                            name = student[1]
                        else:
                            name = "Unknown"
                    else:
                        name = "Unknown"

                    if confidence > 50 and name != "Unknown":
                        db.mark_attendance(student_id, name)
                        label = f"{name} ({student_id}) - {confidence}%"
                        color = (0, 255, 0)
                        status = "Marked"
                    else:
                        label = "Unknown"
                        color = (0, 0, 255)
                        status = "Not Recognized"

                    cv2.rectangle(img, (x, y), (x+w, y+h), color, 2)
                    cv2.putText(img, label, (x, y-10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

                    cv2.putText(img, f"Status: {status}", (x, y+h+25),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)

                cv2.imshow("Face Recognition", img)

                if cv2.waitKey(1) == 13:
                    break

                print("Predicted:", numeric_id, "Confidence:", confidence)

            cap.release()
            cv2.destroyAllWindows()

        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    root = Tk()
    app = FaceRecognition(root)
    root.mainloop()