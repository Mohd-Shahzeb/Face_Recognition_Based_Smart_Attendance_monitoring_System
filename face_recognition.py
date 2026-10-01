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

        Label(
            self.root,
            text="Face Recognition System",
            font=("Arial", 18, "bold")
        ).pack(pady=20)

        Button(
            self.root,
            text="Start Recognition",
            command=self.face_recog,
            bg="green",
            fg="white",
            width=20,
            height=2
        ).pack(pady=20)

    def load_mapping(self):
        # Get the project folder
        base_dir = os.path.dirname(os.path.abspath(__file__))

        mapping_path = os.path.join(
            base_dir,
            "models",
            "id_mapping.json"
        )

        if not os.path.exists(mapping_path):
            return {}

        with open(mapping_path, "r") as f:
            data = json.load(f)

        # Reverse mapping: numeric ID -> student ID
        return {v: k for k, v in data.items()}

    def face_recog(self):
        cap = None

        try:
            # ==========================================
            # 1. Load Haar Cascade
            # ==========================================

            base_dir = os.path.dirname(
                os.path.abspath(__file__)
            )

            cascade_path = os.path.join(
                base_dir,
                "haarcascade_frontalface_default.xml"
            )

            print("Cascade path:", cascade_path)
            print(
                "Cascade exists:",
                os.path.exists(cascade_path)
            )

            face_cascade = cv2.CascadeClassifier(
                cascade_path
            )

            if face_cascade.empty():
                raise Exception(
                    "Haar Cascade could not be loaded.\n\n"
                    "Make sure this file exists in your "
                    "project folder:\n\n"
                    "haarcascade_frontalface_default.xml"
                )

            # ==========================================
            # 2. Load trained LBPH model
            # ==========================================

            classifier_path = os.path.join(
                base_dir,
                "models",
                "classifier.xml"
            )

            if not os.path.exists(classifier_path):
                raise Exception(
                    "Trained classifier not found:\n\n"
                    + classifier_path
                )

            clf = cv2.face.LBPHFaceRecognizer_create()

            clf.read(classifier_path)

            # ==========================================
            # 3. Load ID mapping
            # ==========================================

            mapping = self.load_mapping()

            # ==========================================
            # 4. Open camera
            # ==========================================

            cap = cv2.VideoCapture(0)

            if not cap.isOpened():
                raise Exception(
                    "Could not open the camera.\n\n"
                    "Please check your webcam."
                )

            # ==========================================
            # 5. Start recognition
            # ==========================================

            while True:

                ret, img = cap.read()

                if not ret:
                    print("Could not read camera frame.")
                    continue

                gray = cv2.cvtColor(
                    img,
                    cv2.COLOR_BGR2GRAY
                )

                # Detect faces
                faces = face_cascade.detectMultiScale(
                    gray,
                    scaleFactor=1.3,
                    minNeighbors=5
                )

                # ==========================================
                # 6. Recognize each detected face
                # ==========================================

                for (x, y, w, h) in faces:

                    face = gray[
                        y:y + h,
                        x:x + w
                    ]

                    numeric_id, distance = clf.predict(
                        face
                    )

                    confidence = int(
                        100 * (1 - distance / 300)
                    )

                    # Get student ID from mapping
                    student_id = mapping.get(
                        numeric_id,
                        "Unknown"
                    )

                    # ======================================
                    # Get student information from database
                    # ======================================

                    if student_id != "Unknown":

                        student = db.get_student(
                            student_id
                        )

                        if student:
                            name = student[1]
                        else:
                            name = "Unknown"

                    else:
                        name = "Unknown"

                    # ======================================
                    # Mark attendance
                    # ======================================

                    if (
                        confidence > 50
                        and name != "Unknown"
                    ):

                        db.mark_attendance(
                            student_id,
                            name
                        )

                        label = (
                            f"{name} ({student_id}) "
                            f"- {confidence}%"
                        )

                        color = (0, 255, 0)

                        status = "Marked"

                    else:

                        label = "Unknown"

                        color = (0, 0, 255)

                        status = "Not Recognized"

                    # ======================================
                    # Draw face rectangle
                    # ======================================

                    cv2.rectangle(
                        img,
                        (x, y),
                        (x + w, y + h),
                        color,
                        2
                    )

                    # Student name / ID
                    cv2.putText(
                        img,
                        label,
                        (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        color,
                        2
                    )

                    # Attendance status
                    cv2.putText(
                        img,
                        f"Status: {status}",
                        (x, y + h + 25),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        (255, 255, 255),
                        2
                    )

                    print(
                        "Predicted:",
                        numeric_id,
                        "Confidence:",
                        confidence
                    )

                # ==========================================
                # 7. Display camera
                # ==========================================

                cv2.imshow(
                    "Face Recognition",
                    img
                )

                # Press ENTER to exit
                if cv2.waitKey(1) == 13:
                    break

        except Exception as e:

            messagebox.showerror(
                "Face Recognition Error",
                str(e)
            )

        finally:

            if cap is not None:
                cap.release()

            cv2.destroyAllWindows()


if __name__ == "__main__":

    root = Tk()

    app = FaceRecognition(root)

    root.mainloop()
