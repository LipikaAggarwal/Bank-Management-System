from mysql.connector import Error
import mysql.connector
import tkinter as tk
from tkinter import *
import hashlib
import tkinter.messagebox
from tkinter import ttk,messagebox as tkMessageBox
import os
connect=mysql.connector.connect(host="localhost",user="root",password="@torre58",database=" bank")

root = Tk()
root.title("WELCOME TO BANK")
root.geometry('480x480')
canvas = Canvas(root, width=500, height=450, bd=0, highlightthickness=0, highlightbackground="yellow", bg="Light blue")
canvas.place(x=0,y=0)
# global updatescreen
global adminscreen
global registerScreen
global servicesScreen
global loginScreen
global amt
global k
global customerScreen
# admin credential
admin_id = 0000
admin_passwd = 'root'

def ck_user():
    cursor = connect.cursor()
    cursor.execute("select * from users")
    r=cursor.fetchall()
    
    canvas = Canvas(adminscreen, width=500, height=450, bd=0, highlightthickness=0, highlightbackground="yellow", bg="Light blue")
    canvas.place(x=0,y=0)
    
    tree = ttk.Treeview(canvas,columns=("1","2","3"),selectmode="browse")
    tree.heading('#0', text="Account No",anchor=W)
    tree.heading('1', text="Name",anchor=W)
    tree.heading('2', text="Phone No",anchor=W)
    tree.heading('3', text="Balance",anchor=W)
    tree.column("#0", width=110,stretch=NO)
    tree.column("1", width=110, stretch=NO)
    tree.column("2", width=110,stretch=NO)
    tree.column("3", width=110,stretch=NO)

    scrollbar_vertical = ttk.Scrollbar(canvas, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar_vertical.set)

    tree.place(x=20,y=20)
    
    scrollbar_vertical.place(x=465, y=20,relheight=0.51)

    # print(r)
    len(r)
    for i in range(len(r)):
                tree.insert('','end',text=r[i][0], values=(r[i][1],r[i][2],r[i][3]))
                
    Button(adminscreen,text="Back",command=main_menu_admin,activebackground="red",activeforeground="black",fg="white",bg="darkblue",width=20).place(x=180,y=280)

def main_menu_admin():
    global adminscreen
    adminscreen = Toplevel(root) 
    adminscreen.title("Admin console")
    adminscreen.geometry('480x480')
    canvas = Canvas(adminscreen, width=500, height=450, bd=0, highlightthickness=0, highlightbackground="yellow", bg="Light blue")
    canvas.place(x=0,y=0)
 
    Customers_detailsLabel = tk.Label(adminscreen, text="Customers Details",fg="black",bg="light blue",width=20)
    Customers_detailsLabel.grid(row=4, column=0, padx=10, pady=(20,20))
    Customers_detailsButton = tk.Button(adminscreen, text="Customers Details", command=lambda:[ck_user()],activebackground="white",activeforeground="black",fg="white",bg="black",width=20)
    Customers_detailsButton.grid(row=4, column=1, padx=(20,25), pady=(20,20))

adminLabel = tk.Label(root, text="Admin Console",fg="black",bg="light blue",width=20)
adminLabel.grid(row=2, column=0, pady=20)
adminButton = tk.Button(root, text="Admin", command=main_menu_admin,activebackground="white",activeforeground="black",fg="white",bg="black",width=20)
adminButton.grid(row=3, column=0, padx=140, pady=(40,40))

userLabel = tk.Label(root, text="customer",fg="black",bg="light blue",width=20)
userLabel.grid(row=4, column=0, pady=20)
userButton = tk.Button(root, text="customer", command=lambda:[customer()],activebackground="white",activeforeground="black",fg="white",bg="black",width=20)
userButton.grid(row=5, column=0, padx=140, pady=(40,40))



def regSubmit(nameEntry,pinEntry,initialDepositEntry):
    if nameEntry != "" and pinEntry != "" and initialDepositEntry != "" :
        c=connect.cursor()
        connect.commit()
        account_no = hashlib.md5(f'{nameEntry}{initialDepositEntry}{pinEntry}'.encode('utf-8')).hexdigest()
        a=''.join(i for i in account_no if i.isdigit())[0:11:1]
        sql="INSERT INTO users (NAME, ACCNO, PIN, AMOUNT) VALUES (%s,%s,%s,%s)"
        user=(nameEntry,a,pinEntry,initialDepositEntry)
        c.execute(sql,user)
        connect.commit()
        tk.messagebox.showinfo("Registration Successful", "Your account number is: {} .".format(a), parent=registerScreen)
    else:
        tk.messagebox.showerror("Registration Failed", "Invalid entries! Try again.", parent=registerScreen)
pass

