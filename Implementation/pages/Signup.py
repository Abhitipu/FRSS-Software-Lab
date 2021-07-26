from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
from datetime import datetime as dt
import time
import smtplib
import random
import time
import os

import sys
sys.path.append('..')

from tests import *
from pages import my_cursor, mydb, user_id, is_admin

def Signup():
    signup = Toplevel(bg="#ffdc73")
    signup.geometry("650x700")
    signup.title("Sign Up")

    # namel = Label(signup , text = "Name", bg="#adccb0")
    namel = Label(signup,text="Name",bg="#ffdc73",fg="black",font=("Century gothic", 13))
    namel.grid(row = 1 , column = 0, padx=10, pady=10)
    notif = Label(signup, text="Fill in the details!", font=("Comic sans ms", 13), fg="red", bg="#ffdc73")
    notif.grid(row=0, column=0, columnspan=2)
    usernamel = Label(signup , text = "Username", bg="#ffdc73",fg="black",font=("Century gothic", 13))
    usernamel.grid(row = 2 , column = 0, padx=10, pady=10)
    passwordl = Label(signup , text = "Enter password", bg="#ffdc73",fg="black",font=("Century gothic", 13))
    passwordl.grid(row = 3 , column = 0)
    confirmpasswordl = Label(signup , text = "Confirm password", bg="#ffdc73",fg="black",font=("Century gothic", 13))
    confirmpasswordl.grid(row = 4 , column = 0, padx=10, pady=10)
    addressl = Label(signup , text = "Enter the address", bg="#ffdc73",fg="black",font=("Century gothic", 13))
    addressl.grid(row = 5 , column = 0, padx=10, pady=10)
    phonenumberl = Label(signup , text = "Enter the phone number", bg="#ffdc73",fg="black",font=("Century gothic", 13))
    phonenumberl.grid(row = 6 , column = 0, padx=10, pady=10)
    emailIdInput = Label(signup, text = "Enter email id", bg="#ffdc73",fg="black",font=("Century gothic", 13))
    emailIdInput.grid(row = 7 , column =0, padx=10, pady=10)
    sendmailbtn = Button(signup, text="Verify details and send email", font = ("Arial", 10, "bold"),cursor="hand2", bg="#dc143c", fg="white", pady=1)
    sendmailbtn.grid(row=9, padx=40, pady=10, column=0, columnspan=2)
    verifymailbtn = Button(signup, text="Verify OTP!", font = ("Arial", 10), state=DISABLED, bg="#4169e1", fg="white")
    verifymailbtn.grid(row=13, padx=10, pady=10, column=1)

    enterotp = Label(signup, text="Enter the OTP here: ", bg="#ffdc73",fg="black",font=("Century gothic", 13))
    enterotp.grid(row=10, column=0, padx=10, pady=10)

    nameentry = Entry(signup , width = 50, relief=FLAT)
    nameentry.grid(row = 1 , column = 1, padx=10, pady=10)
    usernameentry = Entry(signup , width = 50, relief=FLAT)
    usernameentry.grid(row = 2 , column = 1, padx=10, pady=10)
    passwordentry = Entry(signup , width = 50  , show ='*', relief=FLAT)
    passwordentry.grid(row = 3 , column = 1, padx=10, pady=10)
    confirmpasswordentry = Entry(signup , width = 50  , show = '*', relief=FLAT)
    confirmpasswordentry.grid(row = 4 , column = 1, padx=10, pady=10)
    addressentry = Entry(signup , width = 50, relief=FLAT )
    addressentry.grid(row = 5 , column = 1, padx=10, pady=10)
    phonenumberentry = Entry(signup , width = 50, relief=FLAT)
    phonenumberentry.grid(row = 6 , column = 1, padx=10, pady=10)
    emailentry = Entry(signup, width = 50, relief=FLAT)
    emailentry.grid(row=7, column=1, padx=10, pady=10)
    otpEntry = Entry(signup, width=50, relief=FLAT)
    otpEntry.grid(row=10, column=1, padx=10, pady=10)

    v1 = StringVar(signup , "1")
    adminradiobutton = Radiobutton(signup , text = "Admin" , variable = v1 , value = "1", bg="#ffdc73", font=("Arial", 12))
    adminradiobutton.grid(row = 8 , column = 0, padx=10, pady=10)
    customerradiobutton = Radiobutton(signup , text = "Customer" , variable = v1 , value ="2", bg="#ffdc73", font=("Arial", 12))
    customerradiobutton.grid(row = 8 , column = 1, padx=10, pady=10)

    def verifyNSend():                                      # these checks have to be made!
        name = nameentry.get()
        username = usernameentry.get()
        password = passwordentry.get()
        cpassword = confirmpasswordentry.get()
        address = addressentry.get()
        phonenumber = phonenumberentry.get()
        emailid = emailentry.get()

        global starttime 
        starttime = time.time()
        global otp
        otp = ""

        if v1.get() == "2":
            if name and username and password and cpassword and address and phonenumber and emailid:        
                my_cursor.execute("SELECT username from customers")
                total = my_cursor.fetchall()
                if len(total) > 0 and username in total[0]:
                    messagebox.showwarning("ALERT !" , "User name already registered")
                    usernameentry.delete(0 , END)
                elif password != cpassword:
                    messagebox.showerror("ALERT !" , "Passwords do not match")
                    passwordentry.delete(0 , END)
                    confirmpasswordentry.delete(0 , END)
                else:
                    try:
                        server = smtplib.SMTP('smtp.gmail.com', 587)
                        server.starttls()       # starts a secure shell else you get an error
                        server.login("frental123@gmail.com", "frss20010316") # login information
                        dig = "0123456789"
                        for _ in range(4):
                            otp += random.choice(dig)
                        finalMessage = "OTP for login verification to our Furniture rental store system is " + otp
                        to = emailentry.get()
                        server.sendmail("frental123@gmail.com", to, finalMessage)       # check to
                        notif.config(text = "Success! Email has been sent. Enter OTP sent to email id in 2 minutes", fg = "green")
                        verifymailbtn.config(state=ACTIVE, bg="#4169e1", fg="white")
                    except:
                        messagebox.showerror("Invalid email!" , "Error! Please check the email id entered")
            else:
                messagebox.showwarning("ALERT !" , "Fill all the fields")
                
        else:
            if name and username and password and cpassword and address and phonenumber:
                my_cursor.execute("SELECT username from admins")
                total = my_cursor.fetchall()
                
                if len(total) > 0 and username in total[0]:
                    messagebox.showwarning("ALERT !" , "User name already registered")
                    usernameentry.delete(0 , END)
                    
                elif password != cpassword:
                    messagebox.showwarning("ALERT !" , "Passwords do not match")
                    passwordentry.delete(0 , END)
                    confirmpasswordentry.delete(0 , END)
                else:
                    try:
                        server = smtplib.SMTP('smtp.gmail.com', 587)
                        server.starttls()       # starts a secure shell else you get an error
                        server.login("frental123@gmail.com", "frss1234") # login information
                        dig = "0123456789"
                        for _ in range(4):
                            otp += random.choice(dig)
                        finalMessage = "OTP for login verification to our Furniture rental store system is " + otp
                        to = emailentry.get()
                        server.sendmail("frental123@gmail.com", to, finalMessage)       # check to
                        notif.config(text = "Success! Email has been sent. Enter OTP sent to email id in 2 minutes", fg = "green")
                        verifymailbtn.config(state=ACTIVE, bg="#4169e1", fg="white")
                    except:
                        messagebox.showwarning("Invalid email!" , "Error! Please check the email id entered")
            else:
                messagebox.showwarning("ALERT !" , "Fill all the fields")
                

    def verifyOTP():
        end = time.time()
        t = format(end-starttime)
        if float(t) >= 120:
            messagebox.showinfo("Timed out", "Session expired! Please regenerate OTP")
        else:
            enteredOTP = otpEntry.get()
            if enteredOTP == otp:
                notif.config(text = "Successfully verified OTP! Please click on Sign Up button to add your account!", fg = "green")
                addbutton.config(state=ACTIVE)
            else:
                messagebox.showerror("Invalid OTP", "Please enter a valid OTP!")

    def adduser():
        name = nameentry.get()
        username = usernameentry.get()
        password = passwordentry.get()
        address = addressentry.get()
        phonenumber = phonenumberentry.get()

        if v1.get() == "1":
            exe = 'INSERT INTO admins (name , username , password , address , phonenumber) VALUES (%s , %s , %s , %s , %s)'
            values = (name , username , password , address , phonenumber)
            my_cursor.execute(exe , values)
            mydb.commit()
            notif.config(text="Successfully added to database!")
            testsignup(username)
            

        else:
            exe = 'INSERT INTO customers (name , username , password , address , phonenumber) VALUES (%s , %s , %s , %s , %s)'
            values = (name , username , password , address , phonenumber)
            my_cursor.execute(exe , values)
            mydb.commit()
            notif.config(text="Successfully added to database!")
            testsignup(username)
            
    global sub
    sub = Image.open(os.path.join(os.getcwd() , "images\\signupBtn.jpg"))
    sub = sub.resize((150, 40))
    sub = ImageTk.PhotoImage(sub)
    addbutton = Button(signup,image=sub, command = adduser, width=150, height=40, bg="#ffdc73", relief=FLAT, state = DISABLED)
    addbutton.grid(row=14 , column=1, pady=3)    # configure the state (disabled initially)
    sendmailbtn.config(command=verifyNSend)
    verifymailbtn.config(command=verifyOTP)