from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import os
import cv2
import numpy as np
from tkinter import messagebox
import mysql.connector
import time
from datetime import datetime
import csv

class FaceRecognitionSystem:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1550x800+0+0")
        self.root.title("Face Recognition Attendance System")
        
        #self.root.configure(bg="#f0f0f0")

        # Set background image
        self.bg_image = Image.open("D:/Seminar_4thsem/image/backgroung_image.jpg")  # Replace with your image path
        self.bg_image = self.bg_image.resize((1550, 800), Image.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        
        self.bg_label = Label(root, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Initialize variables
        self.video_cap = None
        self.recognizing = False
        self.min_confidence = 70
        self.recognized_ids = set()
        self.attendance_marked = False
        self.csv_file = "attendance_records.csv"
        self.current_student = None  # To store currently recognized student

        # Custom colors
        self.primary_color = "#3498db"
        self.secondary_color = "#2980b9"
        self.accent_color = "#e74c3c"
        self.success_color = "#2ecc71"
        self.text_color = "#ffffff"
        self.card_bg = "#ffffff"
        self.card_fg = "#2c3e50"
        
        # Initialize face recognizer
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        try:
            self.recognizer.read("classifier.xml")
            self.status_message = "Model loaded successfully"
        except:
            self.status_message = "Model not found - Please train first"
            messagebox.showerror("Error", "Classifier model not found. Please train the model first.")

        # Initialize CSV file
        if not os.path.exists(self.csv_file):
            with open(self.csv_file, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["student_id", "rollno", "dept", "course", "date", "status"])

        # UI Components
        self.setup_ui()
        
        # Handle window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def setup_ui(self):
        # Title Frame
        title_frame = Frame(self.root, bg="darkgreen")
        title_frame.place(x=0, y=0, width=1550, height=70)

        # Title Label
        title_lbl = Label(title_frame, text="FACE RECOGNITION ATTENDANCE SYSTEM", 
                         font=("Arial", 25, "bold"), bg="darkgreen", fg="white")
        title_lbl.pack(pady=10)

        # Back Button
        back_btn = Button(title_frame, text="Exit", command=self.on_close,
                         font=("Arial", 12, "bold"), bg="red", fg="white", 
                         relief="ridge", borderwidth=3)
        back_btn.place(x=1400, y=10, width=100, height=40)

        # Main Content Frame
        main_frame = Frame(self.root, bg="white")
        main_frame.place(x=10, y=80, width=1530, height=700)

        # Camera Frame
        self.camera_frame = Frame(main_frame, bg="black", bd=3, relief=RAISED)
        self.camera_frame.place(x=20, y=20, width=900, height=600)
        
        # Results Frame
        self.results_frame = Frame(main_frame, bg="white", bd=3, relief=RAISED)
        self.results_frame.place(x=930, y=20, width=580, height=600)
        
        # Control Frame
        control_frame = Frame(main_frame, bg="white")
        control_frame.place(x=20, y=630, width=1490, height=50)
        
        # Recognition Button
        self.recognition_btn = Button(control_frame, text="START RECOGNITION", 
                                    font=("Arial", 14, "bold"), bg="darkgreen", fg="white",
                                    command=self.toggle_recognition)
        self.recognition_btn.pack(side=LEFT, padx=20)
        
        # Confidence Threshold Slider
        Label(control_frame, text="Confidence:", bg="white").pack(side=LEFT, padx=10)
        self.confidence_slider = Scale(control_frame, from_=50, to=90, 
                                     orient=HORIZONTAL, length=150, bg="white")
        self.confidence_slider.set(self.min_confidence)
        self.confidence_slider.pack(side=LEFT, padx=10)
        
        # Export CSV Button
        export_btn = Button(control_frame, text="Export Attendance", 
                          font=("Arial", 12), bg="blue", fg="white",
                          command=self.export_attendance)
        export_btn.pack(side=LEFT, padx=20)
        
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
                SELECT student_id, name, rollno, dept, course 
                FROM tbl_student 
                WHERE student_id = %s
            """
            cursor.execute(query, (student_id,))
            result = cursor.fetchone()
            
            cursor.close()
            conn.close()
            
            return result if result else None
            
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {str(err)}")
            return None

    def mark_attendance(self, student_info):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="face_recognizer",
                port=3310
            )
            cursor = conn.cursor()
            
            today = datetime.now().strftime("%Y-%m-%d")
            check_query = """
                SELECT * FROM tbl_attendance 
                WHERE student_id = %s AND date = %s
            """
            cursor.execute(check_query, (student_info['student_id'], today))
            if cursor.fetchone():
                return False  # Attendance already marked
            
            insert_query = """
                INSERT INTO tbl_attendance 
                (student_id, rollno, dept, course, date, status)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (
                student_info['student_id'],
                student_info['rollno'],
                student_info['dept'],
                student_info['course'],
                today,
                "Present"
            ))
            conn.commit()
            
            # Write to CSV file
            with open(self.csv_file, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([
                    student_info['student_id'],
                    student_info['rollno'],
                    student_info['dept'],
                    student_info['course'],
                    today,
                    "Present"
                ])
            
            cursor.close()
            conn.close()
            return True
            
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error marking attendance: {str(err)}")
            return False

    def show_confirmation_dialog(self, student_info):
        confirm_window = Toplevel(self.root)
        confirm_window.title("Confirm Attendance")
        confirm_window.geometry("400x300+500+300")
        confirm_window.resizable(False, False)
        confirm_window.grab_set()  # Make it modal
        
        Label(confirm_window, text="Confirm Attendance", 
              font=("Arial", 16, "bold")).pack(pady=10)
        
        # Student info display
        info_frame = Frame(confirm_window)
        info_frame.pack(pady=10)
        
        Label(info_frame, text=f"ID: {student_info['student_id']}", 
              font=("Arial", 12)).pack(anchor=W)
        Label(info_frame, text=f"Name: {student_info['name']}", 
              font=("Arial", 12)).pack(anchor=W)
        Label(info_frame, text=f"Roll No: {student_info['rollno']}", 
              font=("Arial", 12)).pack(anchor=W)
        Label(info_frame, text=f"Department: {student_info['dept']}", 
              font=("Arial", 12)).pack(anchor=W)
        Label(info_frame, text=f"Course: {student_info['course']}", 
              font=("Arial", 12)).pack(anchor=W)
        
        # Buttons
        btn_frame = Frame(confirm_window)
        btn_frame.pack(pady=20)
        
        def confirm():
            success = self.mark_attendance(student_info)
            self.show_attendance_alert(student_info, success)
            confirm_window.destroy()
            self.recognized_ids.add(student_info['student_id'])
        
        Button(btn_frame, text="Confirm", command=confirm,
              font=("Arial", 12), bg="green", fg="white").pack(side=LEFT, padx=10)
        
        Button(btn_frame, text="Cancel", command=confirm_window.destroy,
              font=("Arial", 12), bg="red", fg="white").pack(side=LEFT, padx=10)

    def export_attendance(self):
        try:
            today = datetime.now().strftime("%Y-%m-%d")
            export_filename = f"attendance_export_{today}.csv"
            
            with open(self.csv_file, mode='r') as infile:
                reader = csv.reader(infile)
                with open(export_filename, mode='w', newline='') as outfile:
                    writer = csv.writer(outfile)
                    for row in reader:
                        writer.writerow(row)
            
            messagebox.showinfo("Export Successful", 
                              f"Attendance data exported to {export_filename}")
        except Exception as e:
            messagebox.showerror("Export Error", f"Error exporting attendance: {str(e)}")

    def show_attendance_alert(self, student_info, success=True):
        alert_window = Toplevel(self.root)
        alert_window.title("Attendance Alert")
        alert_window.geometry("400x200+500+300")
        alert_window.resizable(False, False)
        
        if success:
            Label(alert_window, text="ATTENDANCE MARKED", font=("Arial", 16, "bold"), fg="green").pack(pady=10)
            Label(alert_window, text=f"ID: {student_info['student_id']}", font=("Arial", 12)).pack()
            Label(alert_window, text=f"Name: {student_info['name']}", font=("Arial", 12)).pack()
        else:
            Label(alert_window, text="ATTENDANCE ALREADY MARKED", font=("Arial", 16, "bold"), fg="red").pack(pady=10)
            Label(alert_window, text=f"ID: {student_info['student_id']}", font=("Arial", 12)).pack()
        
        alert_window.after(3000, alert_window.destroy)

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
        self.recognized_ids.clear()
        
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
            
            # Clear previous results
            for widget in self.results_frame.winfo_children():
                widget.destroy()
            
            if len(faces) == 0:
                Label(self.results_frame, text="No faces detected", 
                     font=("Arial", 16), bg="white").pack(pady=250)
            
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
                id, confidence = self.recognizer.predict(gray[y:y+h, x:x+w])
                confidence_percent = int(100 * (1 - confidence / 300))
                
                if confidence_percent > self.min_confidence:
                    student = self.get_student_info(id)
                    if student:
                        # Display in results frame
                        result_frame = Frame(self.results_frame, bd=2, relief=GROOVE, bg="#f0f0f0")
                        result_frame.pack(fill=X, padx=10, pady=5)
                        
                        Label(result_frame, text=f"Recognized Student", 
                             font=("Arial", 14, "bold"), bg="#f0f0f0").pack(anchor=W)
                        Label(result_frame, text=f"ID: {student['student_id']}", 
                             font=("Arial", 12), bg="#f0f0f0").pack(anchor=W)
                        Label(result_frame, text=f"Name: {student['name']}", 
                             font=("Arial", 12), bg="#f0f0f0").pack(anchor=W)
                        Label(result_frame, text=f"Roll No: {student['rollno']}", 
                             font=("Arial", 12), bg="#f0f0f0").pack(anchor=W)
                        Label(result_frame, text=f"Department: {student['dept']}", 
                             font=("Arial", 12), bg="#f0f0f0").pack(anchor=W)
                        Label(result_frame, text=f"Course: {student['course']}", 
                             font=("Arial", 12), bg="#f0f0f0").pack(anchor=W)
                        Label(result_frame, text=f"Confidence: {confidence_percent}%", 
                             font=("Arial", 12), bg="#f0f0f0").pack(anchor=W)
                        
                        # Show confirmation dialog if not already recognized
                        if id not in self.recognized_ids:
                            self.current_student = student
                            self.show_confirmation_dialog(student)
                            self.recognized_ids.add(id)  # Prevent multiple dialogs for same student
                    else:
                        cv2.putText(img, "Unknown Student", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2)
                else:
                    cv2.putText(img, "Unknown Face", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2)
            
            # Display camera feed
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)
            img = ImageTk.PhotoImage(image=img)
            
            if not hasattr(self, 'camera_label'):
                self.camera_label = Label(self.camera_frame)
                self.camera_label.pack(fill=BOTH, expand=True)
            
            self.camera_label.imgtk = img
            self.camera_label.configure(image=img)
            
            # Continue recognition
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
    obj = FaceRecognitionSystem(root)
    root.mainloop()