import mysql.connector

try:
    mydb = mysql.connector.connect(host = "localhost",
                                user = "root",
                                passwd = "Mysql_20010316",
                                database = "frss",
                                port = 3306,)
except Exception as e:
    print(f"Could not connect to database! {e}")
    # maybe show a messagebox
finally:
    my_cursor = mydb.cursor()
    my_cursor.execute("CREATE DATABASE IF NOT EXISTS frss")
    user_id = ""
    pass_word = ""
    is_admin = False

    my_cursor.execute("CREATE TABLE IF NOT EXISTS customers (name VARCHAR(255) NOT NULL,username VARCHAR(255) PRIMARY KEY,password VARCHAR(255) NOT NULL,address VARCHAR(255) NOT NULL, phonenumber VARCHAR(255) NOT NULL,amountdue DECIMAL(8,2) DEFAULT 0,numberoforders INT(10))")
    my_cursor.execute("CREATE TABLE IF NOT EXISTS admins (name VARCHAR(255) NOT NULL,username VARCHAR(255) PRIMARY KEY,password VARCHAR(255) NOT NULL,address VARCHAR(255) NOT NULL, phonenumber VARCHAR(255) NOT NULL,profit DECIMAL(8,2) DEFAULT 0,investment DECIMAL(8,2) DEFAULT 0)")
    my_cursor.execute("CREATE TABLE IF NOT EXISTS furnitures (id INT auto_increment primary key, name VARCHAR(255) NOT NULL , company VARCHAR(255) NOT NULL , price DECIMAL(8,2) , description VARCHAR(255) NOT NULL , type VARCHAR(255) NOT NULL , rented INT , photo VARCHAR(255) NOT NULL , interest_rate DECIMAL(4,2) , date_started DATE , date_ended DATE , username VARCHAR(255) , FOREIGN KEY (username) REFERENCES customers(username) , days_rented INT DEFAULT 0)")
    my_cursor.execute("CREATE TABLE IF NOT EXISTS past_orders (id INT auto_increment primary key , username VARCHAR(255) , furniture_id INT)")
    my_cursor.execute("CREATE TABLE IF NOT EXISTS feedbacks (id INT auto_increment primary key , type VARCHAR(255), review VARCHAR(255))")
    my_cursor.execute("CREATE TABLE IF NOT EXISTS current_returns (id INT auto_increment primary key , username VARCHAR(255), furniture_id INT)")
    my_cursor.execute("CREATE TABLE IF NOT EXISTS graph (id INT auto_increment primary key , profit DECIMAL(8,2) DEFAULT 0 , investment DECIMAL(8,2) DEFAULT 0)")
    
    # insert into graph if no points are found
    my_cursor.execute("SELECT * from graph")
    points = my_cursor.fetchall()
    if len(points) == 0:
        ex = "INSERT INTO graph (profit, investment) VALUES (%s, %s)"
        va = (0,0)
        my_cursor.execute(ex, va)
        mydb.commit()

    from pages import Signup
    from pages import AdminPage
    from pages import CustomerPage
    from pages import Login
    from pages import BackgroundPage