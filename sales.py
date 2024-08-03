from tkinter import *
from tkinter import PhotoImage
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
import sys
# Ensure the database and tables are created
from create_db import create_db
create_db()

class SalesClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+220+130")
        self.root.title("Business Manager | Sales")
        icon = PhotoImage(file='D:/BM/Python Project/bm2.png')
        root.iconphoto(False, icon)
        self.root.config(bg="white")
        self.root.focus_force()
        self.root.resizable(False, False)

        # Variables
        self.var_sls_id = StringVar()
        self.var_prod_name = StringVar()
        self.var_qty_sold = StringVar()
        self.var_category = StringVar()
        self.var_date = StringVar()
        self.var_stock = StringVar()

        # Title 
        lbl_title = Label(self.root, text="Sales", font=("Bahnschrift", 25), bg="#0f4d7d", fg="white")
        lbl_title.pack(side=TOP, fill=X, padx=2, pady=2)

        # Clock
        self.lbl_clock = Label(self.root, text="", font=('Bahnschrift', 15), bg="#4d636d", fg="white")
        self.lbl_clock.place(x=2, y=48, height=25, width=1096)
        self.update_time()

        # Entries
        self.lbl_product = Label(self.root, text="Product Name", font=('Bahnschrift', 15), bg="white").place(x=50, y=100)
        self.txt_product = Entry(self.root, textvariable=self.var_prod_name, font=('Bahnschrift', 11), bg="lightyellow")
        self.txt_product.place(x=200, y=106)
        self.txt_product.bind("<KeyRelease>", self.autocomplete_product)

        self.product_listbox = Listbox(self.root)
        self.product_listbox.place(x=200, y=130)
        self.product_listbox.bind("<<ListboxSelect>>", self.fill_product_details)

        self.lbl_quantity = Label(self.root, text="Quantity Sold", font=('Bahnschrift', 15), bg="white").place(x=50, y=156)
        self.txt_quantity = Entry(self.root, textvariable=self.var_qty_sold, font=('Bahnschrift', 11), bg="lightyellow").place(x=200, y=156)

        self.lbl_cat = Label(self.root, text="Category", font=("Bahnschrift", 15), bg="white").place(x=600, y=100)
        self.txt_cat = Entry(self.root, textvariable=self.var_category, font=('Bahnschrift', 11), bg="lightyellow").place(x=700, y=106)

        self.lbl_date = Label(self.root, text="Date", font=("Bahnschrift", 15), bg="white").place(x=600, y=150)
        self.txt_date = Entry(self.root, textvariable=self.var_date, font=('Bahnschrift', 11), bg="lightyellow").place(x=700, y=156)

        self.lbl_stock = Label(self.root, text="Stock", font=("Bahnschrift", 15), bg="white").place(x=600, y=200)
        self.txt_stock = Entry(self.root, textvariable=self.var_stock, font=('Bahnschrift', 11), bg="lightyellow").place(x=700, y=206)

        btn_add = Button(self.root, text="Save", font=("Bahnschrift", 15), bg="#2196f3", fg="white", cursor="hand2", command=self.add_sales).place(x=50, y=215, width=110, height=28)
        btn_update = Button(self.root, text="Update", font=("Bahnschrift", 15), bg="#4caf50", fg="white", cursor="hand2", command=self.update_sales).place(x=170, y=215, width=110, height=28)
        btn_delete = Button(self.root, text="Delete", font=("Bahnschrift", 15), bg="#f44336", fg="white", cursor="hand2", command=self.delete_sales).place(x=290, y=215, width=110, height=28)
        btn_clear = Button(self.root, text="Clear", font=("Bahnschrift", 15), bg="#607d8b", fg="white", cursor="hand2", command=self.clear_entries).place(x=410, y=215, width=110, height=28)

        # Sales details
        sales_frame = Frame(self.root, bd=3, relief=RIDGE)
        sales_frame.place(x=0, y=250, relwidth=1, height=250)

        scrolly = Scrollbar(sales_frame, orient=VERTICAL)
        scrollx = Scrollbar(sales_frame, orient=HORIZONTAL)

        self.salesTable = ttk.Treeview(sales_frame, columns=("sid", "name", "category", "quantity", "date"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.salesTable.xview)
        scrolly.config(command=self.salesTable.yview)

        self.salesTable.heading('sid', text='S ID')
        self.salesTable.heading('name', text='Name')
        self.salesTable.heading('category', text='Category')
        self.salesTable.heading('quantity', text='Quantity')
        self.salesTable.heading('date', text='Date')
        self.salesTable["show"] = "headings"

        self.salesTable.column('sid', width=50)
        self.salesTable.column('name', width=100)
        self.salesTable.column('category', width=100)
        self.salesTable.column('quantity', width=100)
        self.salesTable.column('date', width=100)
        self.salesTable.pack(fill=BOTH, expand=1)
        self.salesTable.bind("<ButtonRelease-1>", self.get_sales_data)

        self.connect_db()
        self.show_sales()

    def connect_db(self):
        self.conn = sqlite3.connect('ims.db')
        self.cursor = self.conn.cursor()

    def update_time(self):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        current_date = now.strftime("%d-%m-%Y")
        self.lbl_clock.config(text=f"Sales\t\t Date: {current_date}\t\t Time: {current_time}")
        self.root.after(1000, self.update_time)

    def autocomplete_product(self, event):
        typed = self.var_prod_name.get()
        if typed == "":
            self.product_listbox.place_forget()
        else:
            self.product_listbox.place(x=200, y=130, width=200)
            self.cursor.execute("SELECT Name FROM product WHERE Name LIKE ?", ('%'+typed+'%',))
            products = self.cursor.fetchall()
            self.product_listbox.delete(0, END)
            for product in products:
                self.product_listbox.insert(END, product[0])

    def fill_product_details(self, event):
        selected_product = self.product_listbox.get(self.product_listbox.curselection())
        self.var_prod_name.set(selected_product)
        self.product_listbox.place_forget()
        self.cursor.execute("SELECT Category, Quantity FROM product WHERE Name=?", (selected_product,))
        product = self.cursor.fetchone()
        if product:
            self.var_category.set(product[0])
            self.var_stock.set(product[1])

    def add_sales(self):
        try:
            product_name = self.var_prod_name.get()
            quantity_sold = int(self.var_qty_sold.get())
            category = self.var_category.get()
            date = self.var_date.get()
            stock = int(self.var_stock.get())

            if product_name == "" or quantity_sold == "" or category == "" or date == "" or stock == "":
                messagebox.showerror("Error", "All fields are required")
            elif quantity_sold > stock:
                messagebox.showerror("Error", "Insufficient stock")
            else:
                new_stock = stock - quantity_sold
                self.cursor.execute("INSERT INTO sales (name, category, quantity, date) VALUES (?, ?, ?, ?)",
                                    (product_name, category, quantity_sold, date))
                self.cursor.execute("UPDATE product SET Quantity=? WHERE Name=?", (new_stock, product_name))
                self.conn.commit()
                self.show_sales()
                messagebox.showinfo("Success", "Sales record added successfully")
        except ValueError:
            messagebox.showerror("Error", "Invalid input for quantity or stock")

    def show_sales(self):
        self.cursor.execute("SELECT * FROM sales")
        rows = self.cursor.fetchall()
        self.salesTable.delete(*self.salesTable.get_children())
        for row in rows:
            self.salesTable.insert('', END, values=row)

    def get_sales_data(self, event):
        selected_row = self.salesTable.focus()
        data = self.salesTable.item(selected_row)
        row = data["values"]

        if row:  # Check if the row is not empty
            self.var_sls_id.set(row[0])
            self.var_prod_name.set(row[1])
            self.var_qty_sold.set(row[3])
            self.var_category.set(row[2])
            self.var_date.set(row[4])
            self.cursor.execute("SELECT Quantity FROM product WHERE Name=?", (row[1],))
            product = self.cursor.fetchone()
            if product:
                self.var_stock.set(product[0])
        else:
            self.clear_entries()


    def update_sales(self):
        try:
            sales_id = self.var_sls_id.get()
            product_name = self.var_prod_name.get()
            new_quantity_sold = int(self.var_qty_sold.get())
            category = self.var_category.get()
            date = self.var_date.get()
            current_stock = int(self.var_stock.get())

            if sales_id == "":
                messagebox.showerror("Error", "No sales record selected")
            elif product_name == "" or new_quantity_sold == "" or category == "" or date == "" or current_stock == "":
                messagebox.showerror("Error", "All fields are required")
            elif new_quantity_sold > current_stock:
                messagebox.showerror("Error", "Insufficient stock")
            else:
                # Get the previous quantity sold for this sales record
                self.cursor.execute("SELECT quantity FROM sales WHERE sid=?", (sales_id,))
                previous_quantity_sold = self.cursor.fetchone()[0]

                # Calculate the difference and adjust the stock accordingly
                quantity_difference = new_quantity_sold - previous_quantity_sold
                new_stock = current_stock - quantity_difference

                if new_stock < 0:
                    messagebox.showerror("Error", "Insufficient stock")
                    return

                self.cursor.execute("UPDATE sales SET name=?, category=?, quantity=?, date=? WHERE sid=?",
                                    (product_name, category, new_quantity_sold, date, sales_id))
                self.cursor.execute("UPDATE product SET Quantity=? WHERE Name=?", (new_stock, product_name))
                self.conn.commit()
                self.show_sales()
                messagebox.showinfo("Success", "Sales record updated successfully")
        except ValueError:
            messagebox.showerror("Error", "Invalid input for quantity or stock")

    def delete_sales(self):
        sales_id = self.var_sls_id.get()
        if sales_id == "":
            messagebox.showerror("Error", "No sales record selected")
        else:
            self.cursor.execute("DELETE FROM sales WHERE sid=?", (sales_id,))
            self.conn.commit()
            self.show_sales()
            messagebox.showinfo("Success", "Sales record deleted successfully")

    def clear_entries(self):
        self.var_sls_id.set("")
        self.var_prod_name.set("")
        self.var_qty_sold.set("")
        self.var_category.set("")
        self.var_date.set("")
        self.var_stock.set("")

if __name__ == "__main__":
    # Check if the script was called with the required argument
    if len(sys.argv) < 2 or sys.argv[1] != 'authorized':
        # Display an error message and exit
        print("Error: This script cannot be run directly. Access via dashboard.")
        sys.exit(1)
    
    root = Tk()
    obj = SalesClass(root)
    root.mainloop()
