from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import mysql.connector
import cv2 
import time  # for unique timestamp

class Student:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1550x800+0+0")
        self.root.title("Face Recognition Attendance System")

        #-----------------------Variables----------------------------
        self.var_dept = StringVar()
        self.var_course = StringVar()
        self.var_year = StringVar()
        self.var_semester = StringVar()
        self.var_stud_id = StringVar()
        self.var_stud_name = StringVar()
        self.var_div = StringVar()
        self.var_roll = StringVar()
        self.var_gender = StringVar()
        self.var_dob = StringVar()
        self.var_email = StringVar()
        self.var_phone = StringVar()
        self.var_address = StringVar()
        self.var_teacher = StringVar()

        # ----------------------Header Images-------------------------
        img = Image.open("D:/Seminar_4thsem/image/student_img1.webp").resize((550, 130), Image.ANTIALIAS)
        self.photoimag = ImageTk.PhotoImage(img)
        Label(self.root, image=self.photoimag).place(x=0, y=0, width=530, height=180)

        img1 = Image.open("D:/Seminar_4thsem/image/student_img2.jpg").resize((550, 130), Image.ANTIALIAS)
        self.photoimag2 = ImageTk.PhotoImage(img1)
        Label(self.root, image=self.photoimag2).place(x=500, y=0, width=520, height=180)

        img2 = Image.open("D:/Seminar_4thsem/image/student_img3.jpg").resize((550, 130), Image.ANTIALIAS)
        self.photoimag3 = ImageTk.PhotoImage(img2)
        Label(self.root, image=self.photoimag3).place(x=1000, y=0, width=540, height=180)

        # ----------------------Background Image-------------------------
        bg_img = Image.open("D:/Seminar_4thsem/image/background_img1.jpg").resize((1550, 800), Image.ANTIALIAS)
        self.photoimag4 = ImageTk.PhotoImage(bg_img)
        bg_label = Label(self.root, image=self.photoimag4)
        bg_label.place(x=0, y=130, width=1550, height=710)

        # ----------------------Title Label-------------------------
        title_lbl = Label(bg_label, text="STUDENT MANAGEMENT SYSTEM", font=("Arial", 25, "bold"), bg="white", fg="green")
        title_lbl.place(x=0, y=0, width=1550, height=45)

        # ----------------------Main Frame-------------------------
        main_frame = Frame(bg_label, bd=2, bg="white")
        main_frame.place(x=15, y=50, width=1500, height=610)

        # ----------------------Left Frame-------------------------
        left_frame = LabelFrame(main_frame, bd=5, relief=RIDGE, text="Student Details", font=("Arial", 12, "bold"), bg="white")
        left_frame.place(x=10, y=10, width=730, height=580)

        # Top image in left frame
        img_left = Image.open("D:/Seminar_4thsem/image/left_frame_student_pic.jpg").resize((720, 130), Image.ANTIALIAS)
        self.photoimg_left = ImageTk.PhotoImage(img_left)
        Label(left_frame, image=self.photoimg_left).place(x=5, y=0, width=700, height=130)

        # ----------------------Current Course Frame-------------------------
        current_course_frame = LabelFrame(left_frame, bd=2, bg="white", relief=RIDGE, text="Current Course Information", font=("Arial", 12, "bold"))
        current_course_frame.place(x=5, y=135, width=710, height=100)

        # Department
        Label(current_course_frame, text="Department", font=("arial", 12, "bold"), bg="white").grid(row=0, column=0, padx=10, pady=5, sticky=W)
        dept_combo = ttk.Combobox(current_course_frame, textvariable=self.var_dept, font=("arial", 12), state="readonly", width=17)
        dept_combo["values"] = ("Select Department", "DCS", "LAW", "CHEMISTRY", "CIVIL", "ELECTRICAL", "MECHANICAL")
        dept_combo.current(0)
        dept_combo.grid(row=0, column=1, padx=10, pady=5, sticky=W)

        # Course
        Label(current_course_frame, text="Course", font=("arial", 12, "bold"), bg="white").grid(row=0, column=2, padx=10, pady=5, sticky=W)
        course_combo = ttk.Combobox(current_course_frame, textvariable=self.var_course, font=("arial", 12), state="readonly", width=17)
        course_combo["values"] = ("Select Course", "MCA", "BCA", "AI/ML", "PGDCA", "BSC IT", "MSC IT", "LLB", "LLM")
        course_combo.current(0)
        course_combo.grid(row=0, column=3, padx=10, pady=5, sticky=W)

        # Year
        Label(current_course_frame, text="Year", font=("arial", 12, "bold"), bg="white").grid(row=1, column=0, padx=10, pady=5, sticky=W)
        year_combo = ttk.Combobox(current_course_frame, textvariable=self.var_year, font=("arial", 12), state="readonly", width=17)
        year_combo["values"] = ("Select Year", "2024-25", "2023-24", "2022-23", "2021-22")
        year_combo.current(0)
        year_combo.grid(row=1, column=1, padx=10, pady=5, sticky=W)

        # Semester
        Label(current_course_frame, text="Semester", font=("arial", 12, "bold"), bg="white").grid(row=1, column=2, padx=10, pady=5, sticky=W)
        semester_combo = ttk.Combobox(current_course_frame, textvariable=self.var_semester, font=("arial", 12), state="readonly", width=17)
        semester_combo["values"] = ("Select Semester", "SEM 1", "SEM 2", "SEM 3", "SEM 4", "SEM 5", "SEM 6")
        semester_combo.current(0)
        semester_combo.grid(row=1, column=3, padx=10, pady=5, sticky=W)

        # ----------------------Class Student Frame-------------------------
        class_student_frame = LabelFrame(left_frame, bd=2, bg="white", relief=RIDGE, text="Class Student Information", font=("Arial", 12, "bold"))
        class_student_frame.place(x=5, y=240, width=710, height=200)

        # Row 1
        Label(class_student_frame, text="Student ID:", font=("arial", 12), bg="white").grid(row=0, column=0, padx=10, pady=5, sticky=W)
        ttk.Entry(class_student_frame,textvariable=self.var_stud_id, width=20, font=("arial", 12)).grid(row=0, column=1, padx=10, pady=5, sticky=W)

        Label(class_student_frame, text="Student Name:", font=("arial", 12), bg="white").grid(row=0, column=2, padx=10, pady=5, sticky=W)
        ttk.Entry(class_student_frame,textvariable=self.var_stud_name, width=20, font=("arial", 12)).grid(row=0, column=3, padx=10, pady=5, sticky=W)

        # Row 2
        Label(class_student_frame, text="Class Division:", font=("arial", 12), bg="white").grid(row=1, column=0, padx=10, pady=5, sticky=W)
        ttk.Entry(class_student_frame,textvariable=self.var_div, width=20, font=("arial", 12)).grid(row=1, column=1, padx=10, pady=5, sticky=W)

        Label(class_student_frame, text="Roll No:", font=("arial", 12), bg="white").grid(row=1, column=2, padx=10, pady=5, sticky=W)
        ttk.Entry(class_student_frame,textvariable=self.var_roll, width=20, font=("arial", 12)).grid(row=1, column=3, padx=10, pady=5, sticky=W)

        # Row 3
        Label(class_student_frame, text="Gender:", font=("arial", 12), bg="white").grid(row=2, column=0, padx=10, pady=5, sticky=W)
        ttk.Entry(class_student_frame,textvariable=self.var_gender, width=20, font=("arial", 12)).grid(row=2, column=1, padx=10, pady=5, sticky=W)

        Label(class_student_frame, text="DOB:", font=("arial", 12), bg="white").grid(row=2, column=2, padx=10, pady=5, sticky=W)
        ttk.Entry(class_student_frame,textvariable=self.var_dob, width=20, font=("arial", 12)).grid(row=2, column=3, padx=10, pady=5, sticky=W)

        # Row 4
        Label(class_student_frame, text="Email:", font=("arial", 12), bg="white").grid(row=3, column=0, padx=10, pady=5, sticky=W)
        ttk.Entry(class_student_frame,textvariable=self.var_email, width=20, font=("arial", 12)).grid(row=3, column=1, padx=10, pady=5, sticky=W)

        Label(class_student_frame, text="Phone No:", font=("arial", 12), bg="white").grid(row=3, column=2, padx=10, pady=5, sticky=W)
        ttk.Entry(class_student_frame, textvariable=self.var_phone, width=20, font=("arial", 12)).grid(row=3, column=3, padx=10, pady=5, sticky=W)

        # Row 5
        Label(class_student_frame, text="Address:", font=("arial", 12), bg="white").grid(row=4, column=0, padx=10, pady=5, sticky=W)
        ttk.Entry(class_student_frame, textvariable=self.var_address, width=20, font=("arial", 12)).grid(row=4, column=1, padx=10, pady=5, sticky=W)

        Label(class_student_frame, text="Teacher Name:", font=("arial", 12), bg="white").grid(row=4, column=2, padx=10, pady=5, sticky=W)
        ttk.Entry(class_student_frame, textvariable=self.var_teacher, width=20, font=("arial", 12)).grid(row=4, column=3, padx=10, pady=5, sticky=W)

        # Radio Buttons
        self.var_radio1 = StringVar()
        Radiobutton(left_frame, text="Take Photo Sample", variable=self.var_radio1, value="Yes", bg="white", font=("arial", 12)).place(x=10, y=450)
        Radiobutton(left_frame, text="No Photo Sample", variable=self.var_radio1, value="No", bg="white", font=("arial", 12)).place(x=200, y=450)

        # Buttons
        Button(left_frame, text="Save", width=15, command=self.insert_data, font=("arial", 12, "bold"), bg="blue", fg="white").place(x=10, y=480)
        Button(left_frame, text="Update", width=15, command=self.update_student,  font=("arial", 12, "bold"), bg="blue", fg="white").place(x=190, y=480)
        Button(left_frame, text="Delete", width=15, command=self.delete_student, font=("arial", 12, "bold"), bg="blue", fg="white").place(x=370, y=480)
        Button(left_frame, text="Reset", width=15, command=self.reset, font=("arial", 12, "bold"), bg="blue", fg="white").place(x=550, y=480)

        Button(left_frame, text="Take Photo Sample",command= self.genrate_dataset, width=30, font=("arial", 12, "bold"), bg="blue", fg="white").place(x=10, y=520)
        Button(left_frame, text="Update Photo Sample", width=30, font=("arial", 12, "bold"), bg="blue", fg="white").place(x=370, y=520)

        # ----------------------Right Frame-------------------------
        right_frame = LabelFrame(main_frame, bd=5, relief=RIDGE, text="Student Details", font=("Arial", 12, "bold"), bg="white")
        right_frame.place(x=760, y=10, width=720, height=580)

        # ----------------------Search System-------------------------
        search_frame = LabelFrame(right_frame, bd=2, relief=RIDGE, text="Search System", font=("Arial", 12, "bold"), bg="white")
        search_frame.place(x=10, y=10, width=690, height=70)

        Label(search_frame, text="Search By:", font=("arial", 12, "bold"), bg="white").grid(row=0, column=0, padx=10, pady=5, sticky=W)

        self.search_var = StringVar()
        search_combo = ttk.Combobox(search_frame, textvariable=self.search_var, font=("arial", 12), state="readonly", width=12)
        search_combo["values"] = ("Select", "Roll_No", "Phone", "Name")
        search_combo.current(0)
        search_combo.grid(row=0, column=1, padx=10, pady=5, sticky=W)

        self.search_txt = StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_txt, font=("arial", 12), width=15)
        search_entry.grid(row=0, column=2, padx=10, pady=5, sticky=W)

        Button(search_frame, text="Search", width=10, font=("arial", 12, "bold"), bg="blue", fg="white").grid(row=0, column=3, padx=10)
        Button(search_frame, text="Show All", width=10, font=("arial", 12, "bold"), bg="green", fg="white").grid(row=0, column=4, padx=10)

        # ----------------------Table Frame-------------------------
        table_frame = Frame(right_frame, bd=2, relief=RIDGE, bg="white")
        table_frame.place(x=10, y=90, width=690, height=450)

        scroll_x = ttk.Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(table_frame, orient=VERTICAL)

        self.student_table = ttk.Treeview(table_frame, columns=(
            "Dept", "Course", "Year", "Sem", "Id", "Name", "Div", "Roll", "Gender", "DOB", "Email", "Phone", "Address", "Teacher", "Photo"),
            xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set
        )

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.student_table.xview)
        scroll_y.config(command=self.student_table.yview)

        self.student_table.heading("Dept", text="Department")
        self.student_table.heading("Course", text="Course")
        self.student_table.heading("Year", text="Year")
        self.student_table.heading("Sem", text="Semester")
        self.student_table.heading("Id", text="Student ID")
        self.student_table.heading("Name", text="Name")
        self.student_table.heading("Div", text="Division")
        self.student_table.heading("Roll", text="Roll No")
        self.student_table.heading("Gender", text="Gender")
        self.student_table.heading("DOB", text="DOB")
        self.student_table.heading("Email", text="Email")
        self.student_table.heading("Phone", text="Phone")
        self.student_table.heading("Address", text="Address")
        self.student_table.heading("Teacher", text="Teacher")
        self.student_table.heading("Photo", text="PhotoSample")

        self.student_table["show"] = "headings"
        
        self.student_table.column("Dept", width=100)
        self.student_table.column("Course", width=100)
        self.student_table.column("Year", width=100)
        self.student_table.column("Sem", width=100)
        self.student_table.column("Id", width=100)
        self.student_table.column("Name", width=150)
        self.student_table.column("Div", width=100)
        self.student_table.column("Roll", width=100)
        self.student_table.column("Gender", width=100)
        self.student_table.column("DOB", width=100)
        self.student_table.column("Email", width=150)
        self.student_table.column("Phone", width=100)
        self.student_table.column("Address", width=200)
        self.student_table.column("Teacher", width=150)
        self.student_table.column("Photo", width=150)

        self.student_table.pack(fill=BOTH, expand=1)
        # Bind click
        self.student_table.bind("<ButtonRelease>", self.get_cursor)
        self.fetch_data()

    #============================function decreation============================
    def insert_data(self):
        if self.var_dept.get() == "Select Department" or self.var_stud_name.get() == "" or self.var_stud_id.get() == "":
            messagebox.showerror("Error","All Fileds Are Required",parent=self.root)
        else:
            try:
                conn = mysql.connector.connect(host="localhost",username="root",password="root",database="face_recognizer",port=3310)
                my_cursor = conn.cursor()
                my_cursor.execute("insert into tbl_student values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(self.var_dept.get()
                                                                                                                   ,self.var_course.get()
                                                                                                                   ,self.var_year.get()
                                                                                                                   ,self.var_semester.get()
                                                                                                                   ,self.var_stud_id.get()
                                                                                                                   ,self.var_stud_name.get()
                                                                                                                   ,self.var_div.get()
                                                                                                                   ,self.var_roll.get()
                                                                                                                   ,self.var_gender.get()
                                                                                                                   ,self.var_dob.get()
                                                                                                                   ,self.var_email.get()
                                                                                                                   ,self.var_phone.get()
                                                                                                                   ,self.var_address.get()
                                                                                                                   ,self.var_teacher.get()
                                                                                                                   ,self.var_radio1.get()
                                                                                                                   ))
                conn.commit()
                self.fetch_data()
                self.reset()
                conn.close()
                messagebox.showinfo("Success","Student Details Record Has Been Added Successfully...!")
            except Exception as ex:
                messagebox.showwarning("Warning",f"Something Want Worng : {str(ex)}", parent=self.root)
    
    def fetch_data(self):
        conn = mysql.connector.connect(host="localhost",username="root",password="root",database="face_recognizer",port=3310)
        my_cursor = conn.cursor()
        my_cursor.execute("SELECT * FROM tbl_student")
        rows = my_cursor.fetchall()

        if len(rows) != 0:
            self.student_table.delete(*self.student_table.get_children())

            for i in rows:
                self.student_table.insert("",END,values=i)
            conn.commit()
        conn.close()
    
    def get_cursor(self, event=""):
        cursor_row = self.student_table.focus()
        content = self.student_table.item(cursor_row)
        row = content["values"]

        if row:  # safety check
            self.var_dept.set(row[0])
            self.var_course.set(row[1])
            self.var_year.set(row[2])
            self.var_semester.set(row[3])
            self.var_stud_id.set(row[4])
            self.var_stud_name.set(row[5])
            self.var_div.set(row[6])
            self.var_roll.set(row[7])
            self.var_gender.set(row[8])
            self.var_dob.set(row[9])
            self.var_email.set(row[10])
            self.var_phone.set(row[11])
            self.var_address.set(row[12])
            self.var_teacher.set(row[13])
            self.var_radio1.set(row[14])

    def update_student(self):
        if self.var_dept.get() == "Select Department" or self.var_stud_name.get() == "" or self.var_stud_id.get() == "":
            messagebox.showerror("Error","All Fileds Are Required",parent=self.root)
        else:
            try:
                conn = mysql.connector.connect(host="localhost",username="root",password="root",database="face_recognizer",port=3310)
                my_cursor = conn.cursor()
                my_cursor.execute("update tbl_student set dept=%s,course=%s,year=%s,semester=%s,name=%s,division=%s,rollno=%s,gender=%s,dob=%s,email=%s,phone=%s,address=%s,teacher=%s,photosample=%s where student_id=%s",(self.var_dept.get()
                                                                                                                                                                                                                            ,self.var_course.get()
                                                                                                                                                                                                                            ,self.var_year.get()
                                                                                                                                                                                                                            ,self.var_semester.get()
                                                                                                                                                                                                                            ,self.var_stud_name.get()
                                                                                                                                                                                                                            ,self.var_div.get()
                                                                                                                                                                                                                            ,self.var_roll.get()
                                                                                                                                                                                                                            ,self.var_gender.get()
                                                                                                                                                                                                                            ,self.var_dob.get()
                                                                                                                                                                                                                            ,self.var_email.get()
                                                                                                                                                                                                                            ,self.var_phone.get()
                                                                                                                                                                                                                            ,self.var_address.get()
                                                                                                                                                                                                                            ,self.var_teacher.get()
                                                                                                                                                                                                                            ,self.var_radio1.get()
                                                                                                                                                                                                                            ,self.var_stud_id.get()
                                                                                                                                                                                                                            ))
                conn.commit()
                self.fetch_data()
                self.reset()
                conn.close()
                messagebox.showinfo("Record Updated","Student Details Has Been Updated Successfully...!",parent=self.root)
            except Exception as ex:
                messagebox.showwarning("Warning",f"Something Want Worng : {str(ex)}", parent=self.root)
    
    def delete_student(self):
        delete=messagebox.askyesno("Face Bae Attendance Management System","Are You Sure You Want to Delete?",parent=self.root)

        if delete>0:
            conn = mysql.connector.connect(host="localhost",username="root",password="root",database="face_recognizer",port=3310)
            my_cursor = conn.cursor()
            query = "delete from tbl_student where student_id = %s"
            value = (self.var_stud_id.get(),)
            my_cursor.execute(query,value)
        else:
            if not delete:
                return
        conn.commit()

        self.fetch_data()
        self.reset()
        conn.close()

    def reset(self):
        self.var_dept.set("Select Department")
        self.var_course.set("Select Course")
        self.var_year.set("Select Year")
        self.var_semester.set("Select Semster")
        self.var_stud_id.set("")
        self.var_stud_name.set("")
        self.var_div.set("Select Division")
        self.var_roll.set("")
        self.var_gender.set("Male")
        self.var_dob.set("")
        self.var_email.set("")
        self.var_phone.set("")
        self.var_address.set("")
        self.var_teacher.set("")

    # def genrate_dataset(self):
    #     if self.var_dept.get() == "Select Department" or self.var_stud_name.get() == "" or self.var_stud_id.get() == "":
    #         messagebox.showerror("Error","All Fileds Are Required",parent=self.root)
    #     else:
    #         try:
    #             conn = mysql.connector.connect(host="localhost",username="root",password="root",database="face_recognizer",port=3310)
    #             my_cursor = conn.cursor()
    #             my_cursor.execute("select * from tbl_student")
    #             myresult = my_cursor.fetchall()
    #             id = 0
                
    #             for x in myresult:
    #                 id+=1
    #             my_cursor.execute("update tbl_student set dept=%s,course=%s,year=%s,semester=%s,name=%s,division=%s,rollno=%s,gender=%s,dob=%s,email=%s,phone=%s,address=%s,teacher=%s,photosample=%s where student_id=%s",(self.var_dept.get()
    #                                                                                                                                                                                                                         ,self.var_course.get()
    #                                                                                                                                                                                                                         ,self.var_year.get()
    #                                                                                                                                                                                                                         ,self.var_semester.get()
    #                                                                                                                                                                                                                         ,self.var_stud_name.get()
    #                                                                                                                                                                                                                         ,self.var_div.get()
    #                                                                                                                                                                                                                         ,self.var_roll.get()
    #                                                                                                                                                                                                                         ,self.var_gender.get()
    #                                                                                                                                                                                                                         ,self.var_dob.get()
    #                                                                                                                                                                                                                         ,self.var_email.get()
    #                                                                                                                                                                                                                         ,self.var_phone.get()
    #                                                                                                                                                                                                                         ,self.var_address.get()
    #                                                                                                                                                                                                                         ,self.var_teacher.get()
    #                                                                                                                                                                                                                         ,self.var_radio1.get()
    #                                                                                                                                                                                                                         ,self.var_stud_id.get()==id+1
    #                                                                                                                                                                                                                         ))
    #             conn.commit()
    #             self.fetch_data()
    #             self.reset()
    #             conn.close()
    
    #             #===============================Load Predefined Data On Face frontals from opencv==================
    #             face_classifier = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

    #             def face_cropped(img):
    #                 gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #                 faces = face_classifier.detectMultiScale(gray, 1.3, 5)
    #                 #Scaling factore = 1.3
    #                 #Minimum Neighbor = 5

    #                 for (x,y,w,h) in faces:
    #                     face_cropped = img[y:y+h,x:x+w]
    #                     return face_cropped
                
    #             cap = cv2.VideoCapture(0)
    #             img_id = 0

    #             while True:
    #                 ret, my_frame = cap.read()
    #                 if face_cropped(my_frame) is not None:
    #                     img_id += 1
    #                     face = cv2.resize(face_cropped(my_frame), (650, 650))
    #                     face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
    #                     file_name_path = "data/user."+str(id)+"."+str(img_id)+".jpg"
    #                     cv2.imwrite(file_name_path, face)

    #                     cv2.putText(face, str(img_id), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
    #                     cv2.imshow("Capturing Faces", face)

    #                 if cv2.waitKey(1) == 13 or int(img_id) == 5:  # Press Enter or collect 100 samples
    #                     break
    #             cap.release()
    #             cv2.destroyAllWindows()
    #             messagebox.showinfo("Result", "Generating dataset completed!", parent=self.root)
    #         except Exception as ex:
    #                 messagebox.showwarning("Warning",f"Something Want Worng : {str(ex)}", parent=self.root)
    

    def genrate_dataset(self):
        if self.var_dept.get() == "Select Department" or self.var_stud_name.get() == "" or self.var_stud_id.get() == "":
            messagebox.showerror("Error", "All Fields Are Required", parent=self.root)
        else:
            try:
                conn = mysql.connector.connect(host="localhost", username="root", password="root", database="face_recognizer", port=3310)
                my_cursor = conn.cursor()

                # Update student record before capturing photos
                my_cursor.execute("UPDATE tbl_student SET dept=%s, course=%s, year=%s, semester=%s, name=%s, division=%s, rollno=%s, gender=%s, dob=%s, email=%s, phone=%s, address=%s, teacher=%s, photosample=%s WHERE student_id=%s", (
                    self.var_dept.get(),
                    self.var_course.get(),
                    self.var_year.get(),
                    self.var_semester.get(),
                    self.var_stud_name.get(),
                    self.var_div.get(),
                    self.var_roll.get(),
                    self.var_gender.get(),
                    self.var_dob.get(),
                    self.var_email.get(),
                    self.var_phone.get(),
                    self.var_address.get(),
                    self.var_teacher.get(),
                    self.var_radio1.get(),
                    self.var_stud_id.get() == id
                ))

                conn.commit()
                self.fetch_data()
                self.reset()
                conn.close()

                # =============== Load Predefined Face Classifier ===============
                face_classifier = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

                def face_cropped(img):
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    faces = face_classifier.detectMultiScale(gray, 1.3, 5)
                    for (x, y, w, h) in faces:
                        face = img[y:y+h, x:x+w]
                        return face

                cap = cv2.VideoCapture(0)
                img_id = 0

                student_id = self.var_stud_id.get()  # Use form input as unique ID

                while True:
                    ret, my_frame = cap.read()
                    if face_cropped(my_frame) is not None:
                        img_id += 1
                        face = cv2.resize(face_cropped(my_frame), (650, 650))

                        # Create unique filename with timestamp
                        timestamp = int(time.time())
                        file_name_path = f"data/user.{student_id}.{timestamp}_{img_id}.jpg"

                        cv2.imwrite(file_name_path, face)

                        # Show captured face
                        cv2.putText(face, str(img_id), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
                        cv2.imshow("Capturing Faces", face)

                    if cv2.waitKey(1) == 13 or int(img_id) == 5:
                        break

                cap.release()
                cv2.destroyAllWindows()
                messagebox.showinfo("Result", "Generating dataset completed!", parent=self.root)

            except Exception as ex:
                messagebox.showwarning("Warning", f"Something Went Wrong: {str(ex)}", parent=self.root)



if __name__ == "__main__":
    root = Tk()
    obj = Student(root)
    root.mainloop()
