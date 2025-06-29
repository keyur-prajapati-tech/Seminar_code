from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import os
import cv2
import csv
from tkinter import filedialog
import numpy as np
from tkinter import messagebox
import mysql.connector
from datetime import datetime

mydata = []
class FaceRecognizationAttendance:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1550x800+0+0")
        self.root.title("Face Recognition Attendance System")

        #=================================variables======================
        self.var_att_id = StringVar()
        self.var_att_roll = StringVar()
        self.var_att_name = StringVar()
        self.var_att_dept = StringVar()
        self.var_att_time = StringVar()
        self.var_att_date = StringVar()
        self.var_att_attendance = StringVar()

        #First image
        img = Image.open("D:/Seminar_4thsem/image/face_detection_img.jpg")
        img = img.resize((800,200), Image.ANTIALIAS)
        self.photoimg = ImageTk.PhotoImage(img)

        f_lbl = Label(self.root, image=self.photoimg)
        f_lbl.place(x=0,y=0,width=800,height=200)

        #Second image
        img1 = Image.open("D:/Seminar_4thsem/image/home_page_img.webp")
        img1 = img1.resize((800,200), Image.ANTIALIAS)
        self.photoimg1 = ImageTk.PhotoImage(img1)

        f_lbl = Label(self.root, image=self.photoimg1)
        f_lbl.place(x=800,y=0,width=800,height=200)

        #BG Image
        img2 = Image.open("D:/Seminar_4thsem/image/backgroung_image.jpg")
        img2 = img2.resize((1530, 710), Image.ANTIALIAS)
        self.photoimg2 = ImageTk.PhotoImage(img2)

        bg_img = Label(self.root,image=self.photoimg2)
        bg_img .place(x=0,y=200,width=1540,height=710)

        # Title
        title_lbl = Label(self.root, text="ATTENDANCE MANAGEMENT SYSTEM", font=("times new roman", 30, "bold"),
                         bg="navy", fg="white")
        title_lbl.place(x=0, y=200, width=1537, height=50)

        # Back Button
        back_btn = Button(self.root, text="Back", command=self.root.destroy, font=("times new roman", 13, "bold"),
                         bg="red", fg="white", relief="ridge", borderwidth=2)
        back_btn.place(x=1420, y=6, width=100, height=40)

        #Main Frame
        main_frame = Frame(bg_img,bd=2,bg="white")
        main_frame.place(x=10,y=55,width=1480,height=520)

        #------------------------Left Frame-------------------------
        Left_frame = LabelFrame(main_frame,bd=5,bg="white",relief=RIDGE,text="Student Attendance Details",font=("Arial", 12, "bold"))
        Left_frame.place(x=10,y=10,width=730,height=500)

        img_left = Image.open("D:/Seminar_4thsem/image/student_img2.jpg")
        img_left = img_left.resize((710, 130), Image.ANTIALIAS)
        self.photoimg_left = ImageTk.PhotoImage(img_left)

        f_lbl = Label(Left_frame, image=self.photoimg_left)
        f_lbl.place(x=5,y=0,width=710, height=130)

        left_inside_frame = Frame(Left_frame,bd=2,relief=RIDGE,bg="white")
        left_inside_frame.place(x=10,y=135,width=700,height=330)

        #-----------------------Label and Entry---------------------
        # Row 1
        Label(left_inside_frame, text="Attendance Id:", font=("arial", 12), bg="white").grid(row=0, column=0, padx=10, pady=5, sticky=W)
        ttk.Entry(left_inside_frame, width=20, textvariable=self.var_att_id ,font=("arial", 12)).grid(row=0, column=1, padx=10, pady=5, sticky=W)

        # Row 2
        Label(left_inside_frame, text="Roll No:", font=("arial", 12), bg="white").grid(row=0, column=2, padx=10, pady=5, sticky=W)
        ttk.Entry(left_inside_frame, width=20, textvariable=self.var_att_roll ,font=("arial", 12)).grid(row=0, column=3, padx=10, pady=5, sticky=W)

        # Row 3
        Label(left_inside_frame, text="Name:", font=("arial", 12), bg="white").grid(row=1, column=0, padx=10, pady=5, sticky=W)
        ttk.Entry(left_inside_frame, width=20, textvariable=self.var_att_name ,font=("arial", 12)).grid(row=1, column=1, padx=10, pady=5, sticky=W)

        # Row 4
        Label(left_inside_frame, text="Department:", font=("arial", 12), bg="white").grid(row=1, column=2, padx=10, pady=5, sticky=W)
        ttk.Entry(left_inside_frame, width=20, textvariable=self.var_att_dept ,font=("arial", 12)).grid(row=1, column=3, padx=10, pady=5, sticky=W)

        # Row 5
        Label(left_inside_frame, text="Time:", font=("arial", 12), bg="white").grid(row=2, column=0, padx=10, pady=5, sticky=W)
        ttk.Entry(left_inside_frame, width=20, textvariable=self.var_att_time, font=("arial", 12)).grid(row=2, column=1, padx=10, pady=5, sticky=W)

        # Row 6
        Label(left_inside_frame, text="Date:", font=("arial", 12), bg="white").grid(row=2, column=2, padx=10, pady=5, sticky=W)
        ttk.Entry(left_inside_frame, width=20, textvariable=self.var_att_date, font=("arial", 12)).grid(row=2, column=3, padx=10, pady=5, sticky=W)

        # Row 7
        Label(left_inside_frame, text="Attendance Status:", font=("arial", 12), bg="white").grid(row=3, column=0, padx=10, pady=5, sticky=W)
        course_combo = ttk.Combobox(left_inside_frame, textvariable=self.var_att_attendance, font=("arial", 12), state="readonly", width=17)
        course_combo["values"] = ("Select Status", "Persent", "Absent")
        course_combo.current(0)
        course_combo.grid(row=3, column=1, padx=10, pady=5, sticky=W)

        #button frame
        btn_frame = Frame(left_inside_frame,bd=5,relief=RIDGE,bg="white")
        btn_frame.place(x=3,y=280,width=690,height=35)

        # Buttons
        import_csv_btn = Button(btn_frame, text="Import CSV", command=self.importCSV, width=16, font=("arial", 12, "bold"), bg="blue", fg="white")
        import_csv_btn.grid(row=0, column=0)


        export_csv_btn = Button(btn_frame, text="Export CSV", command=self.exportCSV, width=16, font=("arial", 12, "bold"), bg="blue", fg="white")
        export_csv_btn.grid(row=0, column=1)


        update_btn = Button(btn_frame, text="Update", width=16, font=("arial", 12, "bold"), bg="blue", fg="white")
        update_btn.grid(row=0, column=2)

        reset_btn = Button(btn_frame, text="Reset", command= self.reset_data, width=16, font=("arial", 12, "bold"), bg="blue", fg="white")
        reset_btn.grid(row=0, column=3)

        # ----------------------Right Frame-------------------------
        right_frame = LabelFrame(main_frame, bd=5, relief=RIDGE, text="Attendance Details", font=("Arial", 12, "bold"), bg="white")
        right_frame.place(x=740, y=10, width=720, height=500)

        table_frame = Frame(right_frame,bd=2,relief=RIDGE,bg="white")
        table_frame.place(x=5,y=5,width=700,height=455)

        #=======================Scroll bar table=====================
        scroll_x = ttk.Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(table_frame, orient=VERTICAL)

        self.AttendaceReportTable = ttk.Treeview(table_frame, columns=("Id","Roll No","Name","Department","Time","Date","Attendance Status"),
            xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set
        )

       # Scroll bar table
        scroll_x = ttk.Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(table_frame, orient=VERTICAL)

        self.AttendaceReportTable = ttk.Treeview(table_frame, columns=("id", "roll", "name", "department", "time", "date", "attendance"),
            xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set
        )

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x.config(command=self.AttendaceReportTable.xview)
        scroll_y.config(command=self.AttendaceReportTable.yview)

        self.AttendaceReportTable.heading("id", text="Attendance Id")
        self.AttendaceReportTable.heading("roll", text="Roll No")
        self.AttendaceReportTable.heading("name", text="Student Name")
        self.AttendaceReportTable.heading("department", text="Department")
        self.AttendaceReportTable.heading("time", text="Time")
        self.AttendaceReportTable.heading("date", text="Date")
        self.AttendaceReportTable.heading("attendance", text="Attendance Status")

        self.AttendaceReportTable["show"] = "headings"
        
        self.AttendaceReportTable.column("id", width=100)
        self.AttendaceReportTable.column("roll", width=100)
        self.AttendaceReportTable.column("name", width=150)
        self.AttendaceReportTable.column("department", width=100)
        self.AttendaceReportTable.column("time", width=100)
        self.AttendaceReportTable.column("date", width=100)
        self.AttendaceReportTable.column("attendance", width=120)

        self.AttendaceReportTable.pack(fill=BOTH, expand=1)

        self.AttendaceReportTable.bind("<ButtonRelease>", self.get_cursor)

    def fetchData(self,rows):
        self.AttendaceReportTable.delete(*self.AttendaceReportTable.get_children())
        for i in rows:
            self.AttendaceReportTable.insert("",END,values=i)
    
    #=============================Import CSV============================
    def importCSV(self):
        global mydata
        mydata.clear()
        fln = filedialog.askopenfilename(initialdir=os.getcwd(), title="OPEN CSV", filetypes=(("CSV File","*csv"),("ALL File","*.*")), parent=self.root)
        with open(fln) as myfile:
            csvread = csv.reader(myfile, delimiter=",")

            for i in csvread:
                mydata.append(i)
            self.fetchData(mydata)

    #=============================Export CSV============================
    def exportCSV(self):
        try:
            if len(mydata)<1:
                messagebox.showerror("No Data Found","No Data Found To Export", parent=self.root)
                return False
            fln = filedialog.asksaveasfilename(initialdir=os.getcwd(), title="OPEN CSV", filetypes=(("CSV File","*csv"),("ALL File","*.*")), parent=self.root)
            with open(fln, mode="w",newline="") as myfile:
                export_write = csv.writer(myfile, delimiter=",")

                for i in mydata:
                    export_write.writerow(i)
                messagebox.showinfo("Data Export","Your Data Exported to"+os.path.basename(fln)+"successfully")
        except Exception as es:
            messagebox.showerror("Error",f"Due To : {str(es)}", parent = self.root)

    def get_cursor(self,event=""):
        cursor_row = self.AttendaceReportTable.focus()
        content = self.AttendaceReportTable.item(cursor_row)

        rows = content['values']

        self.var_att_id.set(rows[0])
        self.var_att_roll.set(rows[1])
        self.var_att_name.set(rows[2])
        self.var_att_dept.set(rows[3])
        self.var_att_time.set(rows[4])
        self.var_att_date.set(rows[5])
        self.var_att_attendance.set(rows[6])

    def reset_data(self):
        self.var_att_id.set("")
        self.var_att_roll.set("")
        self.var_att_name.set("")
        self.var_att_dept.set("")
        self.var_att_time.set("")
        self.var_att_date.set("")
        self.var_att_attendance.set("")


if __name__ == "__main__":
    root = Tk()
    obj = FaceRecognizationAttendance(root)
    root.mainloop()