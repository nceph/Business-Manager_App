from tkinter import *
from tkinter import PhotoImage
from tkinter import messagebox
import sqlite3
import os
import subprocess

class Login:
    def __init__(self, root):
        self.root = root
        self.root.geometry("800x500+280+100")
        self.root.title("Business Manager | Promise Electronic Shop")
        icon = PhotoImage(file='D:/BM/Python Project/bm2.png')
        root.iconphoto(False, icon)
        self.root.config(bg="white")
        self.root.focus_force()
        self.root.resizable(False, False)
        
        # Variables
        self.var_username = StringVar()
        self.var_password = StringVar()

        # Login Frame
        Frame_login = Frame(self.root, bg="white", relief=RIDGE, border=2)
        Frame_login.place(x=150, y=50, width=500, height=400)

        # Title
        title = Label(Frame_login, text='Login', font=("Bahnschrift", 20, "bold")).place(x=210, y=20)
        subtitle = Label(Frame_login, text='Members Login Area', font=("Bahnschrift", 18, "bold")).place(x=130, y=60)

        # Username
        lbl_user = Label(Frame_login, text="Username", font=("Bahnschrift", 15)).place(x=90, y=100)
        self.username = Entry(Frame_login, textvariable=self.var_username, font=('Bahnschrift', 11), bg="lightgrey", border=0).place(x=90, y=130, width=200)

        lbl_pass = Label(Frame_login, text="Password", font=("Bahnschrift", 15)).place(x=90, y=160)
        self.password = Entry(Frame_login, textvariable=self.var_password, font=('Bahnschrift', 11), bg="lightgrey", border=0, show="*").place(x=90, y=190, width=200)

        # Login Button with Database Connection
        btn_login = Button(Frame_login, text="Login", font=('Bahnschrift', 15, 'bold'), bg='lightblue', cursor="hand2", command=self.login).place(x=90, y=230, height=50, width=150)

    def login(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_username.get() == "" or self.var_password.get() == "":
                messagebox.showerror("Error", "All fields are required", parent=self.root)
            else:
                cur.execute('SELECT * FROM users WHERE username=? AND password=?', (self.var_username.get(), self.var_password.get()))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Invalid Username or Password", parent=self.root)
                else:
                    messagebox.showinfo("Success", "Login Successful", parent=self.root)
                    self.root.destroy()
                    os.chdir('D:/BM/Python Project')  # Change directory to where dashboard.py is located
                    subprocess.Popen(["python", "dashboard.py", "authorized"])
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)
        finally:
            con.close()

if __name__ == "__main__":
    root = Tk()
    obj = Login(root)
    root.mainloop()
