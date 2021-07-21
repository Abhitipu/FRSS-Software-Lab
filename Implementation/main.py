# from FRSS.test import testsignup
# from FRSS.test import deleteuser
from abc import ABC , abstractmethod
from tkinter import *
import matplotlib.pyplot as plt
from PIL import ImageTk, Image
from tkinter import filedialog
from tkinter import messagebox
import mysql.connector
from datetime import datetime as dt
import math
import smtplib
import random
import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,  NavigationToolbar2Tk
from test import *
import unittest
import os

global user_id , pass_word , is_admin

def CustomerPage(self) :
    self.destroy()
    customer = Tk()
    customer.geometry("1000x600")
    customer.title("Customer page")
    leftBg = "#67faaf"
    rightBg = "#6d2358"
    rightFrame = Frame(customer , width = 50 , height= 100 , background = rightBg)
    leftFrame = Frame(customer , width = 50 , height = 100 , background = leftBg)
    leftFrame.grid(row = 0 , column = 0 , sticky = "nsew")
    rightFrame.grid(row = 0 , column = 1 , sticky = "nsew")
    customer.grid_columnconfigure(0 , weight = 2)
    customer.grid_columnconfigure(1 , weight = 3)
    customer.grid_rowconfigure(0 , weight = 1)
    leftFrame.grid_propagate(False)
    leftFrame.pack_propagate(False)
    rightFrame.grid_propagate(False)
    rightFrame.pack_propagate(False)


    def buynowonloan():
        loan = Tk()
        loan.geometry("500x500")
        loan.title("Buy on loan")
        bgCol = "#fdf5e6"
        loan.config(bg=bgCol)
        l1 = Label(loan , text = "Enter the id of the furniture", bg=bgCol, font=("Linux Biolinum G", 12))
        l1.grid(row = 0 , column = 0, padx=10, pady=10)
        e1 = Entry(loan)
        e1.grid(row = 0 , column = 1)
        l2 = Label(loan , text = "Enter the days to rent", bg=bgCol, font=("Linux Biolinum G", 12))
        e2 = Entry(loan)
        l2.grid(row = 1, column = 0, padx=10, pady=10)
        e2.grid(row = 1 , column = 1)
        ex = "SELECT COUNT(username) FROM past_orders WHERE username = %s"
        va = (user_id , )
        my_cursor.execute(ex , va)
        count = my_cursor.fetchall()[0][0]
        l3 = Label(loan , text = "Your past orders : " + str(count), bg=bgCol, font=("Comic Sans MS", 13, "italic"))
        l3.grid(row = 2 , column = 0 , columnspan = 2, pady=10)
        # print(count)

        def checkprice():
            fur_id = e1.get()
            num_days = e2.get()
            ex = "SELECT interest_rate FROM furnitures WHERE id = %s"
            va = (fur_id , )
            my_cursor.execute(ex , va)
            interest_rate = my_cursor.fetchall()
            new_interest = float(interest_rate[0][0])*(2**(-count))
            l4 = Label(loan , text = "Interest Rate on your experience with us : " + str(new_interest), bg = bgCol ,font=("Centaur", 10, "italic"))
            l4.grid(row = 3 , column = 0 , columnspan = 2, padx=10, pady=10)
            ex = "SELECT price FROM furnitures WHERE id = %s"
            va = (fur_id , )
            my_cursor.execute(ex , va)
            old_price = my_cursor.fetchall()
            # print("old Price " + str(old_price))
            global new_price
            new_price = float(old_price[0][0])*(1+new_interest*int(num_days)/100)
            l5 = Label(loan , text = "Total price on your experience with us : " + str(new_price), bg = bgCol ,font=("Centaur", 10, "italic"))
            l5.grid(row = 4 , column = 0 , columnspan = 2, padx=10, pady=10)
            pass

        def buynow():
            fur_id = e1.get()
            num_days = int(e2.get())
            ex = "UPDATE furnitures SET rented = %s , days_rented = days_rented + %s WHERE id = %s"
            va = (2 , num_days , fur_id)
            my_cursor.execute(ex , va)
            mydb.commit()
            ex = "INSERT INTO past_orders (username , furniture_id) VALUES (%s , %s)"
            va = (user_id , fur_id)
            my_cursor.execute(ex , va)
            mydb.commit()
            ex = "UPDATE customers SET amountdue = %s WHERE username = %s"
            messagebox.showinfo("Information", "Furniture Purchased !")
            va = (new_price , user_id)
            my_cursor.execute(ex , va)
            mydb.commit()
            CustomerPage(customer)
            pass

        b1 = Button(loan , text = "Buy Now" , command = buynow, bg="#002366", font=("Arial", 13, "bold"), fg="white")
        b1.grid(row = 7 , column = 0, padx=10, pady=10, columnspan=2)
        b2 = Button(loan , text = "Check Price" , command = checkprice, bg="#991229", font=("Arial", 13, "bold"), fg="white")
        b2.grid(row = 6 , column = 0, padx=10, pady=10, columnspan=2)
        pass

    def buynowonrent():
        rent = Tk()
        rent.geometry("500x500")
        bgCol = "#fdf5e6"
        rent.config(bg=bgCol)
        rent.title("Buy now on rent")
        l1 = Label(rent , text = "Enter the id of the furniture", bg=bgCol, font=("Linux Biolinum G", 12))
        l1.grid(row = 0 , column = 0, padx=10, pady=10)
        e1 = Entry(rent)
        e1.grid(row = 0 , column = 1)
        l2 = Label(rent , text = "Enter the days to rent ", bg=bgCol, font=("Linux Biolinum G", 12))
        e2 = Entry(rent)
        l2.grid(row = 1, column = 0 , padx=10, pady=10)
        e2.grid(row = 1 , column = 1)

        def checkprice():
            fur_id = e1.get()
            num_days = e2.get()
            ex = "SELECT price FROM furnitures WHERE id = %s"
            va = (fur_id , )
            my_cursor.execute(ex , va)
            old_price = my_cursor.fetchall()
            global ne_price
            ne_price = old_price[0][0]*math.ceil(int(num_days)/10)
            l5 = Label(rent , text = "Total price on your experience with us : " + str(ne_price),bg = bgCol, font=("Centaur", 10, "italic"))
            l5.grid(row = 4 , column = 0 , columnspan = 2)
            pass

        def buynow():
            fur_id = e1.get()
            num_days = int(e2.get())
            ex = "UPDATE furnitures SET rented = %s , days_rented = days_rented + %s WHERE id = %s"
            va = (1 , num_days , fur_id)
            my_cursor.execute(ex , va)
            mydb.commit()
            ex = "INSERT INTO past_orders (username , furniture_id) VALUES (%s , %s)"
            va = (user_id , fur_id)
            my_cursor.execute(ex , va)
            mydb.commit()
            ex = "SELECT profit FROM admins LIMIT 1"
            my_cursor.execute(ex)
            res = my_cursor.fetchall()
            ex = "SELECT username FROM admins LIMIT 1"
            my_cursor.execute(ex)
            re = my_cursor.fetchall()
            ex ="UPDATE admins SET profit = %s WHERE username = %s"
            va = (ne_price + res[0][0] , re[0][0])
            my_cursor.execute(ex , va)
            mydb.commit()
            exe = "SELECT profit FROM graph WHERE id = (SELECT max(id) FROM graph)"
            my_cursor.execute(exe)
            oldprofit = my_cursor.fetchall()
            exe = "SELECT investment FROM graph WHERE id = (SELECT max(id) FROM graph)"
            my_cursor.execute(exe)
            oldinvestment = my_cursor.fetchall()
            exe = "INSERT INTO graph (profit , investment) VALUES (%s , %s)"
            va = (float(oldprofit[0][0])+float(ne_price), float(oldinvestment[0][0]))
            my_cursor.execute(exe , va)
            mydb.commit()
            messagebox.showinfo("Information", "Furniture Purchased !")
            CustomerPage(customer)
            pass

        b2 = Button(rent , text = "Check Price" , command = checkprice, font=("Arial", 13, "bold"), fg="white", bg="#002366")
        b2.grid(row = 5 , column = 0, padx=10, pady=10, columnspan=2)

        b1 = Button(rent , text = "Buy Now" , command = buynow, font=("Arial", 13, "bold"), fg="white", bg="#991229")
        b1.grid(row = 6 , column = 0, padx=10, pady=10, columnspan=2)
        pass

    def returnitem():
        item = Tk()
        item.geometry("500x500")
        item.title("Return item")
        bgCol = "#ffdc73"
        item.config(bg=bgCol)
        l6 = Label(item , text = "Enter the id of the furniture : ", bg=bgCol, font=("Times new roman", 14))
        l6.grid(row = 0 , column = 0, padx=10, pady=10)
        e6 = Entry(item, relief=FLAT)
        e6.grid(row = 0 , column = 1)

        def addreturn():
            temp = e6.get()
            if temp:
                ex = "INSERT INTO current_returns (username , furniture_id) VALUES (%s , %s)"
                va = (user_id , int(e6.get()))
                my_cursor.execute(ex , va)
                mydb.commit()
                messagebox.showinfo("Information", "Return Process Initiated, you will be notified soon !")
                testreturnadded(e6.get())
            else:
                messagebox.showwarning("Warning", "Enter the ID !")
            pass

        b6 = Button(item , text = "Add to return" , command = addreturn, bg="#800080", font=("Arial", 12, "bold"), fg="white")
        b6.grid(row = 1 , column = 1, padx=10, pady=10)
        pass

    def checkamountdue():
        amount = Tk()
        amount.geometry("500x500")
        amount.title("Amount details")
        cbg="#00eaff"
        amount.config(bg=cbg)
        ex = "SELECT amountdue FROM customers WHERE username = %s"
        va = (user_id , )
        my_cursor.execute(ex , va)
        res = my_cursor.fetchall()[0][0]
        l1 = Label(amount , text = "Your amount due : " + str(res), bg=cbg, font=("Comic sans ms", 13))
        l1.grid(row=0, column=0,padx=10, pady=10, columnspan=2)
        testcustomeramountdue(user_id, res)
        l2 = Label(amount , text = "Enter amount to be paid", bg=cbg, font=("Comic sans ms", 13))
        l2.grid(row=1, column=0, padx=10, pady=10)
        e2 = Entry(amount, relief=FLAT)
        e2.grid(row=1, column=1)

        def paynow():
            
            money = (e2.get())
            if money:
                money = float(money)
                ex = "SELECT profit FROM admins LIMIT 1"
                my_cursor.execute(ex)
                r = my_cursor.fetchall()
                new_profit = r[0][0] + money
                ex = "SELECT username FROM admins LIMIT 1"
                my_cursor.execute(ex)
                re = my_cursor.fetchall()
                ex ="UPDATE admins SET profit = %s WHERE username = %s"
                va = (new_profit , re[0][0])
                my_cursor.execute(ex , va)
                mydb.commit()
                ex = "UPDATE customers SET amountdue = %s WHERE username = %s"
                va = (max(res-money , 0) , user_id)
                my_cursor.execute(ex , va)
                mydb.commit()
                testpaymentdone(user_id, res)
                messagebox.showinfo("Information", "Amount Paid !")
                exe = "SELECT profit FROM graph WHERE id = (SELECT max(id) FROM graph)"
                my_cursor.execute(exe)
                oldprofit = my_cursor.fetchall()
                exe = "SELECT investment FROM graph WHERE id = (SELECT max(id) FROM graph)"
                my_cursor.execute(exe)
                oldinvestment = my_cursor.fetchall()
                exe = "INSERT INTO graph (profit , investment) VALUES (%s , %s)"
                va = (float(oldprofit[0][0])+float(money), float(oldinvestment[0][0]))
                my_cursor.execute(exe , va)
                mydb.commit()
            else:
                messagebox.showwarning("Warning", "No money added !")
            pass

        b1 = Button(amount , text = "Pay amount due !" , command = paynow, bg="#60e84e", font=("Arial", 13, "bold"))
        b1.grid(row=2, column=0, padx=10, pady=10, columnspan=2)
        pass

    def pastorder():
        past = Tk()
        past.geometry("500x500")
        past.title("Past order history")
        ex = "SELECT * FROM past_orders WHERE username = %s"
        va = (user_id , )
        my_cursor.execute(ex , va)
        res = my_cursor.fetchall()
        text_scroll = Scrollbar(past)
        text_scroll.pack(side = RIGHT , fill = Y)
        my_text = Text(past , width = 100 , height = 120 , font = ('Comic sans ms' , 10) , yscrollcommand = text_scroll.set, spacing1=8)
        my_text.pack(pady = 10 , padx = 10)
        text_scroll.config(command = my_text.yview)
        for furniture in res:
            my_text.insert(END , "          Furniture id = " + str(furniture[2]) + "\n")
        pass

    def giveFeedback():
        give = Tk()
        give.geometry("800x500")
        give.title("Give feedback")
        gbg = "#fdcb9f"
        give.config(bg = gbg)
        lab2 = Label(give , text = "Enter the name of the furniture", bg=gbg, font=("Courier New", 12, "bold"))
        lab2.grid(row = 0 ,column = 0, padx=10, pady=10)
        ent2 = Entry(give, relief=FLAT, width=70)
        ent2.grid(row = 0 , column = 1)
        lab1 = Label(give , text = "Give Feedback", bg=gbg, font=("Courier New", 12, "bold"))
        lab1.grid(row = 1,column = 0, padx=10, pady=10)
        ent1 = Entry(give, relief=FLAT, width=70)
        ent1.grid(row = 1 , column = 1)
        
        def submitFeedback():
            typ = ent2.get()
            feed = ent1.get()
            if typ and feed:
                ex = "INSERT INTO feedbacks (type , review) VALUES (%s , %s)"
                va = (typ , feed)
                my_cursor.execute(ex , va)
                mydb.commit()
                testfeedbackinsert(typ, feed)
                messagebox.showinfo("Information", "Feedback Submitted !")
            else:
                messagebox.showwarning("Warning", "All fields must be filled !")
            
            pass

        but1 = Button(give , text = "Submit feedback" , command = submitFeedback, bg="#60e84e", font=("Arial", 13, "bold"))
        but1.grid(row = 2 , column = 0 , columnspan = 2, padx=10, pady=10)

        pass

    def searchFurniture():
        search = Tk()
        search.geometry("800x500")
        search.title("Search for furniture")
        lbg = "#ccff47"
        rbg = "#f56c00"
        frame1 = Frame(search , background = lbg)
        frame1.grid(row = 0 , column = 0 , sticky = "nsew")
        frame2 = Frame(search , background = rbg)
        frame2.grid(row = 0 , column = 1 , sticky = "nsew")
        search.grid_columnconfigure(0 , weight = 2)
        search.grid_columnconfigure(1 , weight = 3)
        search.grid_rowconfigure(0 , weight = 1)
        frame1.grid_propagate(False)
        frame2.grid_propagate(False)
        frame1.pack_propagate(False)
        frame2.pack_propagate(False)
        la1 = Label(frame1 , text = "Enter the name :", font=("Times new roman", 14), bg=lbg)
        la1.grid(row = 0 , column = 0, padx=10, pady=10)
        ent1 = Entry(frame1, relief=FLAT, font=("Comic sans ms", 9))
        ent1.grid(row = 0 , column = 1)
        text_scroll2 = Scrollbar(frame2)
        text_scroll2.pack(side = RIGHT , fill = Y)
        my_text2 = Text(frame2 , width = 100 , height = 120 , font = ('Comic sans ms' , 10) , yscrollcommand = text_scroll2.set, spacing1=8)
        my_text2.pack(pady = 10 , padx = 10)
        text_scroll2.config(command = my_text2.yview)
        global my_imag
        global imag
        imag = []
        def searchNow():
            my_text2.delete("1.0" , END)
            typ = ent1.get()
            exe = "SELECT * FROM furnitures WHERE rented = 0"
            my_cursor.execute(exe)
            relu = my_cursor.fetchall()
            for furniture in relu:
                if typ in furniture[5]:
                    # print("type", typ)
                    # print("furniture" , furniture)
                    my_imag = Image.open(furniture[7])
                    my_imag = my_imag.resize((120,150) , Image.ANTIALIAS)
                    # my_imag = my_imag.rotate(270)
                    my_imag = ImageTk.PhotoImage(my_imag , master = frame2)
                    my_text2.image_create(END , image = my_imag, padx=40, pady=10)
                    my_text2.insert(END , '\n')
                    imag.append(my_imag)
                    my_text2.insert(END , "         Id : " + str(furniture[0]) + '\n')
                    my_text2.insert(END , "         Name : " + furniture[5] + '\n')
                    my_text2.insert(END , "         Company : " + furniture[2] + '\n')
                    my_text2.insert(END , "         Price : " + str(furniture[3]) + '\n')
                    my_text2.insert(END , "         Description : " + furniture[4] + '\n')
                    my_text2.insert(END , "         Interest Rate : " + str(furniture[8]) + '\n')
                    ex = "SELECT review FROM feedbacks WHERE type = %s"
                    va = (furniture[5],)
                    my_cursor.execute(ex , va)
                    rel = my_cursor.fetchall()
                    my_text2.insert(END , "         Reviews :\n")
                    for feedback in rel:
                        my_text2.insert(END , "         "+ feedback[0] + "\n")
                        pass
                    my_text2.insert(END , "\n\n")
            pass

        bu1 = Button(frame1 , text = "Search Now" , command = searchNow, bg="red", fg="white", font=("Centaur", 14, "bold"))
        bu1.grid(row = 1 , column = 0 , columnspan = 2, padx=10, pady=10)
        pass

    def logOut():
        Login(customer)
        pass
    
    BtnBg = "#f3893E"
    buy_now_on_loan = Button(leftFrame , text = "Buy Now On Loan" , width = 35 , command = buynowonloan, bg=BtnBg, font=("Century gothic", 13))
    buy_now_on_loan.pack(padx=10, pady=(50, 10))
    buy_now_on_rent = Button(leftFrame , text = "Buy Now On Rent" , width = 35 , command = buynowonrent, bg=BtnBg, font=("Century gothic", 13))
    buy_now_on_rent.pack(padx=10, pady=10)
    returnbutton = Button(leftFrame , text = "Return" , width = 35 , command = returnitem, bg=BtnBg, font=("Century gothic", 13))
    returnbutton.pack(padx=10, pady=10)
    amountdue = Button(leftFrame , text = "Amount Due" , width = 35 , command = checkamountdue, bg=BtnBg, font=("Century gothic", 13))
    amountdue.pack(padx=10, pady=10)
    pastorder = Button(leftFrame , text = "Past Order History" , width = 35 , command = pastorder, bg=BtnBg, font=("Century gothic", 13))
    pastorder.pack(padx=10, pady=10)
    feedback = Button(leftFrame , text = "Give Feedback" , command = giveFeedback, bg=BtnBg, font=("Century gothic", 13), width=35)
    feedback.pack(padx=10, pady=10)
    searchbutton = Button(leftFrame , text = "Search furniture" , width = 35,command = searchFurniture, bg=BtnBg, font=("Century gothic", 13))
    searchbutton.pack(padx=10, pady=10)
    logout = Button(leftFrame , text = "Log Out" , width = 35 , command = logOut, bg=BtnBg, font=("Century gothic", 13))
    logout.pack(padx=10, pady=10)

    text_scroll = Scrollbar(rightFrame)
    text_scroll.pack(side = RIGHT , fill = Y)
    my_text = Text(rightFrame , width = 100 , height = 120 , font = ('Comic Sans Ms' , 10) , yscrollcommand = text_scroll.set, spacing1=8)
    my_text.pack(pady = 10 , padx = 10)
    text_scroll.config(command = my_text.yview)
    global my_image
    global images
    images = []

    exe = "SELECT * FROM furnitures WHERE rented = 0 group by price ,type"
    my_cursor.execute(exe)
    result = my_cursor.fetchall()
    for furniture in result:
        # print(furniture)
        my_image = Image.open(furniture[7])
        my_image = my_image.resize((120,150) , Image.ANTIALIAS)
        # my_image = my_image.rotate(270)
        my_image = ImageTk.PhotoImage(my_image)
        my_text.image_create(END , image = my_image, padx=40, pady=10)
        my_text.insert(END , '\n')
        images.append(my_image)
        my_text.insert(END , "          Id : " + str(furniture[0]) + '\n')
        my_text.insert(END , "          Name : " + furniture[5] + '\n')
        my_text.insert(END , "          Company : " + furniture[2] + '\n')
        my_text.insert(END , "          Price : " + str(furniture[3]) + '\n')
        my_text.insert(END , "          Description : " + furniture[4] + '\n')
        my_text.insert(END , "          Interest Rate : " + str(furniture[8]) + '\n')
        ex = "SELECT review FROM feedbacks WHERE type = %s"
        va = (furniture[5],)
        my_cursor.execute(ex , va)
        rel = my_cursor.fetchall()
        my_text.insert(END , "          Reviews :\n")
        for feedback in rel:
            my_text.insert(END , "          " + feedback[0] + "\n")
            pass
        my_text.insert(END , "\n\n")
        pass


