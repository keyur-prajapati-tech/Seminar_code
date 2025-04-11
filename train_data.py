from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import os
import cv2
import numpy as np
from tkinter import messagebox

class TrainData:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1550x800+0+0")
        self.root.title("Face Recognition Attendance System")

        # Title
        title_lbl = Label(self.root, text="TRAIN DATA SET", font=("times new roman", 30, "bold"),
                          bg="white", fg="red")
        title_lbl.place(x=0, y=0, width=1550, height=50)

        # Back Button
        back_btn = Button(self.root, text="Back", command=self.root.destroy, font=("times new roman", 13, "bold"),
                          bg="white", fg="red", relief="ridge", borderwidth=2)
        back_btn.place(x=1420, y=6, width=100, height=40)

        # Load 3 face detection images
        img1 = Image.open("image/face6.jpg")  # Replace with your own image paths
        img1 = img1.resize((500, 270), Image.ANTIALIAS)
        self.photo1 = ImageTk.PhotoImage(img1)

        img2 = Image.open("image/face2.png")
        img2 = img2.resize((500, 270), Image.ANTIALIAS)
        self.photo2 = ImageTk.PhotoImage(img2)

        img3 = Image.open("image/face5.jpg")
        img3 = img3.resize((500, 270), Image.ANTIALIAS)
        self.photo3 = ImageTk.PhotoImage(img3)

        Label(self.root, image=self.photo1).place(x=7, y=50, width=500, height=270)
        Label(self.root, image=self.photo2).place(x=520, y=50, width=500, height=270)
        Label(self.root, image=self.photo3).place(x=1030, y=50, width=500, height=270)

        # TRAIN DATA Label
        train_btn = Button(self.root, text="TRAIN DATA", command=self.train_classifier, bd=5, font=("times new roman", 20, "bold"), bg="navy", fg="white", cursor="hand2")
        train_btn.place(x=0, y=310, width=1550, height=40)


        # Big face collage
        img4 = Image.open("image/collage1.jpg")  # Replace with your collage image
        img4 = img4.resize((1550, 450), Image.ANTIALIAS)
        self.photo4 = ImageTk.PhotoImage(img4)

        Label(self.root, image=self.photo4).place(x=0, y=350, width=1550, height=450)
    
    def train_classifier(self):
        data_dir = "data"
        path = [os.path.join(data_dir, file) for file in os.listdir(data_dir)]

        faces = []
        ids = []

        for image in path:
            if image.endswith(".jpg") and "user." in image:
                try:
                    # Example filename: user.1.1.jpg
                    id = int(os.path.split(image)[1].split('.')[1])
                    img = Image.open(image).convert('L')  # Grayscale
                    image_np = np.array(img, 'uint8')
                    faces.append(image_np)
                    ids.append(id)
                except Exception as e:
                    print(f"Skipping file {image}: {e}")
                    continue

        if len(faces) == 0:
            messagebox.showerror("Error", "No valid training images found!", parent=self.root)
            return

        ids = np.array(ids)

        # Train the recognizer and save the classifier
        clf = cv2.face.LBPHFaceRecognizer_create()
        clf.train(faces, ids)
        clf.write("classifier.xml")

        messagebox.showinfo("Result", "Training dataset completed!", parent=self.root)

    # def train_classifier(self):
    
    #     data_dir = "data"
    #     path = [os.path.join(data_dir, file) for file in os.listdir(data_dir)]

    #     faces = []
    #     ids = []

    #     for image in path:
    #         img = Image.open(image).convert('L')  # Convert to grayscale
    #         image_np = np.array(img, 'uint8')
    #         id = int(os.path.split(image)[1].split('.')[1])  # Extract user ID
    #         faces.append(image_np)
    #         ids.append(id)
    #         cv2.imshow("Traning",image_np)
    #         cv2.waitKey(1) == 13
    #     ids = np.array(ids)

    #     # Train the classifier and save
    #     clf = cv2.face.LBPHFaceRecognizer_create()
    #     clf.train(faces, ids)
    #     clf.write("classifier.xml")
    #     cv2.destroyAllWindows()

    #     messagebox.showinfo("Result", "Training dataset completed!", parent=self.root)

if __name__ == "__main__":
    root = Tk()
    obj = TrainData(root)
    root.mainloop()