from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image


def login():
    if username_entry.get() == "" or password_entry.get() == "":
        messagebox.showerror("Error", "Please enter your username and password")
    elif username_entry.get() == "Arif" and password_entry.get() == "1234":
        messagebox.showinfo("Success", "Login successful")
        root.destroy()
        import dashboard
    else:
        messagebox.showerror("Error", "Wrong username or password")


root = Tk()
root.geometry('1300x700+0+0')
root.resizable(False, False)
root.config(bg='#D7E1A3')
root.title('Login')
img=ImageTk.PhotoImage(Image.open('login.png'))
image_label = Label(root, image=img)
image_label.pack()
heading_label=Label(root,text='Management System Login',font=('Arial',20,'bold'),bg='#E3ECB9',fg='black')
heading_label.place(x=480,y=10)

num_label = Label(root, text="Username :", font=('Arial',20,'bold'),bg='#715A29',fg='white', width=10)
num_label.place(x=300,y=150)

username_entry=Entry(root, font=('Arial',20,'bold'),bg='#D7E1A3', width=15)
username_entry.place(x=550,y=150)

pass_label = Label(root, text="Password :", font=('Arial',20,'bold'),bg='#715A29',fg='white', width=10)
pass_label.place(x=300,y=225)

password_entry=Entry(root, font=('Arial',20,'bold'),bg='#D7E1A3',width=15, show='*')
password_entry.place(x=550,y=225)

login_button=Button(root, text='Login',font=('Arial',15,'bold'), bg='#D7E1A3', cursor='hand2',
                    command=login)
login_button.place(x=615,y=310)

root.mainloop()