def AdminPage(self):
    self.destroy()
    admin = Tk()
    admin.geometry("900x550")
    admin.title("Admin page")
    leftBg = "#9cd083"
    rightBg = "#a1cfce"
    rightFrame = Frame(admin , width = 50 , height= 100 , background = rightBg)
    leftFrame = Frame(admin , width = 50 , height = 100 , background = leftBg)
    leftFrame.grid(row = 0 , column = 0 , sticky = "nsew")
    rightFrame.grid(row = 0 , column = 1 , sticky = "nsew")
    admin.grid_columnconfigure(0 , weight = 1)
    admin.grid_columnconfigure(1 , weight = 1)
    admin.grid_rowconfigure(0 , weight = 1)
    leftFrame.grid_propagate(False)
    leftFrame.pack_propagate(False)
    rightFrame.grid_propagate(False)
    rightFrame.pack_propagate(False)

    exe = "SELECT id FROM furnitures WHERE days_rented >= %s"
    va = (365,)
    my_cursor.execute(exe, va)
    res = my_cursor.fetchall()

    if(len(res) > 0):
        for id in res[0]:
            ex = "UPDATE furnitures SET days_rented = days_rented - %s , price = price * %s WHERE id = %s"
            va = (365, 0.9, id)
            my_cursor.execute(ex, va)


    mydb.commit()




    def createCustomer():
        Signup()
        pass

    def deleteCustomer():
        delcustomer = Tk()
        delcustomer.geometry("650x200")
        delcustomer.title("Delete a customer account")
        delcustomer.config(bg="#ffdc73")
        l1 = Label(delcustomer , text = "Enter the username of the customer to delete : ", bg="#ffdc73", font=("Courier new", 13))
        l1.grid(row = 0 , column = 1, padx=10, pady=10)
        e1 = Entry(delcustomer, relief=FLAT)
        e1.grid(row = 0 , column = 2)

        def removeCustomer():
            user = e1.get()
            exe = "SELECT * FROM customers WHERE username = %s"
            val = (user , )
            my_cursor.execute(exe , val)
            res = my_cursor.fetchall()
            if len(res) == 0:
                messagebox.showwarning("ALERT !" , "NO such user found !")
            elif res[0][5] != 0:
                messagebox.showwarning("Warning","User Cannot be Deleted !")
                testnotdeleteduser(user)
            else:
                exe = "DELETE FROM customers WHERE username = %s"
                my_cursor.execute(exe , val)
                mydb.commit()
                messagebox.showinfo("ALERT !" , "USER DELETED !")
                testdeleteuser(user)
            pass

        b = Button(delcustomer , text = "Delete !" , command = removeCustomer, bg="red", fg="white", font=("Arial", 13, "bold"))
        b.grid(row = 1 , column = 0 , columnspan = 2)
        pass

    def seeNotifications():
        # get distinct type of furniture put it in the list
        # do a count query with each item in the list
        # if any count falls below threshold display it
        see = Tk()
        see.geometry("500x500")
        see.title("Notifications")
        text_scroll = Scrollbar(see)
        text_scroll.pack(side = RIGHT , fill = Y)
        my_text = Text(see , width = 100 , height = 120 , font = ('Comic sans ms' , 10) , yscrollcommand = text_scroll.set, spacing1=8)
        my_text.pack(pady = 10 , padx = 10)
        text_scroll.config(command = my_text.yview)
        exe = "SELECT DISTINCT type FROM furnitures"
        my_cursor.execute(exe)
        res = my_cursor.fetchall()
        # print("REsult : " , res)
        for t in res:
            ex = "SELECT COUNT(type) FROM furnitures WHERE rented = %s AND type = %s"
            # print("t = " , t[0])
            v = (0 , t[0])
            my_cursor.execute(ex , v)
            r = my_cursor.fetchall()
            # print("r = " , r)
            if r[0][0]<5:
                my_text.insert(END , "          " + t[0] + " type of furniture is low !\n")
            pass
        pass

    def checkInvestmentAndProfit():
        inv = Tk()
        inv.geometry("1360x678")
        leftBg = "#FFA400"
        rightBg = "#9ACD32"
        fram1 = Frame(inv , background = leftBg)
        fram2 = Frame(inv , background = rightBg)
        fram1.grid(row = 0 , column = 0 , sticky = "nsew")
        fram2.grid(row = 0 , column = 1 , sticky = "nsew")
        inv.grid_columnconfigure(0 , weight = 3)
        inv.grid_columnconfigure(1 , weight = 4)
        inv.grid_rowconfigure(0 , weight = 1)
        fram1.grid_propagate(False)
        fram2.grid_propagate(False)
        # fram1.pack_propagate(False)
        # fram2.pack_propagate(False)
        exe = "SELECT SUM(investment) FROM admins"
        my_cursor.execute(exe)
        investment = my_cursor.fetchall()
        # print(investment[0][0])
        l4 = Label(fram1 , text = "INVESTMENT = " + str(investment[0][0]), bg=leftBg, font=("Century gothic", 13, "bold"))
        l4.grid(row=0, column=0, pady=200, padx=25)
        testinvestment(float(investment[0][0]))
        exe = "SELECT SUM(profit) FROM admins"
        my_cursor.execute(exe)
        pro = my_cursor.fetchall()
        # print(pro[0][0])
        l5 = Label(fram1 , text = "Profit = " + str(pro[0][0]), bg=leftBg, font=("Century gothic", 13, "bold"))
        testprofit(float(pro[0][0]))
        l5.grid(row=1, column=0, padx=25)
        exe = "SELECT profit , investment FROM graph"
        my_cursor.execute(exe)
        rel = my_cursor.fetchall()
        x = []
        y = []
        for tup in rel:
            x.append(tup[1])
            y.append(tup[0])
        fig = Figure(figsize = (8,6),dpi = 100)
        canvas = FigureCanvasTkAgg(fig, master = fram2)
        plot1 = fig.add_subplot(111)
        plot1.plot(x,y)
        plot1.set_xlabel("investment")
        plot1.set_ylabel("profit")
        canvas.draw()
        canvas.get_tk_widget().pack(pady = 30 , padx = 8)
        pass

    def changePrice():
        change = Tk()
        change.geometry("600x400")
        change.title("Change price of an item")
        changeBg = "#ff9a5b"
        change.config(bg=changeBg)
        l2 = Label(change, text = "Enter the type of the furniture for changing price: ", font=("Times New Roman", 15), bg=changeBg)
        l2.grid(row = 0 , column = 0, padx=10, pady=10)
        e2 = Entry(change, relief=FLAT)
        e2.grid(row = 0 , column = 1)
        l3 = Label(change , text = "Enter the new price :", font=("Times New Roman", 15), bg=changeBg)
        l3.grid(row = 1 , column = 0, padx=10, pady=10)
        e3 = Entry(change, relief=FLAT)
        e3.grid(row = 1 , column = 1)

        def alter():
            typ = e2.get()
            np = e3.get()
            ex = "SELECT * FROM furnitures WHERE type = %s"
            va = (typ,)
            my_cursor.execute(ex , va)
            res = my_cursor.fetchall()
            if len(res) == 0:
                messagebox.showerror("Error", "No furniture of this type found !")
                return
            exe = "UPDATE furnitures SET price = %s WHERE type = %s"
            va = (np , typ)
            my_cursor.execute(exe , va)
            mydb.commit()
            testchangeprice(str(typ), float(np))
            messagebox.showinfo("Information", "Price Changed")
            pass

        b2 = Button(change , command = alter , text = "Alter", bg="red", font=("Arial", 16, "bold"), fg="white")
        b2.grid(row = 2 , column = 1, pady=10)
        
        pass

    def reAddition():
        readd = Tk()
        readd.geometry("1000x500")
        readd.title("Verify Returns")
        rightBg = "#ADFF2F"
        leftBg = "#DEB887"
        rightFrame1 = Frame(readd , width = 50 , height= 100 , background = rightBg)
        leftFrame1 = Frame(readd , width = 50 , height = 100 , background = leftBg)
        leftFrame1.grid(row = 0 , column = 0 , sticky = "nsew")
        rightFrame1.grid(row = 0 , column = 1 , sticky = "nsew")
        readd.grid_columnconfigure(0 , weight = 2)
        readd.grid_columnconfigure(1 , weight = 3)
        readd.grid_rowconfigure(0 , weight = 1)
        leftFrame1.grid_propagate(False)
        leftFrame1.pack_propagate(False)
        rightFrame1.grid_propagate(False)
        rightFrame1.pack_propagate(False)

        text_scroll1 = Scrollbar(rightFrame1)
        text_scroll1.pack(side = RIGHT , fill = Y)
        my_text1 = Text(rightFrame1 , width = 100 , height = 120 , font = ('Comic sans ms' , 10) , yscrollcommand = text_scroll1.set, spacing1=8)
        my_text1.pack(pady = 10 , padx = 10)
        text_scroll1.config(command = my_text1.yview)

        ex = "SELECT * FROM current_returns"
        my_cursor.execute(ex)
        result = my_cursor.fetchall()
        for query in result:
            my_text1.insert(END , "         Furniture id = " + str(query[2]) + " Username = " + str(query[1]) + "\n")

        l1 = Label(leftFrame1 , text = "Enter the furniture id : ", font=("Eras Demi ITC", 12), bg=leftBg)
        e1 = Entry(leftFrame1)
        l1.grid(row = 0 , column = 0, padx=10, pady=10)
        e1.grid(row = 0 , column = 1)
        l2 = Label(leftFrame1 , text = "Enter the username : ", font=("Eras Demi ITC", 12), bg=leftBg)
        e2 = Entry(leftFrame1)
        l2.grid(row = 1 , column = 0, padx=10, pady=10)
        e2.grid(row = 1 , column = 1)
        v1 = StringVar(leftFrame1 , "1")
        R1 = Radiobutton(leftFrame1 , text = "Damaged" , variable = v1 , value = "1", bg=leftBg)
        R2 = Radiobutton(leftFrame1 , text = "Not Damaged" , variable = v1 , value ="2", bg=leftBg)
        R1.grid(row = 2 , column = 0, padx=10, pady=10)
        R2.grid(row = 2 , column = 1, padx=10, pady=10)


        def completereturn():
            fur_id = e1.get()
            user = e2.get()
            if v1.get() == "1" :
                ex = "SELECT price FROM furnitures WHERE id = %s"
                va = (fur_id,)
                my_cursor.execute(ex , va)
                price = my_cursor.fetchall()
                ex = "SELECT amountdue FROM customers WHERE username = %s"
                va = (user,)
                my_cursor.execute(ex , va)
                oldamount = my_cursor.fetchall()
                ex = "UPDATE customers SET amountdue = %s WHERE username = %s"
                va = (oldamount[0][0] + price[0][0] , user)
                my_cursor.execute(ex , va)
                mydb.commit()
                ex = "DELETE FROM furnitures WHERE id = %s"
                va = (fur_id , )
                my_cursor.execute(ex , va)
                mydb.commit()
                messagebox.showinfo("Information", "Furniture Deleted !")
                testfurnituredelete(int(fur_id))
                pass
            else:
                ex = "UPDATE furnitures SET rented = %s WHERE id = %s"
                va = (0 , fur_id )
                my_cursor.execute(ex , va)
                mydb.commit()
                messagebox.showinfo("Information", "Furniture Added to the Inventory !")
                testreadditionfurniture(int(fur_id))
                pass
            ex = "DELETE FROM current_returns WHERE username = %s AND furniture_id = %s"
            va = (user , fur_id)
            my_cursor.execute(ex , va)
            mydb.commit()
            ex = "SELECT * FROM current_returns"
            my_cursor.execute(ex)
            result = my_cursor.fetchall()
            my_text1.delete("1.0",END)
            for query in result:
                my_text1.insert(END , "Furniture id = " + str(query[2]) + " Username = " + str(query[1]) + "\n")
            pass

        b1 = Button(leftFrame1 , text = "Complete the return !" , command = completereturn, bg="#B22222", font=("Arial", 13, "bold"), fg="white")
        b1.grid(row = 3 , column = 0 , columnspan = 2)
        pass
    
    btnBg = "#ffe08d"
    createcustomeraccountbutton = Button(leftFrame , text = "Create a customer account" , width = 30 , command = createCustomer, bg=btnBg,fg="black",font=("Century gothic", 13))
    createcustomeraccountbutton.pack(pady=(50,10))
    deletecustomeraccountbutton = Button(leftFrame , text = "Delete a customer account" , width = 30 , command = deleteCustomer, bg=btnBg,fg="black",font=("Century gothic", 13))
    deletecustomeraccountbutton.pack(pady=10)
    notificationsbutton = Button(leftFrame , text = "See the notifications" , width = 30 , command = seeNotifications, bg=btnBg,fg="black",font=("Century gothic", 13))
    notificationsbutton.pack(pady=10)
    investmentprofitbutton = Button(leftFrame , text = "Investment and profit" , width = 30 , command = checkInvestmentAndProfit, bg=btnBg,fg="black",font=("Century gothic", 13))
    investmentprofitbutton.pack(pady=10)
    changeprice = Button(leftFrame , text = "Change price" , width = 30 , command = changePrice, bg=btnBg,fg="black",font=("Century gothic", 13))
    changeprice.pack(pady=10)
    readdition = Button(leftFrame , text = "Check returns" , width = 30 , command = reAddition, bg=btnBg,fg="black",font=("Century gothic", 13))
    readdition.pack(pady=10)

    def adminlogoutcommand():
        Login(admin)

    adminlogout = Button(leftFrame , text = "Log Out" , width = 30 , command = adminlogoutcommand, bg=btnBg,fg="black",font=("Century gothic", 13))
    adminlogout.pack(pady=10)

    notifl = Label(rightFrame , text = "Add new funiture to inventory", bg=rightBg, relief=FLAT, font=("Comic sans ms", 13), fg="red")
    notifl.grid(row=0, column=0, columnspan=2, padx=30)
    namel =  Label(rightFrame , text = "Name", bg=rightBg, relief=FLAT, font=("Comic sans ms", 13))
    namel.grid(row = 1 , column = 0, padx=30, pady=10)
    type = Label(rightFrame , text = "Type", bg=rightBg, relief=FLAT, font=("Comic sans ms", 13))
    type.grid(row = 2 , column = 0, padx=30, pady=10)
    price = Label(rightFrame , text = "Price", bg=rightBg, relief=FLAT, font=("Comic sans ms", 13))
    price.grid(row = 3 , column = 0, padx=30, pady=10)
    interestrate = Label(rightFrame , text = "Interest Rate", bg=rightBg, relief=FLAT, font=("Comic sans ms", 13))
    interestrate.grid(row = 4 , column = 0, padx=30, pady=10)
    description = Label(rightFrame , text = "Description", bg=rightBg, relief=FLAT, font=("Comic sans ms", 13))
    description.grid(row = 5 , column = 0, padx=30, pady=10)
    companyl = Label(rightFrame , text = "Company", bg=rightBg, relief=FLAT, font=("Comic sans ms", 13))
    companyl.grid(row = 6 , column = 0, padx=40, pady=10)

    nameentry =  Entry(rightFrame, relief=FLAT)
    nameentry.grid(row = 1 , column = 1)
    typeentry = Entry(rightFrame, relief=FLAT)
    typeentry.grid(row = 2 , column = 1)
    priceentry = Entry(rightFrame , relief=FLAT)
    priceentry.grid(row = 3 , column = 1)
    interestrateentry = Entry(rightFrame, relief=FLAT)
    interestrateentry.grid(row = 4 , column = 1)
    descriptionentry = Entry(rightFrame, relief=FLAT)
    descriptionentry.grid(row = 5 , column = 1)
    companyentry = Entry(rightFrame, relief=FLAT)
    companyentry.grid(row = 6 , column = 1)

    global filepath
    filepath = ""

    def openImage():
        rightFrame.filename= filedialog.askopenfilename(initialdir = os.path.join(os.getcwd() , "images") , title = 'select an image' , filetypes = (("jpg files" , "*.jpg"),))
        global filepath
        filepath = rightFrame.filename
        pass

    def add_furniture():
        name = nameentry.get()
        company = companyentry.get()
        type = typeentry.get()
        interestrate = (interestrateentry.get())
        price = (priceentry.get())
        description = descriptionentry.get()
        date = dt.today().strftime('%Y-%m-%d')
        # print(filepath , date)
        if name and type and interestrate and price and description and filepath:
            interestrate = float(interestrate)
            price = float(price)
            exe = 'INSERT INTO furnitures (name , company , price , description , type , rented , photo , interest_rate , date_started) VALUES (%s , %s , %s , %s , %s , %s , %s , %s ,%s)'
            values = (name , company , price , description , type , 0 , filepath , interestrate , date)
            my_cursor.execute(exe , values)
            mydb.commit()
            exe = "UPDATE admins SET investment = investment + %s WHERE username = %s"
            va = (price , user_id)
            my_cursor.execute(exe , va)
            mydb.commit()
            exe = "SELECT profit FROM graph WHERE id = (SELECT max(id) FROM graph)"
            my_cursor.execute(exe)
            oldprofit = my_cursor.fetchall()
            # print("oldprofit " , oldprofit)
            exe = "SELECT investment FROM graph WHERE id = (SELECT max(id) FROM graph)"
            my_cursor.execute(exe)
            oldinvestment = my_cursor.fetchall()
            # print("oldinvestment " , oldinvestment)
            exe = "INSERT INTO graph (profit , investment) VALUES (%s , %s)"
            va = (float(oldprofit[0][0]), float(oldinvestment[0][0])+float(price))
            my_cursor.execute(exe , va)
            mydb.commit()
            messagebox.showinfo("Information", "Furniture Added !")
            nameentry.delete(0,END)
            companyentry.delete(0,END)
            typeentry.delete(0,END)
            interestrateentry.delete(0,END)
            priceentry.delete(0,END)
            descriptionentry.delete(0,END)
            testaddfuniture(type, filepath)
        else:
            messagebox.showwarning("ALERT !" , "Fill all the fields")
        pass

    chooseimage = Button(rightFrame , text = "Choose Image" , command = openImage , width = 20, bg="#fd759f", font=("Arial", 13, "bold"))
    chooseimage.grid(row = 7 , column = 0, padx=30, pady=10, columnspan=2)

    add = Button(rightFrame , text = "Add Furniture" , width = 30 , command = add_furniture, bg="#60e84e", font=("Arial", 13, "bold"))
    add.grid(row = 8 , column = 0, padx=30, pady=10, columnspan=2)

