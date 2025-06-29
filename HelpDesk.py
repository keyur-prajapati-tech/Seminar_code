from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import webbrowser

class HelpDesk:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1550x800+0+0")
        self.root.title("Help Desk - Attendance Management System")
        self.root.config(bg="white")

        # ====================== Title Bar ======================
        title_lbl = Label(
            self.root,
            text="HELP DESK",
            font=("Helvetica", 30, "bold"),
            bg="navy",
            fg="white",
            padx=10,
            pady=10
        )
        title_lbl.pack(fill=X)

        # Back Button
        back_btn = Button(
            self.root,
            text="← Back",
            command=self.root.destroy,
            font=("Helvetica", 12, "bold"),
            bg="red",
            fg="white",
            relief=FLAT
        )
        back_btn.place(x=10, y=15)

        # ====================== Main Frame ======================
        main_frame = Frame(self.root, bg="white")
        main_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)

        # ====================== Left Frame (FAQ & Guides) ======================
        left_frame = LabelFrame(
            main_frame,
            text="FAQs & Troubleshooting",
            font=("Helvetica", 14, "bold"),
            bg="white",
            padx=10,
            pady=10
        )
        left_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=10)

        # FAQ Section
        faq_label = Label(
            left_frame,
            text="Frequently Asked Questions",
            font=("Helvetica", 14, "bold"),
            bg="white"
        )
        faq_label.pack(anchor=W, pady=5)

        # FAQ List
        faq_list = [
            "Q: How do I mark attendance using face recognition?",
            "A: Click on 'Face Recognition' and allow camera access.",
            "",
            "Q: Why is my attendance not being recorded?",
            "A: Ensure proper lighting and face alignment.",
            "",
            "Q: How do I export attendance data?",
            "A: Use the 'Export CSV' button in the Attendance tab.",
            "",
            "Q: Can I update attendance manually?",
            "A: Yes, select a record and click 'Update'."
        ]

        for item in faq_list:
            lbl = Label(
                left_frame,
                text=item,
                font=("Helvetica", 11),
                bg="white",
                anchor="w",
                justify=LEFT
            )
            lbl.pack(fill=X, padx=5, pady=2)

        # Troubleshooting Guide
        guide_label = Label(
            left_frame,
            text="Troubleshooting Guide",
            font=("Helvetica", 14, "bold"),
            bg="white"
        )
        guide_label.pack(anchor=W, pady=(15, 5))

        guide_text = """
        - Ensure the camera is properly connected.
        - Restart the application if face detection fails.
        - Update the software if issues persist.
        - Check database connection if data is not loading.
        """
        guide_lbl = Label(
            left_frame,
            text=guide_text,
            font=("Helvetica", 11),
            bg="white",
            justify=LEFT
        )
        guide_lbl.pack(fill=X, padx=5)

        # ====================== Right Frame (Contact Support) ======================
        right_frame = LabelFrame(
            main_frame,
            text="Contact Support",
            font=("Helvetica", 14, "bold"),
            bg="white",
            padx=10,
            pady=10
        )
        right_frame.pack(side=RIGHT, fill=BOTH, expand=True, padx=10)

        # Contact Form
        Label(right_frame, text="Name:", font=("Helvetica", 12), bg="white").pack(anchor=W, pady=5)
        self.name_entry = Entry(right_frame, font=("Helvetica", 12), width=30)
        self.name_entry.pack(fill=X, padx=5, pady=5)

        Label(right_frame, text="Email:", font=("Helvetica", 12), bg="white").pack(anchor=W, pady=5)
        self.email_entry = Entry(right_frame, font=("Helvetica", 12), width=30)
        self.email_entry.pack(fill=X, padx=5, pady=5)

        Label(right_frame, text="Issue Type:", font=("Helvetica", 12), bg="white").pack(anchor=W, pady=5)
        self.issue_type = ttk.Combobox(
            right_frame,
            values=["Technical Issue", "Feature Request", "General Inquiry"],
            font=("Helvetica", 12),
            state="readonly"
        )
        self.issue_type.pack(fill=X, padx=5, pady=5)

        Label(right_frame, text="Description:", font=("Helvetica", 12), bg="white").pack(anchor=W, pady=5)
        self.desc_text = Text(right_frame, height=5, font=("Helvetica", 12))
        self.desc_text.pack(fill=X, padx=5, pady=5)

        # Submit Button
        submit_btn = Button(
            right_frame,
            text="Submit Request",
            command=self.submit_request,
            font=("Helvetica", 12, "bold"),
            bg="green",
            fg="white"
        )
        submit_btn.pack(pady=10)

        # Live Chat Button (Simulated)
        chat_btn = Button(
            right_frame,
            text="💬 Start Live Chat",
            command=self.simulate_chat,
            font=("Helvetica", 12),
            bg="#3498db",
            fg="white"
        )
        chat_btn.pack(fill=X, padx=5, pady=5)

        # Support Links
        support_links = Frame(right_frame, bg="white")
        support_links.pack(fill=X, pady=10)

        Label(support_links, text="Quick Links:", font=("Helvetica", 12, "bold"), bg="white").pack(anchor=W)

        links = [
            ("📄 Documentation", "https://example.com/docs"),
            ("📧 Email Support", "mailto:support@example.com"),
            ("📞 Call Us", "tel:+1234567890")
        ]

        for text, url in links:
            btn = Button(
                support_links,
                text=text,
                command=lambda u=url: webbrowser.open(u),
                font=("Helvetica", 11),
                bg="white",
                fg="blue",
                relief=FLAT,
                cursor="hand2"
            )
            btn.pack(anchor=W, padx=5, pady=2)

    def submit_request(self):
        name = self.name_entry.get()
        email = self.email_entry.get()
        issue = self.issue_type.get()
        desc = self.desc_text.get("1.0", END).strip()

        if not name or not email or not issue or not desc:
            messagebox.showerror("Error", "All fields are required!")
        else:
            messagebox.showinfo(
                "Success",
                "Your request has been submitted!\nWe will contact you soon."
            )
            self.name_entry.delete(0, END)
            self.email_entry.delete(0, END)
            self.issue_type.set("")
            self.desc_text.delete("1.0", END)

    def simulate_chat(self):
        chat_window = Toplevel(self.root)
        chat_window.title("Live Chat Support")
        chat_window.geometry("400x500")
        chat_window.config(bg="#f0f0f0")

        chat_frame = Frame(chat_window, bg="#f0f0f0")
        chat_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        chat_log = Text(
            chat_frame,
            bg="white",
            font=("Helvetica", 12),
            state=DISABLED,
            wrap=WORD
        )
        chat_log.pack(fill=BOTH, expand=True)

        def send_message():
            user_msg = entry.get()
            if user_msg:
                chat_log.config(state=NORMAL)
                chat_log.insert(END, f"You: {user_msg}\n", "user")
                chat_log.insert(END, "Support Agent: Thank you for your message. We will respond shortly.\n", "agent")
                chat_log.config(state=DISABLED)
                entry.delete(0, END)
                chat_log.see(END)

        entry = Entry(chat_frame, font=("Helvetica", 12))
        entry.pack(fill=X, pady=5)
        entry.bind("<Return>", lambda e: send_message())

        send_btn = Button(
            chat_frame,
            text="Send",
            command=send_message,
            font=("Helvetica", 12),
            bg="#4CAF50",
            fg="white"
        )
        send_btn.pack(pady=5)

        # Tag configurations for chat bubbles
        chat_log.tag_config("user", foreground="blue")
        chat_log.tag_config("agent", foreground="green")

        # Initial bot message
        chat_log.config(state=NORMAL)
        chat_log.insert(END, "Support Agent: Hello! How can we help you today?\n", "agent")
        chat_log.config(state=DISABLED)

# ====================== Run the Help Desk ======================
if __name__ == "__main__":
    root = Tk()
    app = HelpDesk(root)
    root.mainloop()