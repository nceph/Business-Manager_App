import sqlite3
def create_db():
    con=sqlite3.connect(database=r'ims.db')
    cur=con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS employee(eid INTEGER PRIMARY KEY AUTOINCREMENT,name text,email text,gender text,contact text,dob text,id text,pass text,utype text,address text,salary text)")
    con.commit()
    
    cur.execute("CREATE TABLE IF NOT EXISTS supplier(invoice INTEGER PRIMARY KEY AUTOINCREMENT,name text,contact text,desc text)")
    con.commit()

    cur.execute("CREATE TABLE IF NOT EXISTS category(cid INTEGER PRIMARY KEY AUTOINCREMENT,name text)")
    con.commit()

    cur.execute("CREATE TABLE IF NOT EXISTS product(pid INTEGER PRIMARY KEY AUTOINCREMENT,Supplier text,Category text,Name text,Price text,Quantity text,Status text)")
    con.commit()
    
    cur.execute("""CREATE TABLE IF NOT EXISTS sales(sid INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT,category TEXT,quantity INTEGER,date TEXT)""")
    con.commit()
    
    cur.execute("CREATE TABLE IF NOT EXISTS users(uid INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT)")
    con.commit()
    
create_db()    