# make a back button here!

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
                CustomerPage(login)
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
                AdminPage(login)

        else:
            messagebox.showwarning("ALERT !" , "All fields should be filled !")

    usernameentry = Entry(login, relief=FLAT)
    usernameentry.grid(row = 1 , column = 1)
    passwordentry = Entry(login , show ='*', relief=FLAT)
    passwordentry.grid(row = 2 , column = 1)
    global lb
    lb = Image.open(os.path.join(os.getcwd() , "images\\loginBtn.jpg"))
    lb = lb.resize((150, 45))
    lb = ImageTk.PhotoImage(lb)
    completelogin = Button(login ,image = lb, command = adduser, bg=loginBg, relief=FLAT)
    completelogin.grid(row = 4 , column = 0, columnspan = 2, padx=(70,0))


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


if __name__ == '__main__':
    root = Tk()
    root.geometry("1580x800")
    root.title("FRSS Pvt Ltd")
    mydb = mysql.connector.connect(host = "localhost",
								user = "root",
								passwd = "Mysql_20010316",
                                database = "frss",
                                port = 3306,)
    
    global my_cursor
    my_cursor = mydb.cursor()
    my_cursor.execute("CREATE DATABASE IF NOT EXISTS frss")
    # my_cursor.execute("SHOW DATABASES")
    # for db in my_cursor:
        # print(db)

    my_cursor.execute("CREATE TABLE IF NOT EXISTS customers (name VARCHAR(255) NOT NULL,username VARCHAR(255) PRIMARY KEY,password VARCHAR(255) NOT NULL,address VARCHAR(255) NOT NULL, phonenumber VARCHAR(255) NOT NULL,amountdue DECIMAL(8,2) DEFAULT 0,numberoforders INT(10))")
    my_cursor.execute("CREATE TABLE IF NOT EXISTS admins (name VARCHAR(255) NOT NULL,username VARCHAR(255) PRIMARY KEY,password VARCHAR(255) NOT NULL,address VARCHAR(255) NOT NULL, phonenumber VARCHAR(255) NOT NULL,profit DECIMAL(8,2) DEFAULT 0,investment DECIMAL(8,2) DEFAULT 0)")
    my_cursor.execute("CREATE TABLE IF NOT EXISTS furnitures (id INT auto_increment primary key, name VARCHAR(255) NOT NULL , company VARCHAR(255) NOT NULL , price DECIMAL(8,2) , description VARCHAR(255) NOT NULL , type VARCHAR(255) NOT NULL , rented INT , photo VARCHAR(255) NOT NULL , interest_rate DECIMAL(4,2) , date_started DATE , date_ended DATE , username VARCHAR(255) , FOREIGN KEY (username) REFERENCES customers(username) , days_rented INT DEFAULT 0)")
    my_cursor.execute("CREATE TABLE IF NOT EXISTS past_orders (id INT auto_increment primary key , username VARCHAR(255) , furniture_id INT)")
    my_cursor.execute("CREATE TABLE IF NOT EXISTS feedbacks (id INT auto_increment primary key , type VARCHAR(255), review VARCHAR(255))")
    my_cursor.execute("CREATE TABLE IF NOT EXISTS current_returns (id INT auto_increment primary key , username VARCHAR(255), furniture_id INT)")
    my_cursor.execute("CREATE TABLE IF NOT EXISTS graph (id INT auto_increment primary key , profit DECIMAL(8,2) DEFAULT 0 , investment DECIMAL(8,2) DEFAULT 0)")
    
    # ex = "INSERT INTO graph (profit, investment) VALUES (%s, %s)"
    # va = (0,0)
    # my_cursor.execute(ex, va)
    # mydb.commit()

    # my_cursor.execute("SELECT * FROM customers")
    # print(my_cursor.description)
    wallpaper_path = os.path.join(os.getcwd() , "images\\Wp1.jpg")
    background_image = Image.open(wallpaper_path)
    background_image = background_image.resize((1580,800))
    background_image = ImageTk.PhotoImage(background_image)
    background_label = Label(root , image = background_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    loginbutton = Button(root, text = 'Login', command = lambda : Login(root), height=2, width=40, font=("Comic sans ms", 12), padx=10, pady=0.001)
    loginbutton.pack(side= LEFT, padx=230)
    signupbutton = Button(root, text = 'Sign Up', command = Signup, height=2, width=40, font=("Comic sans ms", 12), padx=10, pady=0.001)
    signupbutton.pack(side= LEFT)
    root.mainloop()
    unittest.main()