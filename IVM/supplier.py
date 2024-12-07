from tkinter import *
from tkinter import ttk, messagebox
from employees import connect_database



def delete_supplier(invoice, treeview):
    index = treeview.selection()
    if not index:
        messagebox.showerror('Error', 'No selected row')
    else:
        messagebox.askyesno('Confirm', 'Do you want to delete this record?')
        cursor, connection = connect_database()
        if not cursor or not connection:
            return
        try:
            cursor.execute('use inventory_system')
            cursor.execute('DELETE FROM supplier_data WHERE invoice=%s',invoice)
            connection.commit()
            treeview_data(treeview)
            messagebox.showinfo('Info','Record is deleted')
        except Exception as e:
            messagebox.showerror('Error', str(e))
        finally:
            cursor.close()
            connection.close()


def clear_supplier(invoice_entry, name_entry, contact_entry, description_text, treeview):
    invoice_entry.delete(0,END)
    name_entry.delete(0,END)
    contact_entry.delete(0,END)
    description_text.delete(1.0,END)
    treeview.selection_remove(treeview.selection())

def search_supplier(search_value,treeview):
    if search_value=='':
        messagebox.showerror('Error', 'Please select an invoice')
    else:
        cursor, connection = connect_database()
        if not cursor or not connection:
            return
        try:
            cursor.execute('use inventory_system')
            cursor.execute('SELECT * FROM supplier_data WHERE invoice=%s',search_value)
            record = cursor.fetchone()
            if not record:
                messagebox.showerror('Error', 'No record found')
                return
            treeview.delete(*treeview.get_children())
            treeview.insert('',END,values=record)
        except Exception as e:
            messagebox.showerror('Error', e)
        finally:
            cursor.close()
            connection.close()

def show_all(treeview,search_entry):
    treeview_data(treeview)
    search_entry.delete(0,END)



def update_supplier(invoice, name, contact, description, treeview):
    index=treeview.selection()
    if not index:
        messagebox.showerror('Error', 'No selected row')
        return
    cursor, connection = connect_database()
    if not cursor or not connection:
        return
    try:
        cursor.execute('use inventory_system')
        cursor.execute('SELECT * FROM supplier_data WHERE invoice=%s', invoice)
        current_data=cursor.fetchone()
        current_data=current_data[1:]
        new_data = (name, contact, description)
        if current_data==new_data:
            messagebox.showinfo('Info', 'No Changes detected')
            return
        cursor.execute('UPDATE supplier_data SET name=%s, contact=%s, description=%s WHERE invoice=%s',(name,contact,description,invoice))
        connection.commit()
        messagebox.showinfo('Updated', 'Successfully data updated')
        treeview_data(treeview)
    except Exception as e:
        messagebox.showerror('Error', e)
    finally:
        cursor.close()
        connection.close()


def select_data(event, invoice_entry, name_entry, contact_entry, description_text, treeview):
    index=treeview.selection()
    content = treeview.item(index)
    row=content['values']
    invoice_entry.delete(0,END)
    name_entry.delete(0,END)
    contact_entry.delete(0,END)
    description_text.delete(1.0,END)

    invoice_entry.insert(0, row[0])
    name_entry.insert(0, row[1])
    contact_entry.insert(0, row[2])
    description_text.insert(1.0, row[3])



def treeview_data(treeview):
    cursor, connection = connect_database()
    if not cursor or not connection:
        return
    try:
        cursor.execute('use inventory_system')
        cursor.execute('SELECT * FROM supplier_data')
        records=cursor.fetchall()
        treeview.delete(*treeview.get_children())
        for record in records:
            treeview.insert('', END, values=record)
    except Exception as e:
        messagebox.showerror('Error', e)
    finally:
        cursor.close()
        connection.close()


def add_supplier(invoice, name, contact, description, treeview):
    if invoice == '' or name == '' or contact == '' or description == '':
        messagebox.showinfo('Error', 'Please fill all the fields')
    else:
        cursor, connection = connect_database()
        if not cursor or not connection:
            return
        try:
            cursor.execute('use inventory_system')
            cursor.execute('CREATE TABLE IF NOT EXISTS supplier_data (invoice INT PRIMARY KEY, name VARCHAR(100), contact VARCHAR(40), description TEXT)')

            cursor.execute('SELECT * FROM supplier_data WHERE invoice=%s', invoice)
            if cursor.fetchone():
                messagebox.showinfo('Error', 'Invoice already exists')
                return

            cursor.execute('INSERT INTO supplier_data VALUES(%s,%s,%s,%s)', (invoice, name, contact, description))
            connection.commit()
            messagebox.showinfo('Success', 'Data added successfully')
            treeview_data(treeview)
        except Exception as e:
            messagebox.showerror('Error', e)
        finally:
            cursor.close()
            connection.close()


