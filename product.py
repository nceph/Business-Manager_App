from tkinter import *
from tkinter import PhotoImage
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3

class AutocompleteCombobox(ttk.Combobox):
    def set_completion_list(self, completion_list):
        self._completion_list = sorted(completion_list)
        self._hits = []
        self._hit_index = 0
        self.position = 0
        self.bind('<KeyRelease>', self.handle_keyrelease)
        self['values'] = self._completion_list

    def autocomplete(self, delta=0):
        if delta:
            self.delete(self.position, END)
        else:
            self.position = len(self.get())

        _hits = []
        for item in self._completion_list:
            if item.lower().startswith(self.get().lower()):
                _hits.append(item)

        if _hits != self._hits:
            self._hit_index = 0
            self._hits = _hits

        if _hits:
            self._hit_index = (self._hit_index + delta) % len(_hits)
            self.delete(0, END)
            self.insert(0, _hits[self._hit_index])
            self.select_range(self.position, END)

    def handle_keyrelease(self, event):
        if event.keysym in ('BackSpace', 'Left', 'Right', 'Up', 'Down'):
            return
        self.autocomplete()

class productClass:
    def __init__(self, root,dashboard=None):
        self.root = root
        self.dashboard = dashboard  # Add a reference to the dashboard instance
        self.root.geometry("1100x500+220+130")
        self.root.title("Business manager | Product")
        icon = PhotoImage(file='D:/BM/Python Project/bm2.png')
        root.iconphoto(False, icon)
        self.root.config(bg="white")
        self.root.focus_force()
        self.root.resizable(False, False)

        self.var_searchby = StringVar()
        self.var_searchtxt = StringVar()
        self.var_pid = StringVar()
        self.var_cat = StringVar()
        self.var_sup = StringVar()
        self.cat_list = []
        self.sup_list = []
        self.fetch_cat_sup()
        self.var_name = StringVar()
        self.var_price = StringVar()
        self.var_qty = StringVar()
        self.var_status = StringVar()

        # Frame
        product_Frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        product_Frame.place(x=10, y=10, width=450, height=480)

        # Title
        title = Label(product_Frame, text="Product Details", font=("Bahnschrift", 15), bg="#0f4d7d", fg="white").pack(side=TOP, fill=X)

        # Column 1
        lbl_category = Label(product_Frame, text="Category ", font=('Bahnschrift', 15), bg="white").place(x=10, y=60)
        lbl_supplier = Label(product_Frame, text="Supplier ", font=('Bahnschrift', 15), bg="white").place(x=10, y=110)
        lbl_product_name = Label(product_Frame, text="Name", font=('Bahnschrift', 15), bg="white").place(x=10, y=160)
        lbl_price = Label(product_Frame, text="Price", font=('Bahnschrift', 15), bg="white").place(x=10, y=210)
        lbl_quantity = Label(product_Frame, text="Quantity", font=('Bahnschrift', 15), bg="white").place(x=10, y=260)
        lbl_status = Label(product_Frame, text="Status", font=('Bahnschrift', 15), bg="white").place(x=10, y=310)

        # Column 2
        cmb_cat = AutocompleteCombobox(product_Frame, textvariable=self.var_cat, font=('Bahnschrift', 10))
        cmb_cat.set_completion_list(self.cat_list)
        cmb_cat.place(x=150, y=65, width=200)
        
        cmb_sup = ttk.Combobox(product_Frame, textvariable=self.var_sup, values=self.sup_list, state='readonly', justify=CENTER, font=('Bahnschrift', 10))
        cmb_sup.place(x=150, y=115, width=200)
        cmb_sup.current(0)

        txt_name = Entry(product_Frame, textvariable=self.var_name, font=('Bahnschrift', 10), bg='lightyellow')
        txt_name.place(x=150, y=165, width=200)
        txt_price = Entry(product_Frame, textvariable=self.var_price, font=('Bahnschrift', 10), bg='lightyellow')
        txt_price.place(x=150, y=215, width=200)
        txt_qty = Entry(product_Frame, textvariable=self.var_qty, font=('Bahnschrift', 10), bg='lightyellow')
        txt_qty.place(x=150, y=265, width=200)

        cmb_status = ttk.Combobox(product_Frame, textvariable=self.var_status, values=('', 'Active', 'Inactive'), state='readonly', justify=CENTER, font=('Bahnschrift', 10))
        cmb_status.place(x=150, y=315, width=200)
        cmb_status.current(0)

        # Buttons
        btn_add = Button(product_Frame, text="Save", command=self.add, font=("Bahnschrift", 15), bg="#2196f3", fg="white", cursor="hand2").place(x=10, y=400, width=100, height=28)
        btn_update = Button(product_Frame, text="Update", command=self.update, font=("Bahnschrift", 15), bg="#4caf50", fg="white", cursor="hand2").place(x=120, y=400, width=100, height=28)
        btn_delete = Button(product_Frame, text="Delete", command=self.delete, font=("Bahnschrift", 15), bg="#f44336", fg="white", cursor="hand2").place(x=230, y=400, width=100, height=28)
        btn_clear = Button(product_Frame, text="Clear", command=self.clear, font=("Bahnschrift", 15), bg="#607d8b", fg="white", cursor="hand2").place(x=340, y=400, width=100, height=28)

        # Search Frame
        SearchFrame = LabelFrame(self.root, text="Search Product", font=("Bahnschrift", 12, "bold"), bd=2, relief=RIDGE, bg="white")
        SearchFrame.place(x=480, y=10, width=600, height=80)

        # Search Options
        cmb_search = ttk.Combobox(SearchFrame, textvariable=self.var_searchby, values=('Select', "Category", "Supplier", "Name"), state='readonly', justify=CENTER, font=('Bahnschrift', 10))
        cmb_search.place(x=10, y=10, width=180)
        cmb_search.current(0)

        txt_search = Entry(SearchFrame, textvariable=self.var_searchtxt, font=("Bahnschrift", 11), bg="lightyellow").place(x=200, y=10, width=210)
        btn_search = Button(SearchFrame, command=self.search, text="Search", font=("Bahnschrift", 13), bg="#4caf50", fg="white", cursor="hand2").place(x=410, y=9, width=150, height=23)

        # Product details
        p_frame = Frame(self.root, bd=3, relief=RIDGE)
        p_frame.place(x=480, y=100, width=600, height=390)

        scrolly = Scrollbar(p_frame, orient=VERTICAL)
        scrollx = Scrollbar(p_frame, orient=HORIZONTAL)

        self.product_table = ttk.Treeview(p_frame, columns=("pid", "Supplier", "Category", "Name", "Price", 'Quantity', 'Status'), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.product_table.xview)
        scrolly.config(command=self.product_table.yview)

        self.product_table.heading('pid', text='P ID')
        self.product_table.heading('Category', text='Category')
        self.product_table.heading('Supplier', text='Supplier')
        self.product_table.heading('Name', text='Name')
        self.product_table.heading('Price', text='Price')
        self.product_table.heading('Quantity', text='Quantity')
        self.product_table.heading('Status', text='Status')

        self.product_table["show"] = "headings"

        self.product_table.column('pid', width=90)
        self.product_table.column('Category', width=100)
        self.product_table.column('Supplier', width=100)
        self.product_table.column('Name', width=100)
        self.product_table.column('Price', width=100)
        self.product_table.column('Quantity', width=100)
        self.product_table.column('Status', width=100)
        self.product_table.pack(fill=BOTH, expand=1)
        self.product_table.bind("<ButtonRelease-1>", self.get_data)

        self.show()

    def fetch_cat_sup(self):
        self.cat_list.append("Empty")
        self.sup_list.append("Empty")
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            cur.execute("Select name from category")
            cat = cur.fetchall()
            if len(cat) > 0:
                del self.cat_list[:]
                self.cat_list.append("Select")
                for i in cat:
                    self.cat_list.append(i[0])
            cur.execute("Select name from supplier")
            sup = cur.fetchall()
            if len(sup) > 0:
                del self.sup_list[:]
                self.sup_list.append("Select")
                for i in sup:
                    self.sup_list.append(i[0])
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def add(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_cat.get() == "Select" or self.var_cat.get() == "Empty" or self.var_sup.get() == "Select" or self.var_name.get() == "":
                messagebox.showerror("Error", "All fields are required", parent=self.root)
            else:
                cur.execute("Select * from product where name=?", (self.var_name.get(),))
                row = cur.fetchone()
                if row is not None:
                    messagebox.showerror("Error", "Product already present, try different", parent=self.root)
                else:
                    cur.execute("Insert into product(Category, Supplier, Name, Price, Quantity, Status)values(?,?,?,?,?,?)", (
                        self.var_cat.get(),
                        self.var_sup.get(),
                        self.var_name.get(),
                        self.var_price.get(),
                        self.var_qty.get(),
                        self.var_status.get(),
                    ))

                    con.commit()
                    messagebox.showinfo("Success", "Product Added Successfully", parent=self.root)
                    self.show()
                    if self.dashboard:
                        self.dashboard.update_product_count()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def get_data(self, ev):
        f = self.product_table.focus()
        content = (self.product_table.item(f))
        row = content['values']
        
        if row:
            self.var_pid.set(row[0])
            self.var_cat.set(row[2])
            self.var_sup.set(row[1])
            self.var_name.set(row[3])
            self.var_price.set(row[4])
            self.var_qty.set(row[5])
            self.var_status.set(row[6])
        else:
            self.clear()


    def update(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_pid.get() == "":
                messagebox.showerror("Error", "Please select a product from the list", parent=self.root)
            else:
                cur.execute("Select * from product where pid=?", (self.var_pid.get(),))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Invalid Product ID", parent=self.root)
                else:
                    cur.execute("Update product set Category=?, Supplier=?, Name=?, Price=?, Quantity=?, Status=? where pid=?", (
                        self.var_cat.get(),
                        self.var_sup.get(),
                        self.var_name.get(),
                        self.var_price.get(),
                        self.var_qty.get(),
                        self.var_status.get(),
                        self.var_pid.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("Success", "Product Updated Successfully", parent=self.root)
                    self.show()
                    con.close()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def show(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            cur.execute("select * from product")
            rows = cur.fetchall()
            self.product_table.delete(*self.product_table.get_children())
            for row in rows:
                self.product_table.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def delete(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_name.get() == "":
                messagebox.showerror("Error", "Product Name must be required", parent=self.root)
            else:
                cur.execute("SELECT * FROM product WHERE name=?", (self.var_name.get(),))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Invalid Product Name", parent=self.root)
                else:
                    op = messagebox.askyesno("Confirm", "Do you really want to delete", parent=self.root)
                    if op:
                        cur.execute("DELETE FROM product WHERE name=?", (self.var_name.get(),))
                        con.commit()
                        messagebox.showinfo("Delete", "Product Deleted Successfully", parent=self.root)
                        self.clear()
                        if self.dashboard:
                            self.dashboard.update_product_count()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)
        finally:
            con.close()

    def clear(self):
        self.var_cat.set("Select")
        self.var_sup.set("Empty")
        self.var_name.set("")
        self.var_price.set("")
        self.var_qty.set("")
        self.var_status.set("")
        self.var_pid.set("")
        self.var_searchtxt.set("")
        self.var_searchby.set("Select")
        self.show()

    def search(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_searchby.get() == "Select":
                messagebox.showerror("Error", "Select Search By Option", parent=self.root)
            elif self.var_searchtxt.get() == "":
                messagebox.showerror("Error", "Search Input should be required", parent=self.root)
            else:
                query = f"SELECT * FROM product WHERE {self.var_searchby.get()} LIKE ?"
                cur.execute(query, ('%' + self.var_searchtxt.get() + '%',))
                rows = cur.fetchall()
                if len(rows) != 0:
                    self.product_table.delete(*self.product_table.get_children())
                    for row in rows:
                        self.product_table.insert('', END, values=row)
                else:
                    messagebox.showerror("Error", "No record found!!!", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)
        finally:
            con.close()

if __name__ == "__main__":
    root = Tk()
    obj = productClass(root)
    root.mainloop()
