from tkinter import *
from tkinter import PhotoImage
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
import sys

class employeeClass:
    def __init__(self, root, dashboard=None):
        self.root = root
        self.dashboard = dashboard  # Add a reference to the dashboard instance
        self.root.geometry("1100x500+220+130")
        self.root.title("Business Manager | Employee")
        icon = PhotoImage(file='D:/BM/Python Project/bm2.png')
        root.iconphoto(False, icon)
        self.root.config(bg="white")
        self.root.focus_force()
        self.root.resizable(False, False)
        
        # All variables
        self.var_searchby = StringVar()
        self.var_searchtxt = StringVar()
        self.var_emp_id = StringVar()
        self.var_gender = StringVar()
        self.var_name = StringVar()
        self.var_dob = StringVar()
        self.var_id = StringVar()
        self.var_email = StringVar()
        self.var_pass = StringVar()
        self.var_utype = StringVar()
        self.var_salary = StringVar()
        self.var_contact = StringVar()
        self.date = StringVar()
        self.time = StringVar()
        
        # Search Frame
        SearchFrame = LabelFrame(self.root, text="Search Employee", font=("Bahnschrift", 12, "bold"), bd=2, relief=RIDGE, bg="white")
        SearchFrame.place(x=250, y=10, width=600, height=70)
        
        # Options
        cmb_search = ttk.Combobox(SearchFrame, textvariable=self.var_searchby, values=('Select', "Email", "Name", "Employee", "Contact"), state='readonly', justify=CENTER, font=('Bahnschrift', 10))
        cmb_search.place(x=10, y=10, width=180)
        cmb_search.current(0)
        
        txt_search = Entry(SearchFrame, textvariable=self.var_searchtxt, font=("Bahnschrift", 11), bg="lightyellow").place(x=200, y=10, width=210)
        btn_search = Button(SearchFrame, command=self.search, text="Search", font=("Bahnschrift", 13), bg="#4caf50", fg="white", cursor="hand2").place(x=410, y=9, width=150, height=23)
        
        # Title
        title = Label(self.root, text="Employee Details", font=("Bahnschrift", 15), bg="#0f4d7d", fg="white").place(x=50, y=85, width=1000)
        
        # Clock
        self.lbl_clock = Label(self.root, text="", font=('Bahnschrift', 15), bg="#4d636d", fg="white")
        self.lbl_clock.place(x=50, y=115, height=25, width=1000)
        self.update_time()
        
        # Content
        lbl_empid = Label(self.root, text="Emp ID", font=("Bahnschrift", 15), bg="white").place(x=50, y=150)
        lbl_gender = Label(self.root, text="Gender", font=("Bahnschrift", 15), bg="white").place(x=350, y=150)
        lbl_contact = Label(self.root, text="Contact", font=("Bahnschrift", 15), bg="white").place(x=750, y=150)
        
        txt_empid = Entry(self.root, textvariable=self.var_emp_id, font=("Bahnschrift", 11), bg="lightyellow").place(x=150, y=150, width=180)
        cmb_gender = ttk.Combobox(self.root, textvariable=self.var_gender, values=('Select', "Male", "Female", "Other"), state='readonly', justify=CENTER, font=('Bahnschrift', 12))
        cmb_gender.place(x=500, y=150, width=180)
        cmb_gender.current(0)
        txt_contact = Entry(self.root, textvariable=self.var_contact, font=("Bahnschrift", 11), bg="lightyellow").place(x=850, y=150, width=180)
        
        lbl_name = Label(self.root, text="Name", font=("Bahnschrift", 15), bg="white").place(x=50, y=190)
        lbl_dob = Label(self.root, text="D.O.B", font=("Bahnschrift", 15), bg="white").place(x=350, y=190)
        lbl_id = Label(self.root, text="ID", font=("Bahnschrift", 15), bg="white").place(x=750, y=190)
        
        txt_name = Entry(self.root, textvariable=self.var_name, font=("Bahnschrift", 11), bg="lightyellow").place(x=150, y=190, width=180)
        txt_dob = Entry(self.root, textvariable=self.var_dob, font=("Bahnschrift", 11), bg="lightyellow").place(x=500, y=190, width=180)
        txt_id = Entry(self.root, textvariable=self.var_id, font=("Bahnschrift", 11), bg="lightyellow").place(x=850, y=190, width=180)
        
        lbl_email = Label(self.root, text="Email", font=("Bahnschrift", 15), bg="white").place(x=50, y=230)
        lbl_pass = Label(self.root, text="Password", font=("Bahnschrift", 15), bg="white").place(x=350, y=230)
        lbl_utype = Label(self.root, text="User Type", font=("Bahnschrift", 15), bg="white").place(x=750, y=230)
        
        txt_email = Entry(self.root, textvariable=self.var_email, font=("Bahnschrift", 11), bg="lightyellow").place(x=150, y=230, width=180)
        txt_pass = Entry(self.root, textvariable=self.var_pass, font=("Bahnschrift", 11), bg="lightyellow").place(x=500, y=230, width=180)
        cmb_utype = ttk.Combobox(self.root, textvariable=self.var_utype, values=('', 'Admin', "Employee"), state='readonly', justify=CENTER, font=('Bahnschrift', 10))
        cmb_utype.place(x=850, y=230, width=180)
        cmb_utype.current(0)
        
        lbl_address = Label(self.root, text="Address", font=("Bahnschrift", 15), bg="white").place(x=50, y=270)
        lbl_salary = Label(self.root, text="Salary", font=("Bahnschrift", 15), bg="white").place(x=500, y=270)
        
        self.txt_address = Text(self.root, font=("Bahnschrift", 13), bg="lightyellow")
        self.txt_address.place(x=150, y=270, width=300, height=60)
        txt_salary = Entry(self.root, textvariable=self.var_salary, font=("Bahnschrift", 11), bg="lightyellow").place(x=600, y=270, width=180)
        
        btn_add = Button(self.root, text="Save", command=self.add, font=("Bahnschrift", 15), bg="#2196f3", fg="white", cursor="hand2").place(x=500, y=305, width=110, height=28)
        btn_update = Button(self.root, text="Update", command=self.update, font=("Bahnschrift", 15), bg="#4caf50", fg="white", cursor="hand2").place(x=620, y=305, width=110, height=28)
        btn_delete = Button(self.root, text="Delete", command=self.delete, font=("Bahnschrift", 15), bg="#f44336", fg="white", cursor="hand2").place(x=740, y=305, width=110, height=28)
        btn_clear = Button(self.root, text="Clear", command=self.clear, font=("Bahnschrift", 15), bg="#607d8b", fg="white", cursor="hand2").place(x=860, y=305, width=110, height=28)
        
        emp_frame = Frame(self.root, bd=3, relief=RIDGE)
        emp_frame.place(x=0, y=350, relwidth=1, height=150)
        
        scrolly = Scrollbar(emp_frame, orient=VERTICAL)
        scrollx = Scrollbar(emp_frame, orient=HORIZONTAL)
        
        self.employeeTable = ttk.Treeview(emp_frame, columns=("eid", "name", "email", "gender", "contact", 'dob', 'id', 'pass', 'utype', 'address', 'salary'), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.employeeTable.xview)
        self.employeeTable.heading('eid', text="EID")
        self.employeeTable.heading('name', text="Name")
        self.employeeTable.heading('email', text="Email")
        self.employeeTable.heading('gender', text="Gender")
        self.employeeTable.heading('contact', text="Contact")
        self.employeeTable.heading('dob', text="D.O.B")
        self.employeeTable.heading('id', text="ID")
        self.employeeTable.heading('pass', text="Password")
        self.employeeTable.heading('utype', text="User Type")
        self.employeeTable.heading('address', text="Address")
        self.employeeTable.heading('salary', text="Salary")
        self.employeeTable['show'] = 'headings'
        self.employeeTable.column('eid', width=90)
        self.employeeTable.column('name', width=100)
        self.employeeTable.column('email', width=100)
        self.employeeTable.column('gender', width=100)
        self.employeeTable.column('contact', width=100)
        self.employeeTable.column('dob', width=100)
        self.employeeTable.column('id', width=100)
        self.employeeTable.column('pass', width=100)
        self.employeeTable.column('utype', width=100)
        self.employeeTable.column('address', width=100)
        self.employeeTable.column('salary', width=100)
        self.employeeTable.pack(fill=BOTH, expand=1)
        self.employeeTable.bind("<ButtonRelease-1>", self.get_data)
        
        self.show()
    
    def add(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_emp_id.get() == "":
                messagebox.showerror("Error", "Employee ID must be required", parent=self.root)
            else:
                cur.execute("SELECT * FROM employee WHERE eid=?", (self.var_emp_id.get(),))
                row = cur.fetchone()
                if row != None:
                    messagebox.showerror("Error", "This Employee ID already assigned, try different", parent=self.root)
                else:
                    cur.execute(
                        "INSERT INTO employee (eid, name, email, gender, contact, dob, id, pass, utype, address, salary) values(?,?,?,?,?,?,?,?,?,?,?)",
                        (
                            self.var_emp_id.get(),
                            self.var_name.get(),
                            self.var_email.get(),
                            self.var_gender.get(),
                            self.var_contact.get(),
                            self.var_dob.get(),
                            self.var_id.get(),
                            self.var_pass.get(),
                            self.var_utype.get(),
                            self.txt_address.get('1.0', END),
                            self.var_salary.get(),
                        ))
                    con.commit()
                    messagebox.showinfo("Success", "Employee Added Successfully", parent=self.root)
                    self.clear()
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def show(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM employee")
            rows = cur.fetchall()
            self.employeeTable.delete(*self.employeeTable.get_children())
            for row in rows:
                self.employeeTable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)
    
    def get_data(self, ev):
        f = self.employeeTable.focus()
        content = (self.employeeTable.item(f))
        row = content['values']
        self.var_emp_id.set(row[0])
        self.var_name.set(row[1])
        self.var_email.set(row[2])
        self.var_gender.set(row[3])
        self.var_contact.set(row[4])
        self.var_dob.set(row[5])
        self.var_id.set(row[6])
        self.var_pass.set(row[7])
        self.var_utype.set(row[8])
        self.txt_address.delete('1.0', END)
        self.txt_address.insert(END, row[9])
        self.var_salary.set(row[10])
    
    def update(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_emp_id.get() == "":
                messagebox.showerror("Error", "Employee ID must be required", parent=self.root)
            else:
                cur.execute("SELECT * FROM employee WHERE eid=?", (self.var_emp_id.get(),))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror("Error", "Invalid Employee ID", parent=self.root)
                else:
                    cur.execute(
                        "UPDATE employee SET name=?, email=?, gender=?, contact=?, dob=?, id=?, pass=?, utype=?, address=?, salary=? WHERE eid=?",
                        (
                            self.var_name.get(),
                            self.var_email.get(),
                            self.var_gender.get(),
                            self.var_contact.get(),
                            self.var_dob.get(),
                            self.var_id.get(),
                            self.var_pass.get(),
                            self.var_utype.get(),
                            self.txt_address.get('1.0', END),
                            self.var_salary.get(),
                            self.var_emp_id.get()
                        ))
                    con.commit()
                    messagebox.showinfo("Success", "Employee Updated Successfully", parent=self.root)
                    self.clear()
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)
    
    def delete(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_emp_id.get() == "":
                messagebox.showerror("Error", "Employee ID must be required", parent=self.root)
            else:
                cur.execute("SELECT * FROM employee WHERE eid=?", (self.var_emp_id.get(),))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror("Error", "Invalid Employee ID", parent=self.root)
                else:
                    if messagebox.askyesno("Confirm", "Do you really want to delete?", parent=self.root):
                        cur.execute("DELETE FROM employee WHERE eid=?", (self.var_emp_id.get(),))
                        con.commit()
                        messagebox.showinfo("Delete", "Employee Deleted Successfully", parent=self.root)
                        self.clear()
                        self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)
    
    def clear(self):
        self.var_emp_id.set("")
        self.var_gender.set("")
        self.var_name.set("")
        self.var_dob.set("")
        self.var_id.set("")
        self.var_email.set("")
        self.var_pass.set("")
        self.var_utype.set("")
        self.var_salary.set("")
        self.var_contact.set("")
        self.txt_address.delete('1.0', END)
        self.var_searchtxt.set("")
        self.var_searchby.set("Select")
        self.show()
    
    def search(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_searchby.get() == "Select":
                messagebox.showerror("Error", "Select Search By option", parent=self.root)
            elif self.var_searchtxt.get() == "":
                messagebox.showerror("Error", "Search input should be required", parent=self.root)
            else:
                cur.execute("SELECT * FROM employee WHERE " + self.var_searchby.get() + " LIKE '%" + self.var_searchtxt.get() + "%'")
                rows = cur.fetchall()
                if len(rows) != 0:
                    self.employeeTable.delete(*self.employeeTable.get_children())
                    for row in rows:
                        self.employeeTable.insert('', END, values=row)
                else:
                    messagebox.showerror("Error", "No record found!", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)
    
    def update_time(self):
        now = datetime.now()
        date_time = now.strftime("%d-%m-%Y | %H:%M:%S")
        self.lbl_clock.config(text=f"Welcome to Business Manager\t\t Date: {date_time.split('|')[0]}\t\t Time: {date_time.split('|')[1]}")
        self.lbl_clock.after(1000, self.update_time)

if __name__ == "__main__":
    # Check if the script was called with the required argument
    if len(sys.argv) < 2 or sys.argv[1] != 'authorized':
        # Display an error message and exit
        print("Error: This script cannot be run directly. Access via dashboard.")
        sys.exit(1)
    
    root = Tk()
    obj = employeeClass(root)
    root.mainloop()