def supplier_form(window):
    supplier_frame = Frame(window, width=1100, height=600, bg='white')
    supplier_frame.place(x=200, y=100)
    heading_label = Label(supplier_frame, text="Supplier Details", font=("Arial", 15, 'bold'),

                          bg="#0f4d7d", fg="white")
    heading_label.place(x=0, y=0, relwidth=1)
    back_button = Button(supplier_frame, text="Back", cursor="hand2", bg='white',
                         command=lambda: supplier_frame.place_forget())  #lambda is to see the employee form and off to the main dashboard
    back_button.place(x=10, y=30)

    left_frame = Frame(supplier_frame, bg='white')
    left_frame.place(x=10, y=100)

    invoice_label = Label(left_frame, text="Invoice No.", font=("Times new roman", 15, 'bold'),bg='white')
    invoice_label.grid(row=0, column=0, padx=(20,30), pady=10, sticky=W)
    invoice_entry = Entry(left_frame, font=("Times new roman", 15), bg='lightyellow')
    invoice_entry.grid(row=0, column=1, sticky=W)

    name_label = Label(left_frame, text="Supplier Name", font=("Times new roman", 15, 'bold'),bg='white')
    name_label.grid(row=1, column=0, padx=(20,40), pady=10, sticky=W)
    name_entry = Entry(left_frame, font=("Times new roman", 15), bg='lightyellow')
    name_entry.grid(row=1, column=1, sticky=W)

    contact_label = Label(left_frame, text="Contact", font=("Times new roman", 15, 'bold'),bg='white')
    contact_label.grid(row=2, column=0, padx=(20,40), pady=10, sticky=W)
    contact_entry = Entry(left_frame, font=("Times new roman", 15), bg='lightyellow')
    contact_entry.grid(row=2, column=1, sticky=W)

    description_label = Label(left_frame, text="Description", font=("Times new roman", 15, 'bold'),bg='white')
    description_label.grid(row=3, column=0, padx=(20,40), pady=25, sticky='nw')
    description_text = Text(left_frame, height=6,width=25, bd=2, bg='lightyellow')
    description_text.grid(row=3, column=1, pady=25, sticky='nw')

    button_frame = Frame(left_frame, bg='white')
    button_frame.grid(row=4, columnspan=2, pady=20)

    add_button = Button(button_frame, text="ADD", font=("Times new roman", 12),width=8, cursor='hand2', fg='white',
                        bg='#0f4d7d', command=lambda: add_supplier(invoice_entry.get(), name_entry.get(),
                                                           contact_entry.get(), description_text.get(1.0, END).strip(), treeview))
    add_button.grid(row=0, column=0, padx=(20,10))

    update_button = Button(button_frame, text="UPDATE", font=("Times new roman", 12), width=8, cursor='hand2', fg='white',
                        bg='#0f4d7d', command=lambda: update_supplier(invoice_entry.get(), name_entry.get(),
                                                           contact_entry.get(), description_text.get(1.0, END).strip(), treeview))
    update_button.grid(row=0, column=1, padx=10)

    delete_button = Button(button_frame, text="DELETE", font=("Times new roman", 12), width=8, cursor='hand2', fg='white',
                        bg='#0f4d7d', command=lambda :delete_supplier(invoice_entry.get(), treeview))
    delete_button.grid(row=0, column=2, padx=10)

    clear_button = Button(button_frame, text="CLEAR", font=("Times new roman", 12), width=8, cursor='hand2', fg='white',
                        bg='#0f4d7d', command=lambda :clear_supplier(invoice_entry,name_entry,contact_entry,description_text, treeview))
    clear_button.grid(row=0, column=3,)

    right_frame = Frame(supplier_frame, bg='white')
    right_frame.place(x=500, y=100, height=400, width=500)

    search_frame = Frame(right_frame, bg='white')
    search_frame.pack(pady=(0,15))

    num_label = Label(search_frame, text="Invoice No.", font=("Times new roman", 15, 'bold'), bg='white')
    num_label.grid(row=0, column=0, padx=15, pady=10, sticky=W)
    search_entry = Entry(search_frame, font=("Times new roman", 15), bg='lightyellow', width=10)
    search_entry.grid(row=0, column=1, sticky=W)

    search_button = Button(search_frame, text="SEARCH", font=("Times new roman", 12), width=10, cursor='hand2', fg='white',
                        bg='#0f4d7d', command=lambda :search_supplier(search_entry.get(),treeview))
    search_button.grid(row=0, column=2, padx=15)

    show_button = Button(search_frame, text="SHOW ALL", font=("Times new roman", 12), width=10, cursor='hand2', fg='white',
                        bg='#0f4d7d',command=lambda :show_all(treeview,search_entry))
    show_button.grid(row=0, column=3,)

    horizontal_scrollbar = Scrollbar(right_frame, orient=HORIZONTAL)
    vertical_scrollbar = Scrollbar(right_frame, orient=VERTICAL)

    treeview = ttk.Treeview(right_frame, columns=('invoice', 'name', 'contact', 'description'), show='headings',
                            yscrollcommand=vertical_scrollbar.set, xscrollcommand=horizontal_scrollbar.set)
    horizontal_scrollbar.pack(side=BOTTOM, fill=X)
    vertical_scrollbar.pack(side=RIGHT, fill=Y)
    horizontal_scrollbar.config(command=treeview.xview)
    vertical_scrollbar.config(command=treeview.yview)

    treeview.pack(fill=BOTH, expand=1)
    treeview.heading('invoice', text='Invoice Id')
    treeview.heading('name', text='Supplier Name')
    treeview.heading('contact', text='Supplier Contact')
    treeview.heading('description', text='Description')

    treeview.column('invoice', width=80)
    treeview.column('name', width=160)
    treeview.column('contact', width=120)
    treeview.column('description', width=250)

    treeview_data(treeview)
    treeview.bind('<ButtonRelease-1>', lambda  event:select_data(event,invoice_entry, name_entry, contact_entry,
                                                                 description_text, treeview))


