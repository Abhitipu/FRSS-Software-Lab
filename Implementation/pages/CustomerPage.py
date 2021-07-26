from tkinter import *
from pages import my_cursor, user_id, pass_word, is_admin, mydb
from pages import Login
from tkinter import messagebox, filedialog
import math

import sys
sys.path.append('..')
from tests import *

from PIL import ImageTk, Image

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

