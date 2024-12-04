from datetime import date
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

import pymysql
from tkcalendar import DateEntry


def connect_database():
    try:
        connection = pymysql.connect(host='localhost', user='root', password='1234')
        cursor = connection.cursor()
    except:
        messagebox.showerror('Error', 'Database Connection Error, open mysql client')
        return None, None
    return cursor, connection

def create_database_table():
    cursor, connection = connect_database()
    cursor.execute('CREATE DATABASE IF NOT EXISTS inventory_system')
    cursor.execute('USE inventory_system')
    cursor.execute('CREATE TABLE IF NOT EXISTS employee_data (empid INT PRIMARY KEY, name VARCHAR(100),email VARCHAR(100),'
                   'gender VARCHAR(50), dob VARCHAR(30), contact VARCHAR(30), employment_type VARCHAR(50), '
                   'work_shift VARCHAR(50), address VARCHAR(100), doj VARCHAR(30), salary VARCHAR(50),'
                   'user_type VARCHAR(50), password VARCHAR(50))')
def treeview_data():
    cursor, connection = connect_database()
    if not cursor or not connection:
        return
    cursor.execute('USE inventory_system')
    try:
        cursor.execute('SELECT * FROM employee_data')
        employee_records = cursor.fetchall()
        employee_treeview.delete(*employee_treeview.get_children())
        for record in employee_records:
            employee_treeview.insert('', END, values=record)
    except Exception as e:
        messagebox.showerror('Error', e)
    finally:
        cursor.close()
        connection.close()

def select_data(event, empid_entry, name_entry, email_entry,
                gender_combo, dob_entry, contact_entry, emp_typ_combo, edu_combo,
                work_combo, address_entry, doj_entry,
                usertype_combo, salary_entry, password_entry):

    index = employee_treeview.selection()
    content = employee_treeview.item(index)
    row = content['values']
    print(row)
    empid_entry.insert(0, row[0])  # empid
    name_entry.insert(0, row[1])
    email_entry.insert(0, row[2])
    gender_combo.set(row[3])
    dob_entry.set_date(row[4])
    emp_typ_combo.set(row[5])
    edu_combo.set(row[6])
    work_combo.set(row[7])
    address_entry.insert(1.0,row[8])
    contact_entry.insert(0,row[9])
    doj_entry.set_date(row[10])
    usertype_combo.set(row[11])
    salary_entry.insert(0,row[12])
    password_entry.insert(0,row[13])


def add_employee(empid, name, email, gender, dob, contact, employment_type, education, work_shift, address, doj, salary,
                 user_type, password):

    if (empid == '' or name == '' or email == '' or gender == 'Select Gender' or contact == '' or employment_type == 'Select Emp Type' or
        work_shift == 'Select Shift' or address == '\n' or salary == '' or education == 'Select Education' or
        user_type == 'Select User Type' or password == '<PASSWORD>'):
        messagebox.showerror('Error', 'All fields are required')
    else:
        cursor, connection = connect_database()
        if not cursor or not connection:
            return
        cursor.execute('USE inventory_system')
        try:
            cursor.execute('Select empid from employee_data where empid =%s', (empid,))
            if cursor.fetchone():
                messagebox.showerror('Error', 'ID already exists')
                return
            cursor.execute('INSERT INTO employee_data values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(empid, name, email,
                                                                                                             gender, dob, employment_type, education, work_shift, address, contact, doj, user_type, salary, password))
            connection.commit()
            treeview_data()
            messagebox.showinfo('Success', 'Data inserted successfully')
        except Exception as e:
            messagebox.showerror('Error', e)
        finally:
            cursor.close()
            connection.close()


def clear_fields(empid_entry, name_entry, email_entry, gender_combo, dob_entry, contact_entry, emp_typ_combo, edu_combo,
                 work_combo,address_entry, doj_entry,salary_entry,usertype_combo, password_entry):
    empid_entry.delete(0, END)
    name_entry.delete(0, END)
    email_entry.delete(0, END)
    gender_combo.set('Select Gender')
    from datetime import date
    dob_entry.set_date(date.today())
    contact_entry.delete(0, END)
    emp_typ_combo.set('Select Employee Type')
    edu_combo.set('Select Education')
    work_combo.set('Select Work Shift')
    address_entry.delete(1.0, END)
    doj_entry.set_date(date.today())
    salary_entry.delete(0, END)
    usertype_combo.set('Select User Type')
    password_entry.delete(0, END)


