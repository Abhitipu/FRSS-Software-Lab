from tkinter import *
from pages import my_cursor, mydb, user_id, is_admin
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
from datetime import datetime as dt
from pages import Signup
from pages import Login

import sys
sys.path.append('..')
from tests import *

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
        Signup.Signup()

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


        b = Button(delcustomer , text = "Delete !" , command = removeCustomer, bg="red", fg="white", font=("Arial", 13, "bold"))
        b.grid(row = 1 , column = 0 , columnspan = 2)

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


        b2 = Button(change , command = alter , text = "Alter", bg="red", font=("Arial", 16, "bold"), fg="white")
        b2.grid(row = 2 , column = 1, pady=10)
        

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
    
            else:
                ex = "UPDATE furnitures SET rented = %s WHERE id = %s"
                va = (0 , fur_id )
                my_cursor.execute(ex , va)
                mydb.commit()
                messagebox.showinfo("Information", "Furniture Added to the Inventory !")
                testreadditionfurniture(int(fur_id))
    
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


        b1 = Button(leftFrame1 , text = "Complete the return !" , command = completereturn, bg="#B22222", font=("Arial", 13, "bold"), fg="white")
        b1.grid(row = 3 , column = 0 , columnspan = 2)
    
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
        Login.Login(admin)

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

    chooseimage = Button(rightFrame , text = "Choose Image" , command = openImage , width = 20, bg="#fd759f", font=("Arial", 13, "bold"))
    chooseimage.grid(row = 7 , column = 0, padx=30, pady=10, columnspan=2)

    add = Button(rightFrame , text = "Add Furniture" , width = 30 , command = add_furniture, bg="#60e84e", font=("Arial", 13, "bold"))
    add.grid(row = 8 , column = 0, padx=30, pady=10, columnspan=2)
