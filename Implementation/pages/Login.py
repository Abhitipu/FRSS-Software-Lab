from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import os
from pages import my_cursor, is_admin, pass_word

from pages import AdminPage
from pages import CustomerPage

import sys
sys.path.append('..')

from tests import *

def Login(self):
    self.destroy()
    login = Tk()
    login.title("Log In to your account")
    loginBg = "#f1e39b"

    notif = Label(login, text="   Fill in your login details !", font=("Comic sans ms", 13), fg="red", bg=loginBg)
    notif.grid(row=0, column=0, columnspan=2, padx=(70,0), pady=10)
    login.geometry("500x400")
    login.config(bg=loginBg)
    v1 = StringVar(login , "1")
    adminradiobutton = Radiobutton(login , text = "Admin" , variable = v1 , value = "1", font=("Arial", 12), bg=loginBg)
    customerradiobutton = Radiobutton(login , text = "Customer" , variable = v1 , value ="2", font=("Arial", 12), bg=loginBg)
    usernamel = Label(login , text = "Username", bg=loginBg,font=("Century gothic", 13))
    usernamel.grid(row = 1 , column = 0, padx=80, pady=10)
    passwdl = Label(login , text = "Password", bg=loginBg,font=("Century gothic", 13))
    passwdl.grid(row = 2 , column = 0, padx=(80,80), pady=10)
    adminradiobutton.grid(row = 3 , column = 0, padx=(80,80), pady=10)
    customerradiobutton.grid(row = 3 , column = 1, pady=10)

    def adduser():
        username = usernameentry.get()
        password = passwordentry.get()
        
        # print(username , password)
        if username and password:
            if v1.get() == "2":
                exe =  f'SELECT username , password FROM customers WHERE username = "{username}" AND password = "{password}"'
                
                my_cursor.execute(exe)
                result  = my_cursor.fetchall()
                if len(result) == 0 :
                    messagebox.showerror("Error", "Invalid Username or Password !")
                    return 
                global user_id , pass_word , is_admin
                user_id = result[0][0]
                pass_word = result[0][1]
                testcustomerlogin(username, user_id)
                is_admin = False
                CustomerPage.CustomerPage(login)
            else :
                exe =  f'SELECT username , password FROM admins WHERE username = "{username}" AND password = "{password}"'
                # global user_id , pass_word , is_admin
                my_cursor.execute(exe)
                result  = my_cursor.fetchall()
                if len(result) == 0 :
                    messagebox.showerror("Error", "Invalid Username or Password !")
                    return
                user_id = result[0][0]
                pass_word = result[0][1]
                testadminlogin(username, user_id)
                is_admin = True
                AdminPage.AdminPage(login)

        else:
            messagebox.showwarning("ALERT !" , "All fields should be filled !")

    usernameentry = Entry(login, relief=FLAT)
    usernameentry.grid(row = 1 , column = 1)
    passwordentry = Entry(login , show ='*', relief=FLAT)
    passwordentry.grid(row = 2 , column = 1)
    global lb
    loginbtn_path = os.path.join(os.getcwd() , "images\\loginBtn.jpg")
    lb = Image.open(loginbtn_path)
    lb = lb.resize((150, 45))
    lb = ImageTk.PhotoImage(lb)
    completelogin = Button(login ,image = lb, command = adduser, bg=loginBg, relief=FLAT)
    completelogin.grid(row = 4 , column = 0, columnspan = 2, padx=(70,0))
