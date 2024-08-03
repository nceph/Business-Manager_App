from tkinter import *
from tkinter import PhotoImage
from PIL import Image, ImageTk
from employee import employeeClass
from supplier import supplierclass
from category import categoryClass
from product import productClass
from sales import SalesClass
from datetime import datetime
from stock import stockClass
import sqlite3
from tkinter import ttk, messagebox
import sys
import subprocess

class Dashboard:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1350x700+0+0")
        self.root.title("Business Manager | Promise Electronic Shop")
        icon = PhotoImage(file='D:/BM/Python Project/bm2.png')
        root.iconphoto(False, icon)
        root.state('zoomed')
        self.root.config(bg="white")
        
        # Main Frame
        main_frame = Frame(self.root, bg="white")
        main_frame.pack(fill=BOTH, expand=1)

        # Navigation bar
        self.icon_title = PhotoImage(file="D:/BM/Python Project/inventory.png")
        title = Label(self.root, text="Promise Electronic Shop", image=self.icon_title, compound=LEFT, font=('Bahnschrift', 40, "bold"), bg="#010c48", fg="white", anchor="w", padx=20).place(x=0, y=0, relwidth=1, height=70)
        
        # Logout button
        btn_logout = Button(self.root, text="Logout", font=('Bahnschrift', 15, 'bold'), bg='yellow', cursor="hand2").place(x=1150, y=10, height=50, width=150)
        
        # Clock
        self.lbl_clock = Label(self.root, text="", font=('Bahnschrift', 15), bg="#4d636d", fg="white")
        self.lbl_clock.place(x=0, y=70, relwidth=1, height=30)
        self.update_time()
        
        # Left Menu
        self.MenuLogo = Image.open("D:/BM/Python Project/menu.png")
        self.MenuLogo = self.MenuLogo.resize((200, 200), Image.LANCZOS)
        self.MenuLogo = ImageTk.PhotoImage(self.MenuLogo)
        
        LeftMenu = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        LeftMenu.place(x=0, y=102, width=200, height=565)
        
        lbl_menulogo = Label(LeftMenu, image=self.MenuLogo)
        lbl_menulogo.pack(side=TOP, fill=X)
        
        self.icon_side = PhotoImage(file="D:/BM/Python Project/frsh.png")
        lbl_menu = Label(LeftMenu, text='Menu', font=('Bahnschrift', 20), bg="#009688").pack(side=TOP, fill=X)
        btn_employee=Button(LeftMenu, text="Employee",command=self.open_employee_window,image=self.icon_side,compound=LEFT,padx=5,anchor="w",font=("Bahnschrift",19,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_supplier=Button(LeftMenu,text="Supplier",command=self.open_supplier_window,image=self.icon_side,compound=LEFT,padx=5,anchor="w",font=("Bahnschrift",19,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_category=Button(LeftMenu,text="Category",command=self.open_category_window,image=self.icon_side,compound=LEFT,padx=5,anchor="w",font=("Bahnschrift",19,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_product=Button(LeftMenu,text="Products",command=self.open_product_window,image=self.icon_side,compound=LEFT,padx=5,anchor="w",font=("Bahnschrift",18,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_sales=Button(LeftMenu,text="Sales",command=self.open_sales_window,image=self.icon_side,compound=LEFT,padx=5,anchor="w",font=("Bahnschrift",19,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_stock=Button(LeftMenu,text="Stock",command=self.open_stock_window,image=self.icon_side,compound=LEFT,padx=5,anchor="w",font=("Bahnschrift",19,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        
        # Content
        self.lbl_employee = Label(self.root, text="Total Employee\n[ 0 ]", bd=5, relief=RIDGE, bg="#33bbf9", fg="white", font=("Bahnschrift", 20, "bold"))
        self.lbl_employee.place(x=300, y=120, height=150, width=300)
        self.update_employee_count()
        
        self.lbl_supplier = Label(self.root, text="Total Suppliers\n[ 0 ]", bd=5, relief=RIDGE, bg="#33bbf9", fg="white", font=("Bahnschrift", 20, "bold"))
        self.lbl_supplier.place(x=650, y=120, height=150, width=300)
        
        self.lbl_category = Label(main_frame, text="Total Category\n[ 0 ]", bd=5, relief=RIDGE, bg="#33bbf9", fg="white", font=("Bahnschrift", 20, "bold"))
        self.lbl_category.place(x=1000, y=120, height=150, width=300)
        self.update_category_count()
        
        self.lbl_product = Label(self.root, text="Total Product\n[ 0 ]", bd=5, relief=RIDGE, bg="#33bbf9", fg="white", font=("Bahnschrift", 20, "bold"))
        self.lbl_product.place(x=300, y=300, height=150, width=300)
        self.update_product_count()
        
        self.lbl_sales = Label(self.root, text="Total Sales\n[ 0 ]", bd=5, relief=RIDGE, bg="#33bbf9", fg="white", font=("Bahnschrift", 20, "bold"))
        self.lbl_sales.place(x=650, y=300, height=150, width=300)
        
        # Footer
        lbl_footer = Label(self.root, text="IMS - Inventory Management System | Developed by Nshutinziza Cephas\nFor any Technical Issue Contact: +250 786 077 158", font=('Bahnschrift', 11), bg="#4d636d", fg="white").pack(side=BOTTOM, fill=X)
        
        # Flag to track employee window
        self.employee_window = None
        self.supplier_window = None
        self.category_window = None
        self.product_window = None
        self.sales_window = None
        self.stock_window = None
        
         # Bind minimize and restore events
        self.root.bind("<Unmap>", self.minimize_all)
        self.root.bind("<Map>", self.restore_all)

    def open_employee_window(self):
        if self.employee_window is None or not self.employee_window.winfo_exists():
            self.employee_window = Toplevel(self.root)
            employeeClass(self.employee_window)
          
    def open_supplier_window(self):
        if self.supplier_window is None or not self.supplier_window.winfo_exists():
            self.supplier_window = Toplevel(self.root)
            supplierclass(self.supplier_window) 
         
    def open_category_window(self):
        if self.category_window is None or not self.category_window.winfo_exists():
            self.category_window = Toplevel(self.root)
            categoryClass(self.category_window)  
            
    def open_product_window(self):
        if self.product_window is None or not self.product_window.winfo_exists():
            self.product_window = Toplevel(self.root)
            productClass(self.product_window)  
    
    def open_sales_window(self):
        if self.sales_window is None or not self.sales_window.winfo_exists():
            self.sales_window = Toplevel(self.root)
            SalesClass(self.sales_window)   
    
    def open_stock_window(self):
        if self.stock_window is None or not self.stock_window.winfo_exists():
            self.stock_window = Toplevel(self.root)
            stockClass(self.stock_window)       
                                     
            
    def minimize_all(self, event):
        if self.employee_window is not None and self.employee_window.winfo_exists():
            self.employee_window.withdraw()

    def restore_all(self, event):
        if self.employee_window is not None and self.employee_window.winfo_exists():
            self.employee_window.deiconify()           
        
    def update_time(self):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        current_date = now.strftime("%d-%m-%Y")
        self.lbl_clock.config(text=f"Welcome to Inventory Management System\t\t Date: {current_date}\t\t Time: {current_time}")
        
        # Call this method again after 1000ms (1 second)
        self.root.after(1000, self.update_time)
        
    def update_category_count(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT COUNT(*) FROM category")
            count = cur.fetchone()[0]
            self.lbl_category.config(text=f"Total Category\n[ {count} ]")
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()
            
    def update_product_count(self):
        con = sqlite3.connect(database=r'ims.db')      
        cur = con.cursor()
        try:
            cur.execute("SELECT COUNT(*) FROM product")
            count = cur.fetchone()[0]
            self.lbl_product.config(text=f"Total Product\n[ {count} ]")  
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()
    
    def update_employee_count(self):
        con = sqlite3.connect(database=r'ims.db')      
        cur = con.cursor()
        try:
            cur.execute("SELECT COUNT(*) FROM employee")
            count = cur.fetchone()[0]
            self.lbl_employee.config(text=f"Total Employee\n[ {count} ]")  
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()        
    def open_employee(self):
        # Execute the employee.py script with the 'authorized' argument
        subprocess.Popen(['python', 'employee.py', 'authorized'])
                  
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "authorized":
        root = Tk()
        obj = Dashboard(root)
        root.mainloop()
    else:
        messagebox.showerror("Error", "Unauthorized Access")
