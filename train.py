import os
import cv2
import numpy as np
from tkinter import *
from tkinter import messagebox


class Train:
    def __init__(self, root):
        self.root = root
        self.root.title("Train Model")
        self.root.geometry("500x300")

        Label(self.root, text="Train Face Recognition Model",
              font=("Arial", 18, "bold")).pack(pady=30)

        Button(self.root, text="Train Data",
               command=self.train_classifier,
               bg="blue", fg="white",
               width=20, height=2).pack(pady=20)

    def train_classifier(self):
        data_dir = "data"

        # Check data folder
        if not os.path.exists(data_dir):
            messagebox.showerror("Error", "Data folder not found")
            return

        paths = [os.path.join(data_dir, f)
                 for f in os.listdir(data_dir)
                 if f.endswith(".jpg")]

        if len(paths) == 0:
            messagebox.showerror("Error", "No images found in data folder")
            return

        faces = []
        ids = []

        # for image_path in paths:
        #     # 🔥 Read image using OpenCV (NO PIL)
        #     img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

        #     if img is None:
        #         continue

        #     # 🔥 Noise reduction
        #     img = cv2.GaussianBlur(img, (5, 5), 0)

        #     # Extract ID from filename
        #     # try:
        #     #     id = int(os.path.split(image_path)[1].split('.')[1])
        #     # except:
        #     #     continue

        #     faces.append(img)
        #     ids.append(id)

        #     cv2.imshow("Training", img)
        #     cv2.waitKey(1)

        id_map = {}

        for image_path in paths:
            img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

            if img is None:
                continue

            img = cv2.GaussianBlur(img, (5, 5), 0)

            file_name = os.path.split(image_path)[1]
            student_id = file_name.split('.')[1]

            if student_id not in id_map:
                id_map[student_id] = len(id_map) + 1

            id = id_map[student_id]

            faces.append(img)
            ids.append(id)

            cv2.imshow("Training", img)
            cv2.waitKey(1)

        if len(faces) == 0:
            messagebox.showerror("Error", "No valid images for training")
            return

        ids = np.array(ids)

        # 🔥 Improved LBPH
        clf = cv2.face.LBPHFaceRecognizer_create(
            radius=2,
            neighbors=8,
            grid_x=8,
            grid_y=8
        )

        clf.train(faces, ids)

        # Save model
        if not os.path.exists("models"):
            os.makedirs("models")

        clf.write("models/classifier.xml")

        import json

        mapping_path = os.path.join(os.getcwd(), "models", "id_mapping.json")

        with open(mapping_path, "w") as f:
            json.dump(id_map, f)

        print("Mapping saved at:", mapping_path)

        cv2.destroyAllWindows()

        messagebox.showinfo("Success", "Model trained successfully!")


if __name__ == "__main__":
    root = Tk()
    app = Train(root)
    root.mainloop()