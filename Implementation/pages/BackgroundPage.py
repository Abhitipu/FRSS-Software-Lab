from tkinter import *
from PIL import ImageTk, Image
import unittest
import os
from pages import Login, Signup

def BackgroundPage(root):
    root.geometry("1580x800")
    root.title("FRSS Pvt Ltd")
    wallpaper_path = os.path.join(os.getcwd() , "images\\Wp1.jpg")
    background_image = Image.open(wallpaper_path)
    background_image = background_image.resize((1580,800))
    background_image = ImageTk.PhotoImage(background_image)
    background_label = Label(root , image = background_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    loginbutton = Button(root, text = 'Login', command = lambda : Login.Login(root), height=2, width=40, font=("Comic sans ms", 12), padx=10, pady=0.001)
    loginbutton.pack(side= LEFT, padx=230)
    signupbutton = Button(root, text = 'Sign Up', command = Signup.Signup, height=2, width=40, font=("Comic sans ms", 12), padx=10, pady=0.001)
    signupbutton.pack(side= LEFT)
    root.mainloop()
    unittest.main()