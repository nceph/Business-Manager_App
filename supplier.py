from tkinter import *
from tkinter import PhotoImage
import sys

class supplierclass:
    def __init__(self,root):
        self.root = root
        self.root.geometry("1100x500+220+130")
        self.root.title("Business Manager | Supplier")
        icon = PhotoImage(file='D:/BM/Python Project/bm2.png')
        root.iconphoto(False,icon)
        self.root.config(bg="white")
        self.root.focus_force()
        self.root.resizable(False, False)
        
        label = Label(root,text="PAGE STILL IN CONSTRUCTION YOU CAN STILL INTERACT WITH THE OTHER PAGES",font=('Arial',18,"bold"))
        label.place(x=40,y=200)



if __name__ == "__main__":
    # Check if the script was called with the required argument
    if len(sys.argv) < 2 or sys.argv[1] != 'authorized':
        # Display an error message and exit
        print("Error: This script cannot be run directly. Access via dashboard.")
        sys.exit(1)
    
    root = Tk()
    obj = supplierclass(root)
    root.mainloop()