def displayRegisterScreen():
    global registerScreen
    registerScreen = Toplevel(root) 
    registerScreen.title("Registration ")
    registerScreen.geometry('360x480')
    canvas = Canvas(registerScreen, width=500, height=450, bd=0, highlightthickness=0, highlightbackground="yellow", bg="Light blue")
    canvas.place(x=0,y=0)
    
    nameLabel = tk.Label(registerScreen, text="Name",fg="black",bg="light blue",width=20)
    nameLabel.grid(row=0, column=0, padx=10, pady=(40,40))
    
    nameEntry = tk.Entry(registerScreen)
    nameEntry.grid(row=0, column=1, padx=20, pady=(40,40))
    
    pinLabel = tk.Label(registerScreen, text="PIN",fg="black",bg="light blue",width=20)
    pinLabel.grid(row=1, column=0, padx=10, pady=(40,40))
    
    pinEntry = tk.Entry(registerScreen, show="*")
    pinEntry.grid(row=1, column=1, padx=20, pady=(40,40))
    
    initialDepositLabel = tk.Label(registerScreen, text="Initial deposit (ruppees)",fg="black",bg="light blue",width=20)
    initialDepositLabel.grid(row=2, column=0, padx=10, pady=(40,40))
    
    initialDepositEntry = tk.Entry(registerScreen)
    initialDepositEntry.grid(row=2, column=1, padx=20, pady=(40,40))

    def delete_all():
        nameEntry.delete(0, END)
        pinEntry.delete(0, END)
        initialDepositEntry.delete(0, END)
    regSubmitButton = tk.Button(registerScreen, text="Submit", command=lambda:[regSubmit(nameEntry.get(), pinEntry.get(), initialDepositEntry.get()),delete_all()],activebackground="white",activeforeground="black",fg="white",bg="black",width=20)
    regSubmitButton.grid(row=3, column=1, pady=(40,40))

def loginSubmit(name, account_no, pin):
    if name != "" and account_no != ""  and pin != "":
        c = connect.cursor()
        sql1="SELECT * FROM users WHERE NAME=%s and ACCNO=%s and PIN=%s"
        user1=(name, account_no, pin,)
        c.execute(sql1,user1)
        account = c.fetchall()
        print(account)
        
        if len(account)!=0:
                displayServicesScreen(account_no)
        else:
            tk.messagebox.showerror("Login failed", "Invalid Credentials!", parent=loginScreen)
    else:
        tk.messagebox.showerror("Login failed", "Invalid Credentials!", parent=loginScreen)
    
def displayLoginScreen():
    global loginScreen
    loginScreen = Toplevel(root)
    loginScreen.title("Login Account")
    loginScreen.geometry('360x480')
    # root.withdraw()
    canvas = Canvas(loginScreen, width=500, height=450, bd=0, highlightthickness=0, highlightbackground="yellow", bg="Light blue")
    canvas.place(x=0,y=0)
    
    nameLabel = tk.Label(loginScreen, text="Name",fg="black",bg="light blue",width=20)
    nameLabel.grid(row=0, column=0, padx=10, pady=(40,40))
    
    nameEntry = tk.Entry(loginScreen)
    nameEntry.grid(row=0, column=1, padx=20, pady=(40,40))
    
    accntnoLabel = tk.Label(loginScreen, text="Account No",fg="black",bg="light blue",width=20)
    accntnoLabel.grid(row=1, column=0, padx=10, pady=(40,40))
    
    accntnoEntry = tk.Entry(loginScreen)
    accntnoEntry.grid(row=1, column=1, padx=20, pady=(40,40))
    
    pinLabel = tk.Label(loginScreen, text="PIN",fg="black",bg="light blue",width=20)
    pinLabel.grid(row=2, column=0, padx=10, pady=(40,40))
    
    pinEntry = tk.Entry(loginScreen, show="*")
    pinEntry.grid(row=2, column=1, padx=20, pady=(40,40))    
    
    def delete_all():
        nameEntry.delete(0, END)
        accntnoEntry.delete(0, END)
        pinEntry.delete(0, END)
    
    c = connect.cursor()
    sql1="SELECT * FROM users"
    c.execute(sql1)
    c.fetchall()
        
    loginSubmitButton = tk.Button(loginScreen, text="Submit", command=lambda:[loginSubmit(nameEntry.get(), accntnoEntry.get(), pinEntry.get()),delete_all()],activebackground="white",activeforeground="black",fg="white",bg="black",width=20)
    loginSubmitButton.grid(row=3, column=1, pady=(40,40))    
