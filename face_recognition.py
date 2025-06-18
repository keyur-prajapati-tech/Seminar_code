from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import os
import cv2
import numpy as np
from tkinter import messagebox
import mysql.connector

class FaceRecognition:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1550x800+0+0")
        self.root.title("Face Recognition System")
        self.root.configure(bg="#f0f0f0")
        
        # Initialize variables
        self.video_cap = None
        self.recognizing = False
        self.min_confidence = 70  # Minimum confidence threshold
        
        # Initialize face recognizer
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        try:
            self.recognizer.read("classifier.xml")
            self.status_message = "Model loaded successfully"
        except:
            self.status_message = "Model not found - Please train first"
            messagebox.showerror("Error", "Classifier model not found. Please train the model first.")

        # UI Components
        self.setup_ui()
        
        # Handle window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def setup_ui(self):
        # Title Frame
        title_frame = Frame(self.root, bg="darkgreen")
        title_frame.place(x=0, y=0, width=1550, height=70)

        # Title Label
        title_lbl = Label(title_frame, text="FACE RECOGNITION SYSTEM", 
                         font=("Arial", 30, "bold"), bg="darkgreen", fg="white")
        title_lbl.pack(pady=10)

        # Back Button
        back_btn = Button(title_frame, text="Exit", command=self.on_close,
                         font=("Arial", 12, "bold"), bg="red", fg="white", 
                         relief="ridge", borderwidth=3)
        back_btn.place(x=1400, y=10, width=100, height=40)

        # Main Content Frame
        main_frame = Frame(self.root, bg="white")
        main_frame.place(x=10, y=80, width=1530, height=700)

        # Left Image
        img1 = Image.open("D:/Seminar_4thsem/image/Face-Recognition-img2.jpg")
        img1 = img1.resize((600, 650), Image.LANCZOS)
        self.photo1 = ImageTk.PhotoImage(img1)
        
        img1_label = Label(main_frame, image=self.photo1, bd=3, relief=RAISED)
        img1_label.place(x=20, y=20, width=600, height=650)

        # Right Image
        img2 = Image.open("D:/Seminar_4thsem/image/facial_recognition_system_identification.webp")
        img2 = img2.resize((900, 650), Image.LANCZOS)
        self.photo2 = ImageTk.PhotoImage(img2)
        
        img2_label = Label(main_frame, image=self.photo2, bd=3, relief=RAISED)
        img2_label.place(x=630, y=20, width=880, height=650)

        # Face Recognition Button
        self.recognition_btn = Button(main_frame, text="START RECOGNITION", bd=5,
                         font=("Arial", 12, "bold"), bg="darkgreen", fg="white", 
                         cursor="hand2", command=self.toggle_recognition)
        self.recognition_btn.place(x=950, y=595, width=250, height=40)

        # Confidence Threshold Slider
        self.confidence_frame = Frame(main_frame, bg="white")
        self.confidence_frame.place(x=650, y=595, width=250, height=40)
        
        Label(self.confidence_frame, text="Confidence:", bg="white").pack(side=LEFT)
        self.confidence_slider = Scale(self.confidence_frame, from_=50, to=90, 
                                     orient=HORIZONTAL, bg="white")
        self.confidence_slider.set(self.min_confidence)
        self.confidence_slider.pack(side=LEFT, fill=X, expand=True)

        # Status Bar
        self.status_var = StringVar()
        self.status_var.set(self.status_message)
        status_bar = Label(self.root, textvariable=self.status_var, bd=1, 
                         relief=SUNKEN, anchor=W, font=("Arial", 10), 
                         bg="darkgreen", fg="white")
        status_bar.place(x=0, y=780, width=1550, height=20)

    def get_student_info(self, student_id):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="face_recognizer",
                port=3310
            )
            cursor = conn.cursor(dictionary=True)
            
            query = """
                SELECT student_id, name, email, dept, course, rollno, division, semester 
                FROM tbl_student 
                WHERE student_id = %s
            """
            cursor.execute(query, (student_id,))
            result = cursor.fetchone()
            
            cursor.close()
            conn.close()
            
            if result:
                return {
                    'name': result['name'],
                    'email': result['email'],
                    'rollno': result['rollno'],
                    'division': result['division'],
                    'dept': result['dept'],
                    'course': result['course'],
                    'semester': result['semester']
                }
            return None
            
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
            return None

    def toggle_recognition(self):
        if not self.recognizing:
            self.start_recognition()
        else:
            self.stop_recognition()

    def start_recognition(self):
        if self.recognizing:
            return
            
        self.recognizing = True
        self.min_confidence = self.confidence_slider.get()
        self.recognition_btn.config(text="STOP RECOGNITION", bg="red")
        self.status_var.set("Recognition in progress...")
        
        # Initialize camera
        self.video_cap = cv2.VideoCapture(0)
        if not self.video_cap.isOpened():
            messagebox.showerror("Error", "Could not open video device")
            self.stop_recognition()
            return
        
        self.recognize_faces()

    def recognize_faces(self):
        if not self.recognizing:
            return
            
        ret, img = self.video_cap.read()
        if ret:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
                id, confidence = self.recognizer.predict(gray[y:y+h, x:x+w])
                confidence_percent = int(100 * (1 - confidence / 300))
                
                # Update confidence threshold from slider
                self.min_confidence = self.confidence_slider.get()
                
                if confidence_percent > self.min_confidence:  # Use dynamic confidence threshold
                    student = self.get_student_info(id)
                    if student:
                        # Display student info
                        cv2.putText(img, f"ID: {id}", (x, y-100), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                        cv2.putText(img, f"Name: {student['name']}", (x, y-80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                        cv2.putText(img, f"Roll: {student['rollno']}", (x, y-60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                        cv2.putText(img, f"Dept: {student['dept']}", (x, y-40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                        cv2.putText(img, f"Confidence: {confidence_percent}%", (x, y-20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                    else:
                        cv2.putText(img, "Unknown Student", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2)
                else:
                    cv2.putText(img, "Unknown Face", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2)
            
            cv2.imshow("Face Recognition", img)
            
            # Check if window was closed
            if cv2.getWindowProperty("Face Recognition", cv2.WND_PROP_VISIBLE) < 1:
                self.stop_recognition()
                return
            
            # Continue recognition after 10ms
            self.root.after(10, self.recognize_faces)
        else:
            self.stop_recognition()

    def stop_recognition(self):
        if self.recognizing:
            self.recognizing = False
            self.recognition_btn.config(text="START RECOGNITION", bg="darkgreen")
            self.status_var.set("Recognition stopped")
            
            if self.video_cap and self.video_cap.isOpened():
                self.video_cap.release()
            cv2.destroyAllWindows()

    def on_close(self):
        self.stop_recognition()
        self.root.destroy()

if __name__ == "__main__":
    root = Tk()
    obj = FaceRecognition(root)
    root.mainloop()