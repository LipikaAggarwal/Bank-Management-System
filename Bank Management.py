import mysql.connector
import tkinter as tk
from tkinter import *
import hashlib
import tkinter.messagebox
connect=mysql.connector.connect(host="localhost",user="root",password="@torre58",database=" bank")

root = Tk()
root.title("WELCOME TO BANK")
root.geometry('360x360')
global registerScreen
global servicesScreen
global loginScreen

def regSubmit(nameEntry,pinEntry,initialDepositEntry):
    if nameEntry != "" and pinEntry != "" and initialDepositEntry != "" :
        c=connect.cursor()
        # c.execute("SELECT MAX(ACCNO) from users")
        # maxAccount_no = c.fetchall()
        # print( maxAccount_no)
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
    
    nameLabel = tk.Label(registerScreen, text="Name")
    nameLabel.grid(row=0, column=0, padx=10, pady=(40,40))
    
    nameEntry = tk.Entry(registerScreen)
    nameEntry.grid(row=0, column=1, padx=20, pady=(40,40))
    
    pinLabel = tk.Label(registerScreen, text="PIN")
    pinLabel.grid(row=1, column=0, padx=10, pady=(40,40))
    
    pinEntry = tk.Entry(registerScreen, show="*")
    pinEntry.grid(row=1, column=1, padx=20, pady=(40,40))
    
    initialDepositLabel = tk.Label(registerScreen, text="Initial deposit (ruppees)")
    initialDepositLabel.grid(row=2, column=0, padx=10, pady=(40,40))
    
    initialDepositEntry = tk.Entry(registerScreen)
    initialDepositEntry.grid(row=2, column=1, padx=20, pady=(40,40))

    def delete_all():
        nameEntry.delete(0, END)
        pinEntry.delete(0, END)
        initialDepositEntry.delete(0, END)
    regSubmitButton = tk.Button(registerScreen, text="Submit", command=lambda:[regSubmit(nameEntry.get(), pinEntry.get(), initialDepositEntry.get()),delete_all()])
    regSubmitButton.grid(row=3, column=1, pady=(40,40))

registerLabel = tk.Label(root, text="Or register for a new account:")
registerLabel.grid(row=2, column=0, pady=20)
registerButton = tk.Button(root, text="Register", command=displayRegisterScreen)
registerButton.grid(row=3, column=0, padx=140, pady=(40,40))

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
    
    nameLabel = tk.Label(loginScreen, text="Name")
    nameLabel.grid(row=0, column=0, padx=10, pady=(40,40))
    
    nameEntry = tk.Entry(loginScreen)
    nameEntry.grid(row=0, column=1, padx=20, pady=(40,40))
    
    accntnoLabel = tk.Label(loginScreen, text="Account No")
    accntnoLabel.grid(row=1, column=0, padx=10, pady=(40,40))
    
    accntnoEntry = tk.Entry(loginScreen)
    accntnoEntry.grid(row=1, column=1, padx=20, pady=(40,40))
    
    pinLabel = tk.Label(loginScreen, text="PIN")
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
        
    loginSubmitButton = tk.Button(loginScreen, text="Submit", command=lambda:[loginSubmit(nameEntry.get(), accntnoEntry.get(), pinEntry.get()),delete_all()])
    loginSubmitButton.grid(row=3, column=1, pady=(40,40))    
    
loginLabel = tk.Label(root, text="Login using your existing account:")
loginLabel.grid(row=0, column=0, pady=(40,40))
loginButton = tk.Button(root, text="Log in", command=displayLoginScreen)
loginButton.grid(row=1, column=0, padx=140, pady=(40,40))

# with open("transaction.txt","w+") as f:
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
        # a=f.write("Money Deposited", depositEntry,date,end="\n")
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
            # a=f.write("Money Withdrawn",withdrawEntry ,date,end="\n")
    else:
        tk.messagebox.showerror("Error", "Invalid amount entered!", parent=servicesScreen)
# def transaction(date):
#     b=f.read()
#     c=b.splitlines()
#     d=c.split("")
#     for i in d:
#         servicesScreen.title("Transaction History", "Amount ₹ {}","Date {}" .format(i[1], i[2]), parent=servicesScreen)
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
    
    # dateLabel = tk.Label(servicesScreen, text="Date")
    # dateLabel.grid(row=1, column=0, padx=10, pady=(20,20))
    
    # dateEntry = tk.Entry(servicesScreen)
    # dateEntry.grid(row=1, column=1, padx=20, pady=(20,20))
    
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
    # balanceButton = tk.Button(servicesScreen, text="Transaction History", command=lambda:transaction(dateEntry.get()))
    # balanceButton.grid(row=6, column=1, padx=(20,20), pady=(20,20))
    
                   
root.mainloop()