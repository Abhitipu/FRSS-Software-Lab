import mysql.connector

def testsignup(username):
    ex = "SELECT * FROM customers WHERE username = %s"
    va = (username,)
    my_cursor1.execute(ex, va)
    res = my_cursor1.fetchall()
    ex = "SELECT * FROM admins WHERE username = %s"
    va = (username,)
    my_cursor1.execute(ex, va)
    re = my_cursor1.fetchall()
    if len(re) > 0 or len(res) > 0:
        print("User SIGN UP : PASSED")
    else:
        print("USER SIGN UP : FAIL")

def testdeleteuser(username):
    ex = "SELECT * FROM customers WHERE username = %s"
    va = (username,)
    my_cursor1.execute(ex, va)
    res = my_cursor1.fetchall()
    if len(res) == 0:
        print("User DELETE : PASSED")
    else:
        print("USER DELETE : FAILED")

def testnotdeleteduser(username):
    ex = "SELECT * FROM customers WHERE username = %s"
    va = (username,)
    my_cursor1.execute(ex, va)
    res = my_cursor1.fetchall()
    if len(res) == 0:
        print("User DELETE WITH AMOUNT DUE : FAILED")
    else:
        print("USER DELETE WITH AMOUNT DUE : PASSED")

def testaddfuniture(type, file):
    ex = "SELECT * FROM furnitures WHERE type = %s AND photo = %s"
    va = (type , file)
    my_cursor1.execute(ex, va)
    res = my_cursor1.fetchall()
    if len(res) < 1:
        print("ADD FURNITURE : FAILED here")
        return
    else:
        if res[0][5] == type:
            print("ADD FURNITURE : PASSED")
        else:
            print("ADD FURNITURE : FAILED")
        if res[0][7] == file:
            print("CORRECT PHOTO ADDED : PASSED")
        else:
            print("CORRECT PHOTO ADDED : FAILED")

def testinvestment(inv):
    exe = "SELECT SUM(investment) FROM admins"
    my_cursor1.execute(exe)
    investment = my_cursor1.fetchall()
    if float(investment[0][0]) == inv:
        print("INVESTMENT TEST : PASSED")
        pass
    else:
        print("INVESTMENT TEST : FAILED")

def testprofit(pro):
    exe = "SELECT SUM(profit) FROM admins"
    my_cursor1.execute(exe)
    profit = my_cursor1.fetchall()
    if float(profit[0][0]) == pro:
        print("PROFIT TEST : PASSED")
        pass
    else:
        print("PROFIT TEST : FAILED")
    pass


def testchangeprice(type, newprice):
    exe = "SELECT price FROM furnitures WHERE type = %s"
    va = (type,)
    my_cursor1.execute(exe, va)
    res = my_cursor1.fetchall()
    if(int(res[0][0]) == int(newprice)):
        print("CHANGE PRICE TEST : PASSED")
    else:
        print("CHANGE PRICE TEST : FAILED")


def testfurnituredelete(fur_id):
    exe = "SELECT * FROM furnitures WHERE id = %s"
    va = (fur_id,)
    my_cursor1.execute(exe, va)
    res = my_cursor1.fetchall()
    if len(res) > 0:
        print("DELETE DAMAGED FURNITURE : FAILED")
    else:
        print("DELETE DAMAGED FURNITURE : PASSED")

def testreadditionfurniture(fur_id):
    exe = "SELECT rented FROM furnitures WHERE id = %s"
    va = (fur_id,)
    my_cursor1.execute(exe, va)
    res = my_cursor1.fetchall()
    if (res[0][0]) != 0:
        print("READDITION FURNITURE : FAILED")
    else:
        print("READDITION FURNITURE : PASSED")

def testcustomeramountdue(username, amt):
    ex = "SELECT amountdue FROM customers WHERE username = %s"
    va = (username , )
    my_cursor1.execute(ex , va)
    res = my_cursor1.fetchall()[0][0]
    if amt != res:
        print("AMOUNT DUE TEST : FAILED")
    else:
        print("AMOUNT DUE TEST : PASSED")

def testpaymentdone(username, amount):
    ex = "SELECT amountdue FROM  customers WHERE username = %s"
    va = (username, )
    my_cursor1.execute(ex , va)
    res = my_cursor1.fetchall()
    if res[0][0] != amount:
        print("PAYMENT DONE : PASSED")
    else:
        print("PAYMENT DONE : FAILED")

def testfeedbackinsert(typ, feed):
    ex = "SELECT review FROM feedbacks WHERE type = %s"
    va = (typ ,)
    my_cursor1.execute(ex , va)
    res = my_cursor1.fetchall()
    if res[0][0] != feed:
        print("FEEDBACK INSERTED : FAILED")
    else:
        print("FEEDBACK INSERTED : PASSED")

def testcustomerlogin(username, user_id):
    if username == user_id:
        print("CUSTOMER LOGIN : PASSED")
    else:
        print("CUSTOMER LOGIN : FAILED")

def testadminlogin(username, user_id):
    if username == user_id:
        print("ADMIN LOGIN : PASSED")
    else:
        print("ADMIN LOGIN : FAILED")

def testreturnadded(fur_id):
    ex = "SELECT * FROM current_returns WHERE furniture_id = %s"
    va = (int(fur_id),)
    my_cursor1.execute(ex , va)
    res = my_cursor1.fetchall()
    if len(res) < 1:
        print("RETURN INITIATED : FAILED")
    else:
        print("RETURN INTIATED : PASSED")

try:
    mydb1 = mysql.connector.connect(host = "localhost",
                                    user = "root",
                                    passwd = "Mysql_20010316",
                                    database = "frss",
                                    port = 3306,)
except Exception as e:
    print(f"Could not connect to database! {e}")
finally:
    global my_cursor1
    my_cursor1 = mydb1.cursor()