def customer():
    global customerScreen
    customerScreen = Toplevel(root)
    customerScreen.title("Customer Window")
    customerScreen.geometry('480x480')

    canvas = Canvas(customerScreen, width=500, height=450, bd=0, highlightthickness=0, highlightbackground="yellow", bg="Light blue")
    canvas.place(x=0,y=0)

    loginLabel = tk.Label(customerScreen, text="Login using your existing account:",bg="Light blue")
    loginLabel.grid(row=0, column=0, pady=(40,40))
    loginButton = tk.Button(customerScreen, text="Log in", command=displayLoginScreen,activebackground="red",activeforeground="black",fg="white",bg="black",width=20)
    loginButton.grid(row=1, column=0, padx=140, pady=(40,40))

    registerLabel = tk.Label(customerScreen, text="Or register for a new account:",bg="Light blue")
    registerLabel.grid(row=2, column=0, pady=20)
    registerButton = tk.Button(customerScreen, text="Register", command=displayRegisterScreen,activebackground="red",activeforeground="black",fg="white",bg="black",width=20)
    registerButton.grid(row=3, column=0, padx=140, pady=(40,40))

def deposit(account_no, depositEntry):
    if account_no != "" and depositEntry != "" :
        c = connect.cursor()
        sql="UPDATE users SET AMOUNT=AMOUNT+%s WHERE ACCNO=%s"
        sql2="SELECT AMOUNT FROM users WHERE ACCNO=%s"
        user=(depositEntry,account_no,)
        user2=(account_no,)
        c.execute(sql,user)
        c.execute(sql2,user2)
        b = c.fetchall()
        b = b[0][0]
        connect.commit()
        tk.messagebox.showinfo("Money Deposited Successfully", "You have deposited ₹ {}\n Updated balance: ₹ {}".format(depositEntry, b))
    else:
        tk.messagebox.showerror("Error", "Invalid amount entered!", parent=servicesScreen)
        
def withdraw(account_no, withdrawEntry):
    if account_no != "" and withdrawEntry != "":
        c = connect.cursor()
        sql="SELECT AMOUNT FROM users WHERE ACCNO=%s"
        user=(account_no,)
        c.execute(sql,user)
        b = c.fetchall()
        b = b[0][0]        
        connect.commit()
        if int(withdrawEntry) > b:
            tk.messagebox.showerror("Error""Insufficient funds!", parent=servicesScreen)
        else:
            sql="UPDATE users SET AMOUNT=AMOUNT-%s WHERE ACCNO=%s"
            user=(withdrawEntry,account_no,)
            c.execute(sql,user)
            sql1="SELECT AMOUNT FROM users WHERE ACCNO=%s"
            user1=(account_no,)
            c.execute(sql1,user1)
            b = c.fetchall()
            b = b[0][0]        
            connect.commit()
            tk.messagebox.showinfo("Money Withdrawn Successfully", "You have withdrawn ₹ {}\n Updated balance: ₹ {}".format(withdrawEntry, b), parent=servicesScreen)
    else:
        tk.messagebox.showerror("Error", "Invalid amount entered!", parent=servicesScreen)
        
def checkBalance(account_no):
    c = connect.cursor()
    sql="SELECT AMOUNT FROM users WHERE ACCNO=%s"
    user=(account_no,)
    c.execute(sql,user)
    bal = c.fetchall()
    tk.messagebox.showinfo("Balance","Your account balance is: ₹ {}".format(bal[0][0]), parent=servicesScreen) 

def displayServicesScreen(account_no):
    global servicesScreen
    c = connect.cursor()
    sql="SELECT name FROM users WHERE ACCNO=%s"
    user=(account_no,)
    c.execute(sql,user)
    name = c.fetchall()
    connect.commit()
    servicesScreen = Toplevel(root)
    servicesScreen.title("Welcome {}".format(name[0][0]))
    servicesScreen.geometry('360x580')
    
    def clearDeposit():
        depositEntry.delete(0, END)
        
    def clearWithdraw():
        withdrawEntry.delete(0, END)
    
    depositLabel = tk.Label(servicesScreen, text="Deposit (₹)")
    depositLabel.grid(row=0, column=0, padx=10, pady=(20,20))
    
    depositEntry = tk.Entry(servicesScreen)
    depositEntry.grid(row=0, column=1, padx=20, pady=(20,20))
    
    depositButton = tk.Button(servicesScreen, text="Deposit", command=lambda:[deposit(account_no, depositEntry.get()), clearDeposit()])
    depositButton.grid(row=2, column=1, padx=(20,25), pady=(20,20))
    
    withdrawLabel = tk.Label(servicesScreen, text="Withdraw (₹)")
    withdrawLabel.grid(row=3, column=0, padx=10, pady=(20,20))
    
    withdrawEntry = tk.Entry(servicesScreen)
    withdrawEntry.grid(row=3, column=1, padx=20, pady=(20,20))
    
    withdrawButton = tk.Button(servicesScreen, text="Withdraw", command=lambda:[withdraw(account_no, withdrawEntry.get()), clearWithdraw()])
    withdrawButton.grid(row=4, column=1, padx=(20,20), pady=(20,20))    
    
    balanceButton = tk.Button(servicesScreen, text="Check Balance", command=lambda:checkBalance(account_no))
    balanceButton.grid(row=5, column=1, padx=(20,20), pady=(20,20))
               
root.mainloop()
