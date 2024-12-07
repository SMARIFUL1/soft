from tkinter import *
from tkinter import ttk, messagebox
from employees import connect_database



def treeview_data(treeview):
    cursor, connection = connect_database()
    if not cursor or not connection:
        return
    try:
        cursor.execute('use inventory_system')
        cursor.execute('select * from category_data')
        records = cursor.fetchall()
        treeview.delete(*treeview.get_children())  #deleting old data at first
        for record in records:
            treeview.insert('', END, values=record)
    except Exception as e:
        messagebox.showinfo('Error', e)
    finally:
        cursor.close()
        connection.close()

def add_category(category, name, description, treeview):
    if category == '' or name == '' or description == '':
        messagebox.showerror('Error', 'Please enter all required fields.')
    else:
        cursor, connection = connect_database()
        if not cursor or not connection:
            return
        try:
            cursor.execute('use inventory_system')
            cursor.execute(
                'CREATE TABLE IF NOT EXISTS category_data (category_id INT PRIMARY KEY, name VARCHAR(100), description TEXT)')
            cursor.execute('SELECT * FROM category_data WHERE category_id = %s', category)
            if cursor.fetchone():
                messagebox.showerror('Error', 'Category ID already exists.')
                return
            cursor.execute('INSERT INTO category_data VALUES (%s, %s, %s)',(category, name, description))
            connection.commit()
            messagebox.showinfo('Success', f'Category added successfully.')
            treeview_data(treeview)
        except Exception as e:
            messagebox.showinfo('Error', e)
        finally:
            cursor.close()
            connection.close()

def select_data(event, category_entry, name_entry, description_text, treeview):
    index=treeview.selection()
    content = treeview.item(index)
    row=content['values']
    category_entry.delete(0,END)
    name_entry.delete(0,END)
    description_text.delete(1.0,END)

    category_entry.insert(0, row[0])
    name_entry.insert(0, row[1])
    description_text.insert(1.0, row[2])

def clear_category(category_entry, name_entry, description_text, treeview):
    category_entry.delete(0, END)
    name_entry.delete(0, END)
    description_text.delete(1.0, END)
    treeview.selection_remove(treeview.selection())
def delete_category(category_id, treeview):
    index = treeview.selection()
    if not index:
        messagebox.showerror('Error', 'No selected row')
        return
    else:
        messagebox.askyesno('Confirm', 'Do you want to delete this record?')
        cursor, connection = connect_database()
        if not cursor or not connection:
            return
        try:
            cursor.execute('use inventory_system')
            cursor.execute('DELETE FROM category_data WHERE category_id=%s',category_id)
            connection.commit()
            treeview_data(treeview)
            messagebox.showinfo('Info','Record is deleted')
        except Exception as e:
            messagebox.showerror('Error', str(e))
        finally:
            cursor.close()
            connection.close()

def category_form(window):
    global logo
    category_frame = Frame(window, width=1100, height=600, bg='white')
    category_frame.place(x=200, y=100)
    heading_label = Label(category_frame, text="Product Category Details", font=("Times new roman", 15, 'bold'),
                          bg="#0f4d7d", fg="white")
    heading_label.place(x=0, y=0, relwidth=1)
    back_button = Button(category_frame, text="Back", cursor="hand2", bg='white',
                         command=lambda: category_frame.place_forget())  #lambda is to see the employee form and off to the main dashboard
    back_button.place(x=10, y=30)

    logo=PhotoImage(file='category.png')
    logo_label = Label(category_frame, image=logo, height=400, width=300, bg='white')
    logo_label.place(x=20, y=120)

    details_frame = Frame(category_frame, bg='white')
    details_frame.place(x=330, y=110)

    category_label = Label(details_frame, text="Category ID", font=("Times new roman", 15, 'bold'), bg='white')
    category_label.grid(row=0, column=0, padx=10, pady=10, sticky=W)
    category_entry = Entry(details_frame, font=("Times new roman", 15), bg='lightyellow')
    category_entry.grid(row=0, column=1, sticky=W)

    name_label = Label(details_frame, text="Category Name", font=("Times new roman", 15, 'bold'), bg='white')
    name_label.grid(row=1, column=0, padx=10, pady=10, sticky=W)
    name_entry = Entry(details_frame, font=("Times new roman", 15), bg='lightyellow')
    name_entry.grid(row=1, column=1, sticky=W)

    description_label = Label(details_frame, text="Description", font=("Times new roman", 15, 'bold'), bg='white')
    description_label.grid(row=2, column=0, padx=10, pady=25, sticky='nw')
    description_text = Text(details_frame, height=6, width=25, bd=2, bg='lightyellow')
    description_text.grid(row=2, column=1, pady=25, sticky='nw')

    button_frame = Frame(details_frame, bg='white')
    button_frame.grid(row=3, columnspan=2, pady=70)

    add_button = Button(button_frame, text="ADD", font=("Times new roman", 12), width=8, cursor='hand2', fg='white',
                        bg='#0f4d7d', command=lambda: add_category(category_entry.get(), name_entry.get(),
                                                                   description_text.get(1.0, END).strip(), treeview))
    add_button.grid(row=0, column=0, padx=(110, 12))

    clear_button = Button(button_frame, text="CLEAR", font=("Times new roman", 12), width=8, cursor='hand2', fg='white',
                        bg='#0f4d7d', command=lambda :clear_category(category_entry,name_entry,description_text, treeview))
    clear_button.grid(row=0, column=1, padx=15)

    delete_button = Button(button_frame, text="DELETE", font=("Times new roman", 12), width=8, cursor='hand2',
                           fg='white', bg='#0f4d7d', command=lambda: delete_category(category_entry.get(), treeview))
    delete_button.grid(row=0, column=2,padx=(12,10))

    treeview_frame = Frame(category_frame, bg='lightblue')
    treeview_frame.place(x=750, y=120, height=400, width=330)

    horizontal_scrollbar = Scrollbar(treeview_frame, orient=HORIZONTAL)
    vertical_scrollbar = Scrollbar(treeview_frame, orient=VERTICAL)

    treeview = ttk.Treeview(treeview_frame, columns=('id', 'name', 'description'), show='headings',
                            yscrollcommand=vertical_scrollbar.set, xscrollcommand=horizontal_scrollbar.set)
    horizontal_scrollbar.pack(side=BOTTOM, fill=X)
    vertical_scrollbar.pack(side=RIGHT, fill=Y)
    horizontal_scrollbar.config(command=treeview.xview)
    vertical_scrollbar.config(command=treeview.yview)

    treeview.pack(fill=BOTH, expand=1)
    treeview.heading('id', text='Category ID')
    treeview.heading('name', text='Category Name')
    treeview.heading('description', text='Description')

    treeview.column('id', width=80)
    treeview.column('name', width=120)
    treeview.column('description', width=150)

    treeview_data(treeview)
    treeview.bind('<ButtonRelease-1>', lambda event: select_data(event, category_entry, name_entry,
                                                                 description_text, treeview))
