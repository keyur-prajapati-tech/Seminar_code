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

        # Load images
        img1 = Image.open("D:/Seminar_4thsem/image/face6.jpg")
        img1 = img1.resize((500, 270), Image.LANCZOS)
        self.photo1 = ImageTk.PhotoImage(img1)

        img2 = Image.open("D:/Seminar_4thsem/image/face2.png")
        img2 = img2.resize((500, 270), Image.LANCZOS)
        self.photo2 = ImageTk.PhotoImage(img2)

        img3 = Image.open("D:/Seminar_4thsem/image/face5.jpg")
        img3 = img3.resize((500, 270), Image.LANCZOS)
        self.photo3 = ImageTk.PhotoImage(img3)

        Label(self.root, image=self.photo1).place(x=7, y=50, width=500, height=270)
        Label(self.root, image=self.photo2).place(x=520, y=50, width=500, height=270)
        Label(self.root, image=self.photo3).place(x=1030, y=50, width=500, height=270)

        # TRAIN DATA Button
        train_btn = Button(self.root, text="TRAIN DATA", command=self.train_classifier, bd=5,
                          font=("times new roman", 20, "bold"), bg="navy", fg="white", cursor="hand2")
        train_btn.place(x=0, y=310, width=1550, height=40)

        # Background image
        img4 = Image.open("D:/Seminar_4thsem/image/collage1.jpg")
        img4 = img4.resize((1550, 450), Image.LANCZOS)
        self.photo4 = ImageTk.PhotoImage(img4)
        Label(self.root, image=self.photo4).place(x=0, y=350, width=1550, height=450)

    def train_classifier(self):
        data_dir = "data"
        
        # Verify data directory exists
        if not os.path.exists(data_dir):
            messagebox.showerror("Error", "Data directory not found!", parent=self.root)
            return
        
        # Get all image files
        image_files = [os.path.join(data_dir, f) for f in os.listdir(data_dir) 
                      if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        
        if not image_files:
            messagebox.showerror("Error", "No images found in data directory!", parent=self.root)
            return

        faces = []
        ids = []
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        # Progress variables
        total_images = len(image_files)
        processed_images = 0
        unique_student_ids = set()

        for image_path in image_files:
            try:
                # Read image
                img = cv2.imread(image_path)
                if img is None:
                    print(f"Could not read image: {image_path}")
                    continue
                
                # Convert to grayscale
                gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                
                # Detect faces with adjusted parameters
                faces_rect = face_cascade.detectMultiScale(
                    gray_img, 
                    scaleFactor=1.1, 
                    minNeighbors=5,
                    minSize=(100, 100))
                
                # Extract ID from filename (format: user.{student_id}.{number}.jpg)
                filename = os.path.basename(image_path)
                try:
                    student_id = int(filename.split('.')[1])
                    unique_student_ids.add(student_id)
                except (IndexError, ValueError):
                    print(f"Invalid filename format: {filename}")
                    continue
                
                for (x, y, w, h) in faces_rect:
                    face_roi = gray_img[y:y+h, x:x+w]
                    
                    # Resize face to consistent size (recommended for LBPH)
                    face_roi = cv2.resize(face_roi, (200, 200))
                    
                    faces.append(face_roi)
                    ids.append(student_id)
                    
                    # Display progress
                    processed_images += 1
                    print(f"Processing {processed_images}/{total_images} - Student ID: {student_id}")
                    
                    # Show detected face (optional)
                    cv2.imshow("Training Faces", face_roi)
                    if cv2.waitKey(1) == 13:  # Press Enter to stop
                        break
                        
            except Exception as e:
                print(f"Error processing {image_path}: {str(e)}")
                continue

        cv2.destroyAllWindows()
        
        if len(faces) == 0:
            messagebox.showerror("Error", 
                               "No faces detected in images!\n\nPossible solutions:\n"
                               "1. Ensure faces are clearly visible and frontal\n"
                               "2. Check lighting conditions in images\n"
                               "3. Make sure images are not too small or blurry", 
                               parent=self.root)
            return
        
        # Train the recognizer
        try:
            recognizer = cv2.face.LBPHFaceRecognizer_create()
            recognizer.train(faces, np.array(ids))
            
            # Save the trained model
            recognizer.save("classifier.xml")
            recognizer.write("classifier.yml")
            
            messagebox.showinfo("Success", 
                              f"Training completed successfully!\n\n"
                              f"Statistics:\n"
                              f"- Total face samples: {len(faces)}\n"
                              f"- Unique students: {len(unique_student_ids)}\n"
                              f"- Model saved to classifier.xml", 
                              parent=self.root)
        except Exception as e:
            messagebox.showerror("Error", f"Training failed: {str(e)}", parent=self.root)


if __name__ == "__main__":
    root = Tk()
    obj = TrainData(root)
    root.mainloop()