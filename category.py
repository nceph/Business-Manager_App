from tkinter import *
from tkinter import PhotoImage
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3
import sys
class categoryClass:
    def __init__(self, root, dashboard=None):
        self.root = root
        self.dashboard = dashboard  # Add a reference to the dashboard instance
        self.root.geometry("1100x500+220+130")
        self.root.title("Business Manager | Category")
        icon = PhotoImage(file='D:/BM/Python Project/bm2.png')
        root.iconphoto(False, icon)
        self.root.config(bg="white")
        self.root.focus_force()
        self.root.resizable(False, False)

        # Variables
        self.var_cat_id = StringVar()
        self.var_name = StringVar()

        # Title
        lbl_title = Label(self.root, text="Manage Product Category", font=("Bahnschrift", 30), bg="#184a45", fg="white", bd=3, relief=RIDGE)
        lbl_title.pack(side=TOP, fill=X, padx=10, pady=2)
        lbl_title = Label(self.root, text="Enter Category Name", font=("Bahnschrift", 30), bg="white")
        lbl_title.place(x=50, y=100)
        txt_name = Entry(self.root, textvariable=self.var_name, font=("Bahnschrift", 15), bg="lightyellow")
        txt_name.place(x=51, y=170, width=300)
        btn_add = Button(self.root, text="ADD", command=self.add, font=("Bahnschrift", 15), bg="#4caf50", fg="white", cursor='hand2')
        btn_add.place(x=360, y=170, width=150, height=28)
        btn_delete = Button(self.root, command=self.delete, text="DELETE", font=("Bahnschrift", 15), bg="red", fg="white", cursor='hand2')
        btn_delete.place(x=520, y=170, width=150, height=28)

        # Category Details
        cat_frame = Frame(self.root, bd=3, relief=RIDGE)
        cat_frame.place(x=700, y=100, width=380, height=350)

        scrolly = Scrollbar(cat_frame, orient=VERTICAL)
        scrollx = Scrollbar(cat_frame, orient=HORIZONTAL)

        self.category_table = ttk.Treeview(cat_frame, columns=("cid", "name"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.category_table.xview)
        scrolly.config(command=self.category_table.yview)

        self.category_table.heading("cid", text="C ID")
        self.category_table.heading("name", text="Name")
        self.category_table["show"] = "headings"
        self.category_table.column("cid", width=90)
        self.category_table.column("name", width=100)
        self.category_table.pack(fill=BOTH, expand=1)
        self.category_table.bind("<ButtonRelease-1>", self.get_data)

        # Images
        self.im1 = Image.open("D:/BM/Python Project/bm2.png")
        self.im1 = self.im1.resize((500, 250), Image.LANCZOS)
        self.im1 = ImageTk.PhotoImage(self.im1)
        self.lbl_im1 = Label(self.root, image=self.im1, bd=2, relief=RAISED)
        self.lbl_im1.place(x=50, y=220)

        self.show()

    # Functions
    def add(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_name.get() == "":
                messagebox.showerror("Error", "Category name should be required", parent=self.root)
            else:
                cur.execute("SELECT * FROM category WHERE name=?", (self.var_name.get(),))
                row = cur.fetchone()
                if row is not None:
                    messagebox.showerror("Error", "Category already present, try different", parent=self.root)
                else:
                    cur.execute("SELECT MIN(cid + 1) FROM category WHERE (cid + 1) NOT IN (SELECT cid FROM category)")
                    min_id = cur.fetchone()[0]
                    if min_id is None:
                        cur.execute("INSERT INTO category (name) VALUES(?)", (self.var_name.get(),))
                    else:
                        cur.execute("INSERT INTO category (cid, name) VALUES(?, ?)", (min_id, self.var_name.get()))
                    con.commit()
                    messagebox.showinfo("Success", "Category added successfully", parent=self.root)
                    self.show()
                    if self.dashboard:
                        self.dashboard.update_category_count()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def show(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM category")
            rows = cur.fetchall()
            self.category_table.delete(*self.category_table.get_children())
            for row in rows:
                self.category_table.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def get_data(self, ev):
        f = self.category_table.focus()
        content = (self.category_table.item(f))
        row = content['values']
        self.var_cat_id.set(row[0])
        self.var_name.set(row[1])

    def delete(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_cat_id.get() == "":
                messagebox.showerror("Error", "Please select category from the list", parent=self.root)
            else:
                cur.execute("SELECT * FROM category WHERE cid=?", (self.var_cat_id.get(),))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Invalid Category", parent=self.root)
                else:
                    op = messagebox.askyesno("Confirm", "Do you really want to delete?", parent=self.root)
                    if op is True:
                        cur.execute("DELETE FROM category WHERE cid=?", (self.var_cat_id.get(),))
                        con.commit()
                        messagebox.showinfo("Delete", "Category deleted Successfully", parent=self.root)
                        self.show()
                        if self.dashboard:
                            self.dashboard.update_category_count()
                        self.var_cat_id.set("")
                        self.var_name.set("")
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

if __name__ == "__main__":
    # Check if the script was called with the required argument
    if len(sys.argv) < 2 or sys.argv[1] != 'authorized':
        # Display an error message and exit
        print("Error: This script cannot be run directly. Access via dashboard.")
        sys.exit(1)
    
    root = Tk()
    obj = categoryClass(root)
    root.mainloop()
