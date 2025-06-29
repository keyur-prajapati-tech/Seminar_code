from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import os
import cv2
import numpy as np
from tkinter import messagebox
import mysql.connector
from datetime import datetime
import csv

class FaceRecognitionAttandanceSystem:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1550x800+0+0")
        self.root.title("Face Recognition Attendance System")
        
        # Set background image
        try:
            self.bg_image = Image.open("D:/Seminar_4thsem/image/backgroung_image.jpg")
            self.bg_image = self.bg_image.resize((1550, 800), Image.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(self.bg_image)
            self.bg_label = Label(root, image=self.bg_photo)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            print(f"Error loading background image: {e}")
            self.root.configure(bg="#f0f0f0")

        # Initialize variables
        self.video_cap = None
        self.recognizing = False
        self.min_confidence = 70
        self.recognized_ids = set()
        self.csv_file = "attendance_records.csv"
        self.current_student = None

        # Initialize face recognizer
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        try:
            self.recognizer.read("classifier.xml")
            self.status_message = "Model loaded successfully"
        except:
            self.status_message = "Model not found - Please train first"
            messagebox.showerror("Error", "Classifier model not found. Please train the model first.")

        # Initialize CSV file with headers
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
        
        # Results Frame with Scrollbar
        results_container = Frame(main_frame, bg="white", bd=3, relief=RAISED)
        results_container.place(x=930, y=20, width=580, height=600)
        
        # Create a canvas and scrollbar
        self.results_canvas = Canvas(results_container, bg="white", highlightthickness=0)
        scrollbar = Scrollbar(results_container, orient="vertical", command=self.results_canvas.yview)
        self.scrollable_frame = Frame(self.results_canvas, bg="white")
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.results_canvas.configure(
                scrollregion=self.results_canvas.bbox("all")
            )
        )
        
        self.results_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.results_canvas.configure(yscrollcommand=scrollbar.set)
        
        self.results_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
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
                SELECT student_id, name, email, dept, course, rollno, division, semester 
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

    def get_attendance_records(self):
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
                SELECT a.date, s.dept, s.course, s.student_id, s.rollno, s.name, a.status
                FROM tbl_attendance a
                JOIN tbl_student s ON a.student_id = s.student_id
                ORDER BY a.date DESC, s.dept, s.course, s.rollno
            """
            cursor.execute(query)
            results = cursor.fetchall()
            
            cursor.close()
            conn.close()
            
            return results
            
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
                (student_id,name, rollno, dept, course, date, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (
                student_info['student_id'],
                student_info['name'],
                student_info['rollno'],
                student_info['dept'],
                student_info['course'],
                today,
                "Present"
            ))
            conn.commit()
            
            # Write to CSV file in the new format
            self.update_csv_file()
            
            cursor.close()
            conn.close()
            return True
            
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error marking attendance: {str(err)}")
            return False

    def update_csv_file(self):
        """Update the CSV file with the new grouped format"""
        attendance_data = self.get_attendance_records()
        if not attendance_data:
            return
            
        # Group data by date, department, and course
        grouped_data = {}
        for record in attendance_data:
            key = (record['date'], record['dept'], record['course'])
            if key not in grouped_data:
                grouped_data[key] = []
            grouped_data[key].append(record)
        
        # Write to CSV file
        with open(self.csv_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            # Write headers
            writer.writerow(["student_id", "rollno", "name", "dept", "course", "date", "status"])
            
            # Write grouped data
            for (date, dept, course), records in grouped_data.items():
                # Write header row for this group
                writer.writerow([f"DATE : {date}", f"Department : {dept}", f"Course : {course}"])
                # Write student records
                for record in records:
                    writer.writerow([
                        record['student_id'],
                        record['name'],
                        record['rollno'],
                        record['dept'],
                        record['course'],
                        record['date'],
                        record['status']
                    ])
                # Add empty row between groups
                writer.writerow([])

    def show_student_info(self, student_info, confidence):
        # Clear previous results
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        # Student Info Frame
        student_frame = Frame(self.scrollable_frame, bd=2, relief=GROOVE, bg="#f0f0f0", padx=10, pady=10)
        student_frame.pack(fill=X, padx=10, pady=10)
        
        # Student Information
        Label(student_frame, text="RECOGNIZED STUDENT", 
             font=("Arial", 14, "bold"), bg="#f0f0f0").pack(anchor=W, pady=(0, 10))
        
        info_labels = [
            f"ID: {student_info['student_id']}",
            f"Name: {student_info['name']}",
            f"Roll No: {student_info['rollno']}",
            f"Department: {student_info['dept']}",
            f"Course: {student_info['course']}",
            f"Confidence: {confidence}%"
        ]
        
        for label_text in info_labels:
            Label(student_frame, text=label_text, 
                 font=("Arial", 12), bg="#f0f0f0").pack(anchor=W)
        
        # Today's Attendance Frame
        today_frame = Frame(self.scrollable_frame, bd=2, relief=GROOVE, bg="#f0f0f0", padx=10, pady=10)
        today_frame.pack(fill=X, padx=10, pady=10)
        
        today = datetime.now().strftime("%Y-%m-%d")
        Label(today_frame, text=f"TODAY'S ATTENDANCE - {today}", 
             font=("Arial", 14, "bold"), bg="#f0f0f0").pack(anchor=W, pady=(0, 10))
        
        # Get today's attendance for this student's department and course
        attendance_data = self.get_todays_attendance(student_info['dept'], student_info['course'])
        
        if attendance_data:
            # Create a table-like display
            header_frame = Frame(today_frame, bg="#f0f0f0")
            header_frame.pack(fill=X, pady=(0, 5))
            
            Label(header_frame, text="Roll No", width=10, font=("Arial", 10, "bold"), 
                 bg="#f0f0f0").pack(side=LEFT)
            Label(header_frame, text="Name", width=25, font=("Arial", 10, "bold"), 
                 bg="#f0f0f0").pack(side=LEFT)
            Label(header_frame, text="Status", width=10, font=("Arial", 10, "bold"), 
                 bg="#f0f0f0").pack(side=LEFT)
            
            for student in attendance_data:
                student_frame = Frame(today_frame, bg="#f0f0f0")
                student_frame.pack(fill=X)
                
                Label(student_frame, text=student['rollno'], width=10, 
                     font=("Arial", 10), bg="#f0f0f0").pack(side=LEFT)
                Label(student_frame, text=student['name'], width=25, 
                     font=("Arial", 10), bg="#f0f0f0").pack(side=LEFT)
                
                status = student['status'] if student['status'] else "Absent"
                status_color = "green" if status == "Present" else "red"
                Label(student_frame, text=status, width=10, fg=status_color,
                     font=("Arial", 10), bg="#f0f0f0").pack(side=LEFT)
        else:
            Label(today_frame, text="No attendance data found", 
                 font=("Arial", 12), bg="#f0f0f0").pack(anchor=W)
        
        # Confirmation Buttons
        btn_frame = Frame(self.scrollable_frame, bg="white")
        btn_frame.pack(fill=X, padx=10, pady=10)
        
        def confirm():
            success = self.mark_attendance(student_info)
            self.show_attendance_alert(student_info, success)
            if success:
                self.recognized_ids.add(student_info['student_id'])
                # Refresh attendance display after marking
                self.show_student_info(student_info, confidence)
        
        confirm_btn = Button(btn_frame, text="Confirm Attendance", command=confirm,
                           font=("Arial", 12, "bold"), bg="green", fg="white")
        confirm_btn.pack(side=LEFT, padx=5, ipadx=10)
        
        cancel_btn = Button(btn_frame, text="Cancel", command=lambda: [w.destroy() for w in self.scrollable_frame.winfo_children()],
                          font=("Arial", 12), bg="red", fg="white")
        cancel_btn.pack(side=LEFT, padx=5, ipadx=10)
        
        # Update the scroll region
        self.scrollable_frame.update_idletasks()
        self.results_canvas.configure(scrollregion=self.results_canvas.bbox("all"))

    def get_todays_attendance(self, dept, course):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="face_recognizer",
                port=3310
            )
            cursor = conn.cursor(dictionary=True)
            
            today = datetime.now().strftime("%Y-%m-%d")
            query = """
                SELECT s.student_id, s.name, s.rollno, a.status 
                FROM tbl_student s
                LEFT JOIN tbl_attendance a ON s.student_id = a.student_id AND a.date = %s
                WHERE s.dept = %s AND s.course = %s
                ORDER BY s.rollno
            """
            cursor.execute(query, (today, dept, course))
            results = cursor.fetchall()
            
            cursor.close()
            conn.close()
            
            return results
            
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {str(err)}")
            return None

    def export_attendance(self):
        try:
            # Get all attendance records grouped by date, department, and course
            attendance_data = self.get_attendance_records()
            if not attendance_data:
                messagebox.showinfo("Info", "No attendance records found to export")
                return
            
            # Create export filename with current date
            export_filename = f"attendance_export_{datetime.now().strftime('%Y-%m-%d')}.csv"
            
            # Group data by date, department, and course
            grouped_data = {}
            for record in attendance_data:
                key = (record['date'], record['dept'], record['course'])
                if key not in grouped_data:
                    grouped_data[key] = []
                grouped_data[key].append(record)
            
            # Write to CSV file
            with open(export_filename, mode='w', newline='') as file:
                writer = csv.writer(file)
                # Write headers
                writer.writerow(["student_id", "rollno", "dept", "course", "date", "status"])
                
                # Write grouped data
                for (date, dept, course), records in grouped_data.items():
                    # Write header row for this group
                    writer.writerow([f"DATE : {date}", f"Department : {dept}", f"Course : {course}"])
                    # Write student records
                    for record in records:
                        writer.writerow([
                            record['student_id'],
                            record['rollno'],
                            record['dept'],
                            record['course'],
                            record['date'],
                            record['status']
                        ])
                    # Add empty row between groups
                    writer.writerow([])
            
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
            
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
                id, confidence = self.recognizer.predict(gray[y:y+h, x:x+w])
                confidence_percent = int(100 * (1 - confidence / 300))
                
                if confidence_percent > self.min_confidence:
                    student = self.get_student_info(id)
                    if student and id not in self.recognized_ids:
                        self.current_student = student
                        self.show_student_info(student, confidence_percent)
                        self.recognized_ids.add(id)
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
    obj = FaceRecognitionAttandanceSystem(root)
    root.mainloop()