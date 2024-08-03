from tkinter import *
from tkinter import PhotoImage
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
import sys

class stockClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+220+130")
        self.root.title("Business Manager | Stock")
        icon = PhotoImage(file='D:/BM/Python Project/bm2.png')
        root.iconphoto(False, icon)
        self.root.config(bg="white")
        self.root.focus_force()
        self.root.resizable(False, False)

        # Variables
        self.var_searchby = StringVar()
        self.var_searchtxt = StringVar()
        self.var_pid = StringVar()
        self.var_name = StringVar()
        self.var_category = StringVar()
        self.var_stock = StringVar()

        # Title
        lbl_title = Label(self.root, text="Stock", font=("Bahnschrift", 25), bg="#0f4d7d", fg="white")
        lbl_title.pack(side=TOP, fill=X, padx=2, pady=2)

        # Clock
        self.lbl_clock = Label(self.root, text="", font=('Bahnschrift', 15), bg="#4d636d", fg="white")
        self.lbl_clock.place(x=2, y=48, height=25, width=1096)
        self.update_time()

        # Search Frame
        SearchFrame = LabelFrame(self.root, text="Search Product", font=("Bahnschrift", 12, "bold"), bd=2, relief=RIDGE, bg="white")
        SearchFrame.place(x=250, y=75, width=600, height=70)

        # Options
        cmb_search = ttk.Combobox(SearchFrame, textvariable=self.var_searchby, values=('Select', "Category", "Name"), state='readonly', justify=CENTER, font=('Bahnschrift', 10))
        cmb_search.place(x=10, y=10, width=180)
        cmb_search.current(0)
        txt_search = Entry(SearchFrame, textvariable=self.var_searchtxt, font=("Bahnschrift", 11), bg="lightyellow").place(x=200, y=10, width=210)
        btn_search = Button(SearchFrame, text="Search", command=self.search, font=("Bahnschrift", 13), bg="#4caf50", fg="white", cursor="hand2").place(x=410, y=9, width=150, height=23)

        # Stock details
        stock_frame = Frame(self.root, bd=3, relief=RIDGE)
        stock_frame.place(x=0, y=150, relwidth=1, height=350)

        scrolly = Scrollbar(stock_frame, orient=VERTICAL)
        scrollx = Scrollbar(stock_frame, orient=HORIZONTAL)

        self.stockTable = ttk.Treeview(stock_frame, columns=("pid", "name", "category", "stock"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.stockTable.xview)
        scrolly.config(command=self.stockTable.yview)
        self.stockTable.heading('pid', text='P ID')
        self.stockTable.heading('name', text='Name')
        self.stockTable.heading('category', text='Category')
        self.stockTable.heading('stock', text='Stock')
        self.stockTable["show"] = "headings"

        self.stockTable.column('pid', width=90)
        self.stockTable.column('name', width=100)
        self.stockTable.column('category', width=100)
        self.stockTable.column('stock', width=100)
        self.stockTable.pack(fill=BOTH, expand=1)
        self.stockTable.bind("<ButtonRelease-1>", self.get_data)

        self.show()

    def update_time(self):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        current_date = now.strftime("%d-%m-%Y")
        self.lbl_clock.config(text=f"Stock\t\t Date: {current_date}\t\t Time: {current_time}")
        self.root.after(1000, self.update_time)

    def fetch_products(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT pid, name, category, quantity FROM product")
            rows = cur.fetchall()
            self.stockTable.delete(*self.stockTable.get_children())
            for row in rows:
                self.stockTable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)
        finally:
            con.close()

    def search(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_searchby.get() == "Select":
                messagebox.showerror("Error", "Select Search By Option", parent=self.root)
            elif self.var_searchtxt.get() == "":
                messagebox.showerror("Error", "Search Input should be required", parent=self.root)
            else:
                query = f"SELECT pid, name, category, quantity FROM product WHERE {self.var_searchby.get()} LIKE ?"
                cur.execute(query, ('%' + self.var_searchtxt.get() + '%',))
                rows = cur.fetchall()
                if rows:
                    self.stockTable.delete(*self.stockTable.get_children())
                    for row in rows:
                        self.stockTable.insert('', END, values=row)
                else:
                    messagebox.showerror("Error", "No record found!!!", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)
        finally:
            con.close()

    def get_data(self, ev):
        f = self.stockTable.focus()
        content = self.stockTable.item(f)
        row = content['values']
        self.var_pid.set(row[0])
        self.var_name.set(row[1])
        self.var_category.set(row[2])
        self.var_stock.set(row[3])

    def show(self):
        self.fetch_products()

if __name__ == "__main__":
    # Check if the script was called with the required argument
    if len(sys.argv) < 2 or sys.argv[1] != 'authorized':
        # Display an error message and exit
        print("Error: This script cannot be run directly. Access via dashboard.")
        sys.exit(1)
    
    root = Tk()
    obj = stockClass(root)
    root.mainloop()