def employee_form(window):
    global back_img, employee_treeview
    employee_frame = Frame(window, width=1100, height=600, bg='white')
    employee_frame.place(x=200, y=100)
    heading_label = Label(employee_frame, text="Employee Details", font=("Arial", 15, 'bold'),

                          bg="#0f4d7d", fg="white")
    heading_label.place(x=0, y=0, relwidth=1)
    #back_img = PhotoImage(file="back.png")       #if wish to put any images for back button
    back_button = Button(employee_frame, text="Back", cursor="hand2", bg='white',
                         command=lambda: employee_frame.place_forget())  #lambda is to see the employee form and off to the main dashboard
    back_button.place(x=10, y=30)

    top_frame = Frame(employee_frame, bg='white')
    top_frame.place(x=0, y=50, relwidth=1, height=250)

    search_frame = Frame(top_frame, bg='white')
    search_frame.pack()
    search_combobox = ttk.Combobox(search_frame, values=('Id', 'Name', 'Email'),
                                   font=("Times new roman", 12), state='readonly')
    search_combobox.set('Search By')
    search_combobox.grid(row=0, column=0, padx=20)
    search_entry = Entry(search_frame, font=("Times new roman", 12), bg='lightyellow')
    search_entry.grid(row=0, column=1, padx=20)
    search_button = Button(search_frame, text="Search", font=("Times new roman", 12),
                           width=7, cursor='hand2', fg='white', bg='#0f4d7d', )
    search_button.grid(row=0, column=2, padx=20)
    show_button = Button(search_frame, text="Show All", font=("Times new roman", 12),
                         width=7, cursor='hand2', fg='white', bg='#0f4d7d')
    show_button.grid(row=0, column=3)

    horizontal_scrollbar = Scrollbar(top_frame, orient=HORIZONTAL)
    vertical_scrollbar = Scrollbar(top_frame, orient=VERTICAL)
    employee_treeview = ttk.Treeview(top_frame, columns=('emp_id', 'name', 'email', 'gender', 'dob', 'employment_type',
                                                     'education', 'work_shift', 'address', 'contact', 'join_date',
                                                     'user_type', 'salary'), show='headings',
                                 yscrollcommand=vertical_scrollbar.set, xscrollcommand=horizontal_scrollbar.set)
    horizontal_scrollbar.pack(side=BOTTOM, fill=X)
    vertical_scrollbar.pack(side=RIGHT, fill=Y, pady=(10, 0))
    horizontal_scrollbar.config(command=employee_treeview.xview)
    vertical_scrollbar.config(command=employee_treeview.yview)
    employee_treeview.pack(pady=(10, 0))

    employee_treeview.heading('emp_id', text='Employee ID')
    employee_treeview.heading('name', text='Name')
    employee_treeview.heading('email', text='Email')
    employee_treeview.heading('gender', text='Gender')
    employee_treeview.heading('dob', text='Date of Birth')
    employee_treeview.heading('employment_type', text='Employment Type')
    employee_treeview.heading('education', text='Education')
    employee_treeview.heading('work_shift', text='Work Shift')
    employee_treeview.heading('address', text='Address')
    employee_treeview.heading('contact', text='Contacts')
    employee_treeview.heading('join_date', text='Join Date')
    employee_treeview.heading('user_type', text='User Type')
    employee_treeview.heading('salary', text='Salary')

    employee_treeview.column('emp_id', width=100)
    employee_treeview.column('name', width=120)
    employee_treeview.column('email', width=180)
    employee_treeview.column('gender', width=60)
    employee_treeview.column('dob', width=100)
    employee_treeview.column('employment_type', width=140)
    employee_treeview.column('education', width=80)
    employee_treeview.column('work_shift', width=80)
    employee_treeview.column('address', width=180)
    employee_treeview.column('join_date', width=100)
    employee_treeview.column('user_type', width=100)
    employee_treeview.column('salary', width=60)
    employee_treeview.column('contact', width=100)

    treeview_data()

    detail_frame = Frame(employee_frame,bg='white')
    detail_frame.place(x=20, y=300)

    empid_label = Label(detail_frame, text="Employee ID", font=("Times new roman", 12), bg='white')
    empid_label.grid(row=0, column=0, pady= 10, padx=20)
    empid_entry = Entry(detail_frame, font=("Times new roman", 12), bg='lightyellow')
    empid_entry.grid(row=0, column=1, pady= 10, padx=20)

    name_label = Label(detail_frame, text="Name", font=("Times new roman", 12), bg='white')
    name_label.grid(row=0, column=2, pady= 10, padx=20)
    name_entry = Entry(detail_frame, font=("Times new roman", 12), bg='lightyellow')
    name_entry.grid(row=0, column=3, pady= 10, padx=20)

    email_label = Label(detail_frame, text="Email", font=("Times new roman", 12), bg='white')
    email_label.grid(row=0, column=4, pady= 10, padx=20)
    email_entry = Entry(detail_frame, font=("Times new roman", 12), bg='lightyellow')
    email_entry.grid(row=0, column=5, pady= 10, padx=20)

    gender_label = Label(detail_frame, text="Gender", font=("Times new roman", 12), bg='white')
    gender_label.grid(row=1, column=0, pady= 10, padx=20)
    gender_combo = ttk.Combobox(detail_frame, values=('Male', 'Female'), font=("Times new roman", 12), state='readonly', width=18)
    gender_combo.set('Select Gender')
    gender_combo.grid(row=1, column=1, pady= 10, padx=20)

    dob_label = Label(detail_frame, text="Date of Birth", font=("Times new roman", 12), bg='white')
    dob_label.grid(row=1, column=2, pady=10, padx=20)
    dob_entry = DateEntry(detail_frame, font=("Times new roman", 12),width=18, state='readonly', date_pattern='dd/mm/YY')
    dob_entry.grid(row=1, column=3)

    edu_label = Label(detail_frame, text="Education", font=("Times new roman", 12), bg='white')
    edu_label.grid(row=1, column=4, pady=10, padx=20)
    edu_combo = ttk.Combobox(detail_frame, values=('PhD', 'Masters', 'Bachelors', 'Diploma', 'Vocational'), font=("Times new roman", 12), state='readonly', width=18)
    edu_combo.set('Select Education')
    edu_combo.grid(row=1, column=5, pady=10, padx=20)

    emp_typ_label = Label(detail_frame, text="Employment Type", font=("Times new roman", 12), bg='white')
    emp_typ_label.grid(row=1, column=4, pady=10, padx=20)
    emp_typ_combo = ttk.Combobox(detail_frame, values=('Full Time', 'Part Time', 'Intern', 'Work Student', 'Contract'), font=("Times new roman", 12), state='readonly', width=18)
    emp_typ_combo.set('Select Type')
    emp_typ_combo.grid(row=1, column=5, pady= 10, padx=20)

    contact_label = Label(detail_frame, text="Contact", font=("Times new roman", 12), bg='white')
    contact_label.grid(row=2, column=0, pady=10, padx=20)
    contact_entry = Entry(detail_frame, font=("Times new roman", 12), bg='lightyellow')
    contact_entry.grid(row=2, column=1, pady= 0, padx=20)

    edu_label = Label(detail_frame, text="Education", font=("Times new roman", 12), bg='white')
    edu_label.grid(row=2, column=2, pady=10, padx=20)
    edu_combo = ttk.Combobox(detail_frame, values=('PhD', 'Masters', 'Bachelors', 'Diploma', 'Vocational'), font=("Times new roman", 12), state='readonly', width=18)
    edu_combo.set('Select Education')
    edu_combo.grid(row=2, column=3, pady=10, padx=20)

    work_label = Label(detail_frame, text="Working Shift", font=("Times new roman", 12), bg='white')
    work_label.grid(row=2, column=4, pady= 10, padx=20)
    work_combo = ttk.Combobox(detail_frame, values=('Morning', 'Day', 'Night'), font=("Times new roman", 12), state='readonly', width=18)
    work_combo.set('Select Type')
    work_combo.grid(row=2, column=5, pady= 10, padx=20)

    address_label = Label(detail_frame, text="Address", font=("Times new roman", 12), bg='white')
    address_label.grid(row=3, column=0, pady=10, padx=20)
    address_entry = Text(detail_frame, font=("Times new roman", 12), bg='lightyellow', height=3, width=20)
    address_entry.grid(row=3, column=1, rowspan=2)

    doj_label = Label(detail_frame, text="Date of Joining", font=("Times new roman", 12), bg='white')
    doj_label.grid(row=3, column=2, pady=10, padx=20)
    doj_entry = DateEntry(detail_frame, font=("Times new roman", 12),width=18, state='readonly', date_pattern='dd/mm/YY')
    doj_entry.grid(row=3, column=3)

    usertype_label = Label(detail_frame, text="User Type", font=("Times new roman", 12), bg='white')
    usertype_label.grid(row=3, column=4, pady=10, padx=20)
    usertype_combo = ttk.Combobox(detail_frame, values=('Employee', 'Admin'), font=("Times new roman", 12), state='readonly', width=18)
    usertype_combo.set('Select User Type')
    usertype_combo.grid(row=3, column=5, pady=10, padx=20)

    salary_label = Label(detail_frame, text="Salary", font=("Times new roman", 12), bg='white')
    salary_label.grid(row=4, column=2, pady=10, padx=20)
    salary_entry = Entry(detail_frame, font=("Times new roman", 12), bg='lightyellow')
    salary_entry.grid(row=4, column=3, pady=10, padx=20)

    password_label = Label(detail_frame, text="Password", font=("Times new roman", 12), bg='white')
    password_label.grid(row=4, column=4, pady=10, padx=20)
    password_entry = Entry(detail_frame, font=("Times new roman", 12), bg='lightyellow')
    password_entry.grid(row=4, column=5, pady=10, padx=20)

    button_frame = Frame(employee_frame, bg='white')
    button_frame.place(x=200, y=530)

    add_button = Button(button_frame, text="Add", font=("Times new roman", 12),
                          width=9, cursor='hand2', fg='white', bg='#0f4d7d', command=lambda: add_employee(empid_entry.get(), name_entry.get(), email_entry.get(),
                                                                                                  gender_combo.get(), dob_entry.get(), contact_entry.get(),
                                                                                                  emp_typ_combo.get(), edu_combo.get(), work_combo.get(),
                                                                                                  address_entry.get(1.0,END), doj_entry.get(),
                                                                                                  salary_entry.get(), usertype_combo.get(), password_entry.get()))
    add_button.grid(row=0, column=0, padx=20)
    update_button = Button(button_frame, text="Update", font=("Times new roman", 12),
                          width=9, cursor='hand2', fg='white', bg='#0f4d7d', )
    update_button.grid(row=0, column=1, padx=80)
    delete_button = Button(button_frame, text="Delete", font=("Times new roman", 12),
                          width=9, cursor='hand2', fg='white', bg='#0f4d7d', )
    delete_button.grid(row=0, column=2, padx=80)
    clear_button = Button(button_frame, text="Clear", font=("Times new roman", 12),
                          width=9, cursor='hand2', fg='white', bg='#0f4d7d', command=lambda: clear_fields(empid_entry, name_entry, email_entry,
                                                                                                  gender_combo, dob_entry, contact_entry,
                                                                                                  emp_typ_combo, edu_combo, work_combo,
                                                                                                  address_entry, doj_entry,salary_entry,
                                                                                                  usertype_combo, password_entry))
    clear_button.grid(row=0, column=3, padx=20)
    employee_treeview.bind('<ButtonRelease-1>', lambda event: select_data(event,empid_entry, name_entry, email_entry,
                                                            gender_combo, dob_entry, contact_entry,
                                                            emp_typ_combo, edu_combo, work_combo,
                                                            address_entry, doj_entry, usertype_combo,
                                                            salary_entry,password_entry))

    create_database_table()