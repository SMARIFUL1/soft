from tkinter import *
from employees import employee_form

## FunctionalityPart

#GUI part
window = Tk()

window.title('Dashboard')
window.geometry(
    '1300x700+0+0')  # here 0+0 fixes the window appearance on a certain position on the screen(left upper corner)
window.resizable(False, False)  #resize of window is disabled
window.config(bg='green')

bg_img = PhotoImage(file='ege.png', height=80, width=100, )
titleLabel = Label(window, text=' Management System',
                   image=bg_img, compound=LEFT,
                   font=('times new roman', 40, 'bold'),
                   bg='blue', fg='white',
                   anchor=W, padx=5)
titleLabel.place(x=0, y=0, relwidth=1)

logout_btn = Button(window, text='Logout', font=('times new roman', 20, 'bold'), fg='black')
logout_btn.place(x=1100, y=10)

subtitleLabel = Label(window, text='Welcome Users\t\t Date:1.12.2024\t\t Time:12:12:59 pm',
                      font=('times new roman', 15), bg='gray', fg='white', )
subtitleLabel.place(x=0, y=70, relwidth=1)

leftframe = Frame(window)
leftframe.place(x=0, y=101, width=200, height=655)
left_img = PhotoImage(file='ege1.png', height=150, width=100, )
img_label = Label(leftframe, image=left_img)
img_label.pack()

## MENU
menu_label = Label(leftframe, text='Menu', font=('times new roman', 20), bg='gray', fg='black')
menu_label.pack(fill=X)

## Employee_button
empl_icon = PhotoImage(file='employee.png', height=40, width=40, )
employee_btn = Button(leftframe, image=empl_icon, compound=LEFT,
                      text=' Employees', font=('times new roman', 20, 'bold'), fg='black', anchor=W, padx=5,
                      command=lambda: employee_form(window))
employee_btn.pack(fill=X)

## supplier_button
supp_icon = PhotoImage(file='supplier.png', height=40, width=40, )
supplier_btn = Button(leftframe, image=supp_icon, compound=LEFT,
                      text=' Suppliers', font=('times new roman', 20, 'bold'), fg='black', anchor=W, padx=5)
supplier_btn.pack(fill=X)

## Category_button
cat_icon = PhotoImage(file='product.png', height=40, width=40, )
category_btn = Button(leftframe, image=cat_icon, compound=LEFT,
                      text=' Category', font=('times new roman', 20, 'bold'), fg='black', anchor=W, padx=5)
category_btn.pack(fill=X)

## product_button
prod_icon = PhotoImage(file='product.png', height=40, width=40, )
product_btn = Button(leftframe, image=supp_icon, compound=LEFT,
                     text=' Products', font=('times new roman', 20, 'bold'), fg='black', anchor=W, padx=5)
product_btn.pack(fill=X)

## sales_button
sale_icon = PhotoImage(file='sales.png', height=40, width=40, )
sales_btn = Button(leftframe, image=sale_icon, compound=LEFT,
                   text=' Sales', font=('times new roman', 20, 'bold'), fg='black', anchor=W, padx=5)
sales_btn.pack(fill=X)

## exit_button
exit_icon = PhotoImage(file='employee.png', height=40, width=40, )
exit_btn = Button(leftframe, image=exit_icon, compound=LEFT,
                  text=' Exit', font=('times new roman', 20, 'bold'), fg='black', anchor=W, padx=5)
exit_btn.pack(fill=X)

## EmployeeFrame

emp_frame = Frame(window, background='#87CEFA', bd=3, relief=SUNKEN)
emp_frame.place(x=250, y=120, width=230, height=230)
emp_icon = PhotoImage(file='total_emp.png')
emp_icon_label = Label(emp_frame, image=emp_icon, background='#87CEFA')
emp_icon_label.pack(pady=15)

emp_label = Label(emp_frame, text='Total Employee', font=('times new roman', 15, 'bold'), fg='black', bg='#87CEFA')
emp_label.pack()
emp_count_label = Label(emp_frame, text='0', font=('times new roman', 25, 'bold'), fg='black', bg='#87CEFA')
emp_count_label.pack()

## SupplierFrame

supp_frame = Frame(window, background='#87CEFA', bd=3, relief=SUNKEN)
supp_frame.place(x=550, y=120, width=230, height=230)
supplier_icon = PhotoImage(file='total_sup.png')
supp_icon_label = Label(supp_frame, image=supplier_icon, background='#87CEFA')
supp_icon_label.pack(pady=15)

supp_label = Label(supp_frame, text='Total Supplier', font=('times new roman', 15, 'bold'), fg='black', bg='#87CEFA')
supp_label.pack()
supp_count_label = Label(supp_frame, text='0', font=('times new roman', 25, 'bold'), fg='black', bg='#87CEFA')
supp_count_label.pack()

## SalesFrame

sales_frame = Frame(window, background='#87CEFA', bd=3, relief=SUNKEN)
sales_frame.place(x=850, y=120, width=230, height=230)
sales_icon = PhotoImage(file='total_sales.png')
sales_icon_label = Label(sales_frame, image=sales_icon, background='#87CEFA')
sales_icon_label.pack(pady=15)

sales_label = Label(sales_frame, text='Total Sales', font=('times new roman', 15, 'bold'), fg='black', bg='#87CEFA')
sales_label.pack()
sales_count_label = Label(sales_frame, text='0', font=('times new roman', 25, 'bold'), fg='black', bg='#87CEFA')
sales_count_label.pack()

## CategoryFrame

cats_frame = Frame(window, background='#87CEFA', bd=3, relief=SUNKEN)
cats_frame.place(x=420, y=420, width=230, height=230)
cats_icon = PhotoImage(file='total_cat.png')
cats_icon_label = Label(cats_frame, image=cats_icon, background='#87CEFA')
cats_icon_label.pack(pady=15)

cats_label = Label(cats_frame, text='Total Category', font=('times new roman', 15, 'bold'), fg='black', bg='#87CEFA')
cats_label.pack()
cats_count_label = Label(cats_frame, text='0', font=('times new roman', 25, 'bold'), fg='black', bg='#87CEFA')
cats_count_label.pack()

## ProductFrame

prods_frame = Frame(window, background='#87CEFA', bd=3, relief=SUNKEN)
prods_frame.place(x=720, y=420, width=230, height=230)
prods_icon = PhotoImage(file='total_prod.png')
prods_icon_label = Label(prods_frame, image=prods_icon, background='#87CEFA')
prods_icon_label.pack(pady=15)

prods_label = Label(prods_frame, text='Total Product', font=('times new roman', 15, 'bold'), fg='black', bg='#87CEFA')
prods_label.pack()
prods_count_label = Label(prods_frame, text='0', font=('times new roman', 25, 'bold'), fg='black', bg='#87CEFA')
prods_count_label.pack()

window.mainloop()
