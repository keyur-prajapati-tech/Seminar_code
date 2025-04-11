from tkinter import *
from tkinter import ttk
from PIL import Image,ImageTk #pip install pillow
from student import Student
from train_data import TrainData
import os


class Face_Recognition_System:
    def __init__(self,root):
        self.root = root
        self.root.title("Face Recognition System")
        self.root.geometry("1550x800+0+0")

        #----------------------Image1--------------------------------
        img = Image.open("D:\Seminar_4thsem\image\home_page_img.webp")
        img = img.resize((550,130),Image.ANTIALIAS)
        self.photoimag = ImageTk.PhotoImage(img)

        f_label = Label(self.root,image=self.photoimag)
        f_label.place(x=0,y=0,width=530,height=180)

        #-----------------------Image2-------------------------------
        img1 = Image.open("D:\Seminar_4thsem\image\home_page_img_3.png")
        img1 = img1.resize((550,130),Image.ANTIALIAS)
        self.photoimag2 = ImageTk.PhotoImage(img1)

        f_label = Label(self.root,image=self.photoimag2)
        f_label.place(x=500,y=0,width=520,height=180)

        #---------------------Image3----------------------------------
        img2 = Image.open(r"D:\Seminar_4thsem\image\img_1.webp")
        img2 = img2.resize((550,130),Image.ANTIALIAS)
        self.photoimag3 = ImageTk.PhotoImage(img2)

        f_label = Label(self.root,image=self.photoimag3)
        f_label.place(x=1000,y=0,width=540,height=180)

        #-----------------------home image---------------------------
        img3 = Image.open(r"D:\Seminar_4thsem\image\background_img1.jpg")
        # img3 = Image.open(r"D:\Seminar_4thsem\image\backgroung_image.jpg")
        img3 = img3.resize((1550,800),Image.ANTIALIAS)
        self.photoimag4 = ImageTk.PhotoImage(img3)

        bg_img = Label(self.root,image=self.photoimag4)
        bg_img.place(x=0,y=130,width=1550,height=710)

        #---------------title-----------------------------
        title_lbl = Label(bg_img,text="FACE RECOGNITION ATTENDENCE SYSTEM SOFTWARE",font=("Arial",25,"bold"),bg="navy",fg="white",border="3px solid #000")
        title_lbl.place(x=0,y=0,width=1560,height=45)

        #---------------Student Button--------------------
        img4 = Image.open(r"image\student.jpg")
        img4 = img4.resize((220,220),Image.ANTIALIAS)
        self.photoimag_student = ImageTk.PhotoImage(img4)

        b1 = Button(bg_img,image=self.photoimag_student,cursor="hand2",command=self.student_details,border="3px solid #000",borderwidth="5px")
        b1.place(x=200,y=100,width=220,height=220)

        b1_1 = Button(bg_img,text="Employee Details",cursor="hand2",command=self.student_details,font=("Arial",15,"bold"),bg="navy",fg="white",border="3px solid #000")
        b1_1.place(x=200,y=300,width=220,height=40)


        #---------------Face Recognition Button--------------------
        img5 = Image.open(r"image\face_detection_img.jpg")
        img5 = img5.resize((220,220),Image.ANTIALIAS)
        self.photoimag_facerecognition = ImageTk.PhotoImage(img5)

        b2 = Button(bg_img,image=self.photoimag_facerecognition,cursor="hand2",border="3px solid #000",borderwidth="5px")
        b2.place(x=500,y=100,width=220,height=220)

        b2_1 = Button(bg_img,text="Face Detector",cursor="hand2",font=("Arial",15,"bold"),bg="navy",fg="white",border="3px solid #000")
        b2_1.place(x=500,y=300,width=220,height=40)

        #---------------Face Recognition Button--------------------
        img6 = Image.open(r"image\attendance_img.jpg")
        img6 = img6.resize((220,220),Image.ANTIALIAS)
        self.photoimag_btn3 = ImageTk.PhotoImage(img6)

        b3 = Button(bg_img,image=self.photoimag_btn3,cursor="hand2",border="3px solid #000",borderwidth="5px")
        b3.place(x=800,y=100,width=220,height=220)

        b3_1 = Button(bg_img,text="Attendance",cursor="hand2",font=("Arial",15,"bold"),bg="navy",fg="white",border="3px solid #000")
        b3_1.place(x=800,y=300,width=220,height=40)

        #---------------Face Recognition Button--------------------
        img7 = Image.open(r"image\help_desk_img.jpg")
        img7 = img7.resize((220,220),Image.ANTIALIAS)
        self.photoimag_btn4 = ImageTk.PhotoImage(img7)

        b4 = Button(bg_img,image=self.photoimag_btn4,cursor="hand2",border="3px solid #000",borderwidth="5px")
        b4.place(x=1100,y=100,width=220,height=220)

        b4_1 = Button(bg_img,text="Help Desk",cursor="hand2",font=("Arial",15,"bold"),bg="navy",fg="white",border="3px solid #000")
        b4_1.place(x=1100,y=300,width=220,height=40)

        #---------------Face Recognition Button--------------------
        img8 = Image.open(r"image\train_data_img.png")
        img8 = img8.resize((220,220),Image.ANTIALIAS)
        self.photoimag_btn5 = ImageTk.PhotoImage(img8)

        b5 = Button(bg_img,image=self.photoimag_btn5,cursor="hand2", command=self.train_student_data,border="3px solid #000",borderwidth="5px")
        b5.place(x=200,y=400,width=220,height=220)

        b5_1 = Button(bg_img,text="Train Data",cursor="hand2", command=self.train_student_data,font=("Arial",15,"bold"),bg="navy",fg="white",border="3px solid #000")
        b5_1.place(x=200,y=600,width=220,height=40)

        #---------------Face Recognition Button--------------------
        img9 = Image.open(r"image\photos.png")
        img9 = img9.resize((220,220),Image.ANTIALIAS)
        self.photoimag_btn6 = ImageTk.PhotoImage(img9)

        b6 = Button(bg_img,image=self.photoimag_btn6, command=self.open_img ,cursor="hand2",border="3px solid #000",borderwidth="5px")
        b6.place(x=500,y=400,width=220,height=220)

        b6_1 = Button(bg_img,text="Photos",cursor="hand2", command=self.open_img ,font=("Arial",15,"bold"),bg="navy",fg="white",border="3px solid #000")
        b6_1.place(x=500,y=600,width=220,height=40)

        #---------------Face Recognition Button--------------------
        img10 = Image.open(r"image\img_devloper.jpg")
        img10 = img10.resize((220,220),Image.ANTIALIAS)
        self.photoimag_btn7 = ImageTk.PhotoImage(img10)

        b7 = Button(bg_img,image=self.photoimag_btn7,cursor="hand2",border="3px solid #000",borderwidth="5px")
        b7.place(x=800,y=400,width=220,height=220)

        b7_1 = Button(bg_img,text="Devloper",cursor="hand2",font=("Arial",15,"bold"),bg="navy",fg="white",border="3px solid #000")
        b7_1.place(x=800,y=600,width=220,height=40)

        #---------------Face Recognition Button--------------------
        img11 = Image.open(r"image\exit_img.jpg")
        img11 = img11.resize((220,220),Image.ANTIALIAS)
        self.photoimag_btn8 = ImageTk.PhotoImage(img11)

        b7 = Button(bg_img,image=self.photoimag_btn8,cursor="hand2",border="3px solid #000",borderwidth="5px")
        b7.place(x=1100,y=400,width=220,height=220)

        b7_1 = Button(bg_img,text="Exit",cursor="hand2",font=("Arial",15,"bold"),bg="navy",fg="white",border="3px solid #000")
        b7_1.place(x=1100,y=600,width=220,height=40)


    #=======================Function Buttons======================
    def student_details(self):
        self.new_window = Toplevel(self.root)
        self.app = Student(self.new_window)
    
    def train_student_data(self):
        self.new_window = Toplevel(self.root)
        self.app = TrainData(self.new_window)

    def open_img(self):
        os.startfile("data")

if __name__ == "__main__":
    root = Tk()
    obj = Face_Recognition_System(root)
    root.mainloop()