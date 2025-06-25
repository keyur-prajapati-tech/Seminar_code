from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import os
import cv2
import numpy as np
from tkinter import messagebox
import mysql.connector
from datetime import datetime

class Attendance_Filter:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1550x800+0+0")
        self.root.title("Face Recognition Attendance System")

        # Title
        title_lbl = Label(self.root, text="ATTENDANCE MANAGEMENT SYSTEM", font=("times new roman", 30, "bold"),
                         bg="navy", fg="white")
        title_lbl.place(x=0, y=0, width=1550, height=50)

        # Back Button
        back_btn = Button(self.root, text="Back", command=self.root.destroy, font=("times new roman", 13, "bold"),
                         bg="red", fg="white", relief="ridge", borderwidth=2)
        back_btn.place(x=1420, y=6, width=100, height=40)

        # Main Frame
        main_frame = Frame(self.root, bd=2, bg="white", relief=RIDGE)
        main_frame.place(x=10, y=60, width=1530, height=730)

        # Left Frame - Student Attendance Details
        left_frame = LabelFrame(main_frame, bd=4, bg="white", relief=RIDGE, text="Student Attendance Details",
                              font=("times new roman", 12, "bold"))
        left_frame.place(x=10, y=10, width=750, height=350)

        # Attendance Details Labels
        details_labels = [
            ("Attendance Id:", 0, 0), ("Rule:", 1, 0), ("Name:", 2, 0),
            ("Department:", 3, 0), ("Time:", 4, 0), ("Date:", 5, 0),
            ("Attendance Status:", 6, 0), ("Status:", 7, 0)
        ]

        self.attendance_details = {}
        for text, row, column in details_labels:
            label = Label(left_frame, text=text, font=("times new roman", 12, "bold"), bg="white")
            label.grid(row=row, column=column, padx=10, pady=5, sticky=W)
            
            entry = ttk.Entry(left_frame, width=25, font=("times new roman", 12))
            entry.grid(row=row, column=column+1, padx=10, pady=5, sticky=W)
            self.attendance_details[text.split(":")[0].strip().lower().replace(" ", "_")] = entry

        # Right Frame - Attendance Records
        right_frame = LabelFrame(main_frame, bd=4, bg="white", relief=RIDGE, text="Attendance Details",
                               font=("times new roman", 12, "bold"))
        right_frame.place(x=770, y=10, width=750, height=350)

        # Attendance Table
        scroll_x = ttk.Scrollbar(right_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(right_frame, orient=VERTICAL)

        self.attendance_table = ttk.Treeview(right_frame, columns=(
            "attendance_id", "rule", "name", "department", "time", "date", "status"),
            xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.attendance_table.xview)
        scroll_y.config(command=self.attendance_table.yview)

        self.attendance_table.heading("attendance_id", text="Attendance ID")
        self.attendance_table.heading("rule", text="Rule")
        self.attendance_table.heading("name", text="Name")
        self.attendance_table.heading("department", text="Department")
        self.attendance_table.heading("time", text="Time")
        self.attendance_table.heading("date", text="Date")
        self.attendance_table.heading("status", text="Status")

        self.attendance_table["show"] = "headings"
        
        self.attendance_table.column("attendance_id", width=100)
        self.attendance_table.column("rule", width=100)
        self.attendance_table.column("name", width=150)
        self.attendance_table.column("department", width=100)
        self.attendance_table.column("time", width=100)
        self.attendance_table.column("date", width=100)
        self.attendance_table.column("status", width=100)

        self.attendance_table.pack(fill=BOTH, expand=1)
        self.attendance_table.bind("<ButtonRelease>", self.get_cursor)
        self.fetch_data()

        # Bottom Frame - Controls
        bottom_frame = LabelFrame(main_frame, bd=4, bg="white", relief=RIDGE, text="Targets",
                                font=("times new roman", 12, "bold"))
        bottom_frame.place(x=10, y=370, width=1510, height=350)

        # Buttons
        export_btn = Button(bottom_frame, text="Export CSV", command=self.export_csv,
                          font=("times new roman", 12, "bold"), bg="green", fg="white")
        export_btn.place(x=50, y=20, width=150, height=40)

        update_btn = Button(bottom_frame, text="Update", command=self.update_data,
                          font=("times new roman", 12, "bold"), bg="blue", fg="white")
        update_btn.place(x=250, y=20, width=150, height=40)

        reset_btn = Button(bottom_frame, text="Reset", command=self.reset,
                         font=("times new roman", 12, "bold"), bg="red", fg="white")
        reset_btn.place(x=450, y=20, width=150, height=40)

        # Search Frame
        search_frame = LabelFrame(bottom_frame, bd=2, bg="white", relief=RIDGE, text="Search Attendance",
                                font=("times new roman", 12, "bold"))
        search_frame.place(x=650, y=10, width=800, height=70)

        search_label = Label(search_frame, text="Type here to search:", font=("times new roman", 12, "bold"), bg="white")
        search_label.grid(row=0, column=0, padx=10, pady=5, sticky=W)

        self.search_var = StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=25, font=("times new roman", 12))
        search_entry.grid(row=0, column=1, padx=10, pady=5, sticky=W)

        search_btn = Button(search_frame, text="Search", command=self.search_data,
                          font=("times new roman", 12, "bold"), bg="navy", fg="white")
        search_btn.grid(row=0, column=2, padx=10, pady=5)

        show_all_btn = Button(search_frame, text="Show All", command=self.fetch_data,
                            font=("times new roman", 12, "bold"), bg="gray", fg="white")
        show_all_btn.grid(row=0, column=3, padx=10, pady=5)

        # Filter Options
        filter_frame = LabelFrame(bottom_frame, bd=2, bg="white", relief=RIDGE, text="Filter Options",
                                font=("times new roman", 12, "bold"))
        filter_frame.place(x=50, y=80, width=1400, height=100)

        # Date Filter
        date_label = Label(filter_frame, text="Date:", font=("times new roman", 12, "bold"), bg="white")
        date_label.grid(row=0, column=0, padx=10, pady=5, sticky=W)

        self.date_from_var = StringVar()
        date_from_entry = ttk.Entry(filter_frame, textvariable=self.date_from_var, width=15, font=("times new roman", 12))
        date_from_entry.grid(row=0, column=1, padx=5, pady=5, sticky=W)

        to_label = Label(filter_frame, text="to", font=("times new roman", 12), bg="white")
        to_label.grid(row=0, column=2, padx=5, pady=5)

        self.date_to_var = StringVar()
        date_to_entry = ttk.Entry(filter_frame, textvariable=self.date_to_var, width=15, font=("times new roman", 12))
        date_to_entry.grid(row=0, column=3, padx=5, pady=5, sticky=W)

        # Department Filter
        dept_label = Label(filter_frame, text="Department:", font=("times new roman", 12, "bold"), bg="white")
        dept_label.grid(row=0, column=4, padx=10, pady=5, sticky=W)

        self.dept_var = StringVar()
        dept_combo = ttk.Combobox(filter_frame, textvariable=self.dept_var, font=("times new roman", 12), state="readonly", width=15)
        dept_combo["values"] = ("All", "DCS", "LAW", "Mechanical", "Civil", "Chemistry")
        dept_combo.current(0)
        dept_combo.grid(row=0, column=5, padx=5, pady=5, sticky=W)

        # Status Filter
        status_label = Label(filter_frame, text="Status:", font=("times new roman", 12, "bold"), bg="white")
        status_label.grid(row=0, column=6, padx=10, pady=5, sticky=W)

        self.status_var = StringVar()
        status_combo = ttk.Combobox(filter_frame, textvariable=self.status_var, font=("times new roman", 12), state="readonly", width=15)
        status_combo["values"] = ("All", "Present", "Absent", "Late")
        status_combo.current(0)
        status_combo.grid(row=0, column=7, padx=5, pady=5, sticky=W)

        filter_btn = Button(filter_frame, text="Apply Filter", command=self.apply_filter,
                          font=("times new roman", 12, "bold"), bg="green", fg="white")
        filter_btn.grid(row=0, column=8, padx=10, pady=5)

    def fetch_data(self):
        try:
            conn = mysql.connector.connect(host="localhost", user="root", password="root", database="face_recognizer", port=3310)
            my_cursor = conn.cursor()
            my_cursor.execute("SELECT * FROM tbl_attendance")
            data = my_cursor.fetchall()
            
            if len(data) != 0:
                self.attendance_table.delete(*self.attendance_table.get_children())
                for row in data:
                    self.attendance_table.insert("", END, values=row)
                conn.commit()
            conn.close()
        except Exception as es:
            messagebox.showerror("Error", f"Due To:{str(es)}", parent=self.root)

    def get_cursor(self, event=""):
        cursor_row = self.attendance_table.focus()
        content = self.attendance_table.item(cursor_row)
        row = content["values"]
        
        if row:
            self.attendance_details["attendance_id"].delete(0, END)
            self.attendance_details["attendance_id"].insert(0, row[0])
            
            self.attendance_details["rule"].delete(0, END)
            self.attendance_details["rule"].insert(0, row[1])
            
            self.attendance_details["name"].delete(0, END)
            self.attendance_details["name"].insert(0, row[2])
            
            self.attendance_details["department"].delete(0, END)
            self.attendance_details["department"].insert(0, row[3])
            
            self.attendance_details["time"].delete(0, END)
            self.attendance_details["time"].insert(0, row[4])
            
            self.attendance_details["date"].delete(0, END)
            self.attendance_details["date"].insert(0, row[5])
            
            self.attendance_details["attendance_status"].delete(0, END)
            self.attendance_details["attendance_status"].insert(0, row[6])
            
            self.attendance_details["status"].delete(0, END)
            self.attendance_details["status"].insert(0, row[7])

    def update_data(self):
        if self.attendance_details["attendance_id"].get() == "":
            messagebox.showerror("Error", "Please select an attendance record to update", parent=self.root)
        else:
            try:
                conn = mysql.connector.connect(host="localhost", user="root", password="root", database="face_recognizer", port=3310)
                my_cursor = conn.cursor()
                
                query = """UPDATE tbl_attendance SET 
                          rule=%s, name=%s, department=%s, time=%s, 
                          date=%s, status=%s, remarks=%s 
                          WHERE attendance_id=%s"""
                
                values = (
                    self.attendance_details["rule"].get(),
                    self.attendance_details["name"].get(),
                    self.attendance_details["department"].get(),
                    self.attendance_details["time"].get(),
                    self.attendance_details["date"].get(),
                    self.attendance_details["attendance_status"].get(),
                    self.attendance_details["status"].get(),
                    self.attendance_details["attendance_id"].get()
                )
                
                my_cursor.execute(query, values)
                conn.commit()
                self.fetch_data()
                conn.close()
                messagebox.showinfo("Success", "Attendance record updated successfully", parent=self.root)
            except Exception as es:
                messagebox.showerror("Error", f"Due To:{str(es)}", parent=self.root)

    def reset(self):
        for entry in self.attendance_details.values():
            entry.delete(0, END)
        self.fetch_data()

    def search_data(self):
        if self.search_var.get() == "":
            messagebox.showerror("Error", "Please enter search criteria", parent=self.root)
        else:
            try:
                conn = mysql.connector.connect(host="localhost", user="root", password="root", database="face_recognizer", port=3310)
                my_cursor = conn.cursor()
                
                query = "SELECT * FROM tbl_attendance WHERE " + \
                        "attendance_id LIKE %s OR name LIKE %s OR department LIKE %s OR date LIKE %s OR status LIKE %s"
                
                search_text = "%" + self.search_var.get() + "%"
                my_cursor.execute(query, (search_text, search_text, search_text, search_text, search_text))
                data = my_cursor.fetchall()
                
                if len(data) != 0:
                    self.attendance_table.delete(*self.attendance_table.get_children())
                    for row in data:
                        self.attendance_table.insert("", END, values=row)
                    conn.commit()
                else:
                    messagebox.showinfo("Info", "No matching records found", parent=self.root)
                conn.close()
            except Exception as es:
                messagebox.showerror("Error", f"Due To:{str(es)}", parent=self.root)

    def apply_filter(self):
        try:
            conn = mysql.connector.connect(host="localhost", user="root", password="root", database="face_recognizer", port=3310)
            my_cursor = conn.cursor()
            
            base_query = "SELECT * FROM tbl_attendance WHERE 1=1"
            conditions = []
            params = []
            
            # Date filter
            if self.date_from_var.get() and self.date_to_var.get():
                conditions.append("date BETWEEN %s AND %s")
                params.extend([self.date_from_var.get(), self.date_to_var.get()])
            
            # Department filter
            if self.dept_var.get() != "All":
                conditions.append("dept = %s")
                params.append(self.dept_var.get())
            
            # Status filter
            if self.status_var.get() != "All":
                conditions.append("status = %s")
                params.append(self.status_var.get())
            
            if conditions:
                query = base_query + " AND " + " AND ".join(conditions)
            else:
                query = base_query
                
            my_cursor.execute(query, tuple(params))
            data = my_cursor.fetchall()
            
            if len(data) != 0:
                self.attendance_table.delete(*self.attendance_table.get_children())
                for row in data:
                    self.attendance_table.insert("", END, values=row)
                conn.commit()
            else:
                messagebox.showinfo("Info", "No records match the filter criteria", parent=self.root)
            conn.close()
        except Exception as es:
            messagebox.showerror("Error", f"Due To:{str(es)}", parent=self.root)

    def export_csv(self):
        try:
            if not os.path.exists("Attendance_Reports"):
                os.makedirs("Attendance_Reports")
            
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"Attendance_Reports/attendance_report_{timestamp}.csv"
            
            with open(filename, "w") as f:
                f.write("Attendance ID,Rule,Name,Department,Time,Date,Status,Remarks\n")
                
                conn = mysql.connector.connect(host="localhost", user="root", password="root", database="face_recognizer", port=3310)
                my_cursor = conn.cursor()
                my_cursor.execute("SELECT * FROM tbl_attendance")
                data = my_cursor.fetchall()
                
                for row in data:
                    f.write(",".join(str(item) for item in row) + "\n")
                
                conn.close()
            
            messagebox.showinfo("Success", f"Attendance data exported to {filename}", parent=self.root)
        except Exception as es:
            messagebox.showerror("Error", f"Due To:{str(es)}", parent=self.root)

if __name__ == "__main__":
    root = Tk()
    obj = Attendance_Filter(root)
    root.mainloop()