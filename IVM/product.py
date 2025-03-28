from tkinter import *
from tkinter import ttk, messagebox
from employees import connect_database


def show_all(treeview, search_combobox,search_entry):
    treeview_data(treeview)
    search_combobox.set('Search By')
    search_entry.delete(0, END)

def search_product(search_combobox,search_entry, treeview):
    if search_combobox.get() == "Search By":
        messagebox.showwarning('Warning','Please select an option')
    elif search_entry.get()=='':
        messagebox.showwarning('Warning','Please enter value to search')
    else:
        cursor, connection = connect_database()
        if not cursor or not connection:
            return
        cursor.execute('use inventory_system')
        cursor.execute(f'SELECT * FROM product_data WHERE {search_combobox.get()}=%s',search_entry.get())
        records = cursor.fetchall()
        if len(records) == 0:
            messagebox.showerror('Error','No records found')
            return
        treeview.delete(*treeview.get_children())
        for record in records:
            treeview.insert('', END, values=record)

def select_data(event, treeview,category_combobox,supplier_combobox,name_entry,price_entry,quantity_entry,status_combobox, discount_spinbox):
    index=treeview.selection()
    dict = treeview.item(index)
    content=dict['values']
    category_combobox.delete(0,END)
    supplier_combobox.delete(0,END)
    name_entry.delete(0,END)
    price_entry.delete(0,END)
    discount_spinbox.delete(0,END)
    quantity_entry.delete(0,END)
    status_combobox.delete(0,END)

    category_combobox.set(content[1])
    supplier_combobox.set(content[2])
    name_entry.insert(0, content[3])
    price_entry.insert(0, content[4])
    discount_spinbox.insert(0,content[5])
    quantity_entry.insert(0, content[7])
    status_combobox.set(content[8])

def treeview_data(treeview):
    cursor, connection = connect_database()
    if not cursor or not connection:
        return
    try:
        cursor.execute('use inventory_system')
        cursor.execute('select * from product_data')
        records = cursor.fetchall()
        treeview.delete(*treeview.get_children())  #deleting old data at first
        for record in records:
            treeview.insert('', END, values=record)
    except Exception as e:
        messagebox.showinfo('Error', e)
    finally:
        cursor.close()
        connection.close()

def fetch_supplier_category(category_combobox, supplier_combobox):
    category_option=[]
    supplier_option=[]
    cursor, connection = connect_database()
    if not cursor or not connection:
        return
    cursor.execute('USE inventory_system')
    cursor.execute('SELECT name FROM category_data')
    names = cursor.fetchall()
    if len(names) >0:
        category_combobox.set('Select')
        for name in names:
            category_option.append(name[0])
        category_combobox.config(values=category_option)

    cursor.execute('SELECT name FROM supplier_data')
    names = cursor.fetchall()
    if len(names) >0:
        supplier_combobox.set('Select')
        for name in names:
            supplier_option.append(name[0])
        supplier_combobox.config(values=supplier_option)

def add_product(category, supplier, name, price, discount, quantity, status,treeview):
    if category == 'Empty':
        messagebox.showerror('Error', 'Please enter a valid category.')
    elif supplier=='Empty':
        messagebox.showerror('Error', 'Please enter a valid supplier.')
    elif category=='Select' or supplier=='Select' or name=='' or price=='' or quantity=='' or status=='Select Status':
        messagebox.showerror('Error', 'All fields are required.')
    else:
        cursor, connection = connect_database()
        if not cursor or not connection:
            return
        cursor.execute('USE inventory_system')
        cursor.execute('CREATE TABLE IF NOT EXISTS product_data (id INT AUTO_INCREMENT PRIMARY KEY, category VARCHAR(100),'
                       'supplier VARCHAR(100), name VARCHAR(100),price DECIMAL(10,2),quantity INT,status VARCHAR(50))')

        #cursor.execute('ALTER table product_data ADD COLUMN discount INT AFTER price, ADD COLUMN discounted_price DECIMAL(10,2) AFTER discount')

        cursor.execute('SELECT * FROM product_data WHERE category=%s AND supplier=%s AND name=%s',(category,supplier, name))
        existing_product = cursor.fetchone()
        if existing_product:
            messagebox.showerror('Error', 'Product already exists.')
            return
        discounted_price=round(float(price)*(1-int(discount)/100),2)
        cursor.execute('INSERT INTO product_data (category, supplier, name, price,discount,discounted_price, quantity, status) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)',
                       (category, supplier, name, price,discount,discounted_price, quantity, status))
        connection.commit()
        messagebox.showinfo('Success', 'Data added successfully.')
        treeview_data(treeview)

def update_product(category, supplier, name, price, discount, quantity, status,treeview):
    index=treeview.selection()
    dict=treeview.item(index)
    content=dict['values']

    if not index:
        messagebox.showerror('Error', 'Please select a row.')
        return
    id = content[0]
    cursor, connection = connect_database()
    if not cursor or not connection:
        return
    try:
        cursor.execute('USE inventory_system')
        cursor.execute('SELECT * FROM product_data WHERE id=%s',id)
        current_data=cursor.fetchone()
        current_data=current_data[1:]
        current_data=list(current_data)
        current_data[3]=str(current_data[3])
        current_data[4]=str(current_data[4])
        current_data=tuple(current_data)

        quantity=int(quantity)
        new_data=(category,supplier,name,price,discount,quantity,status,current_data)

        if current_data==new_data:
            messagebox.showerror('Error', 'No changes detected.')
            return
        discounted_price = round(float(price) * (1 - int(discount) / 100), 2)
        cursor.execute('UPDATE product_data SET category=%s, supplier=%s, name=%s,price=%s,discount=%s,discounted_price=%s,'
                       'quantity=%s,status=%s WHERE id=%s',(category,supplier,name,price,discount,discounted_price,quantity,status,id))
        connection.commit()
        messagebox.showinfo('Success', 'Data updated successfully.')
        treeview_data(treeview)

    except Exception as e:
        messagebox.showerror('Error', str(e))
    finally:
        cursor.close()
        connection.close()

def clear_fields(category_combobox,supplier_combobox,name_entry,price_entry,quantity_entry,status_combobox,discount_spinbox, treeview):
        category_combobox.set('Select')
        supplier_combobox.set('Select')
        name_entry.delete(0,END)
        price_entry.delete(0,END)
        discount_spinbox.delete(0, END)
        quantity_entry.delete(0,END)
        status_combobox.set('Select Status')
        treeview.selection_remove(treeview.selection())

def delete_product(treeview,category_combobox,supplier_combobox,name_entry,price_entry,discount_spinbox,quantity_entry,status_combobox):
    index = treeview.selection()
    dict = treeview.item(index)
    content = dict['values']
    if not index:
        messagebox.showerror('Error', 'No selected row')
        return
    id = content[0]
    response=messagebox.askyesno('Confirm', 'Do you want to delete this record?')
    if response:
        cursor, connection = connect_database()
        if not cursor or not connection:
                return
        try:
             cursor.execute('use inventory_system')
             cursor.execute('DELETE FROM product_data WHERE id=%s',id)
             connection.commit()
             treeview_data(treeview)
             messagebox.showinfo('Info','Record is deleted')
             clear_fields(category_combobox,supplier_combobox,name_entry,price_entry,discount_spinbox,quantity_entry,status_combobox,treeview)
        except Exception as e:
            messagebox.showerror('Error', e)
        finally:
            cursor.close()
            connection.close()

def product_form(window):
    product_frame = Frame(window, width=1100, height=600, bg='white')
    product_frame.place(x=200, y=100)
    heading_label = Label(product_frame, text="Product Details Board", font=("Times new roman", 15, 'bold'),
                          bg="#0f4d7d", fg="white")
    heading_label.place(x=0, y=0, relwidth=1)
    back_button = Button(product_frame, text="Back", cursor="hand2", bg='white',
                         command=lambda: product_frame.place_forget())  # lambda is to see the employee form and off to the main dashboard
    back_button.place(x=10, y=30)

    logo = PhotoImage(file='category.png')
    logo_label = Label(product_frame, image=logo, height=400, width=300, bg='white')
    logo_label.place(x=20, y=120)

    left_frame = Frame(product_frame, bg='white', bd=2, relief="ridge")
    left_frame.place(x=20, y=60, height=520)
    heading_label = Label(left_frame, text="Product Entry Details", font=("Times new roman", 15, 'bold'),
                          bg="#0f4d7d", fg='white', )
    heading_label.grid(row=0, columnspan=2, sticky="ew")

    category_label = Label(left_frame, text="Category", font=("Times new roman", 15, 'bold'), bg='white')
    category_label.grid(row=1, column=0, pady=(30,10), sticky=W)
    category_combobox = ttk.Combobox(left_frame, font=('Times new roman', 15, 'bold'),width=18, state='readonly')
    category_combobox.grid(row=1, column=1, padx=20)
    category_combobox.set('Empty')

    supplier_label = Label(left_frame, text="Supplier", font=("Times new roman", 15, 'bold'), bg='white')
    supplier_label.grid(row=2, column=0, pady=10, sticky=W)
    supplier_combobox = ttk.Combobox(left_frame, font=('Times new roman', 15, 'bold'),width=18, state='readonly')
    supplier_combobox.grid(row=2, column=1, padx=20)
    supplier_combobox.set('Empty')

    name_label = Label(left_frame, text="Name", font=("Times new roman", 15, 'bold'), bg='white')
    name_label.grid(row=3, column=0, pady=10, sticky=W)
    name_entry = Entry(left_frame, font=('Times new roman', 15, 'bold'), bg='white', width=20)
    name_entry.grid(row=3, column=1, padx=60, sticky=W)

    price_label = Label(left_frame, text="Price", font=("Times new roman", 15, 'bold'), bg='white')
    price_label.grid(row=4, column=0, pady=10, sticky=W)
    price_entry = Entry(left_frame, font=('Times new roman', 15, 'bold'), bg='white', width=20)
    price_entry.grid(row=4, column=1, padx=60, sticky=W)

    discount_label = Label(left_frame, text="Discount(%)", font=("Times new roman", 15, 'bold'), bg='white')
    discount_label.grid(row=5, column=0, pady=10, sticky=W)
    discount_spinbox = Spinbox(left_frame,from_=0, to=100, font=('Times new roman', 15, 'bold'), bg='white', width=19)
    discount_spinbox.grid(row=5, column=1, padx=59, sticky=W)

    quantity_label = Label(left_frame, text="Quantity", font=("Times new roman", 15, 'bold'), bg='white')
    quantity_label.grid(row=6, column=0, pady=10, sticky=W)
    quantity_entry = Entry(left_frame, font=('Times new roman', 15, 'bold'), bg='white', width=20)
    quantity_entry.grid(row=6, column=1, padx=60, sticky=W)

    status_label = Label(left_frame, text="Status", font=("Times new roman", 15, 'bold'), bg='white')
    status_label.grid(row=7, column=0, pady=(20,0), sticky=W)
    status_combobox = ttk.Combobox(left_frame, values=('Active', 'Inactive'), font=('Times new roman', 15, 'bold'),width=18, state='readonly')
    status_combobox.grid(row=7, column=1,)
    status_combobox.set('Select Status')

    button_frame = Frame(left_frame, bg='white')
    button_frame.grid(row=8, columnspan=2, pady=70)

    add_button = Button(button_frame, text="Add", font=("Times new roman", 12), width=8, cursor='hand2', fg='white',
                         bg='#0f4d7d', command=lambda :add_product(category_combobox.get(),supplier_combobox.get(),
                                                                   name_entry.get(),price_entry.get(),discount_spinbox.get(),quantity_entry.get(),
                                                                   status_combobox.get(), treeview),)
    add_button.grid(row=0, column=0, padx=10)
    update_button = Button(button_frame, text="Update", font=("Times new roman", 12), width=8, cursor='hand2', fg='white',
                           bg='#0f4d7d', command=lambda:update_product(category_combobox.get(),supplier_combobox.get(),
                                                                   name_entry.get(),price_entry.get(),discount_spinbox.get(),
                                                                       quantity_entry.get(),status_combobox.get(), treeview))
    update_button.grid(row=0, column=1, padx=10)
    clear_button = Button(button_frame, text="Clear", font=("Times new roman", 12), width=8, cursor='hand2', fg='white',
                          bg='#0f4d7d', command=lambda :clear_fields(category_combobox,supplier_combobox,name_entry,
                                                                     price_entry,quantity_entry,status_combobox,
                                                                     discount_spinbox,treeview))
    clear_button.grid(row=0, column=2, padx=10)
    delete_button = Button(button_frame, text="Delete", font=("Times new roman", 12), width=8, cursor='hand2',fg='white',
                           bg='#0f4d7d',command=lambda :delete_product(treeview,category_combobox,supplier_combobox,
                                                                       name_entry,price_entry,quantity_entry,status_combobox,
                                                                       discount_spinbox))
    delete_button.grid(row=0, column=3, padx=10)

    search_frame = LabelFrame(product_frame, text='Search Product', font=('times new roman', 14) ,bg='white')
    search_frame.place(x=460, y=50)
    search_combobox = ttk.Combobox(search_frame, values=('Category','Supplier','Name','Price','Status'),
                                   font=('Times new roman', 15, ),width=16)
    search_combobox.grid(row=0, column=0, padx=10, pady=10, sticky=W)
    search_combobox.set('Search By')

    search_entry = Entry(search_frame, font=('Times new roman', 15, 'bold'), bg='lightyellow', width=18)
    search_entry.grid(row=0, column=1, padx=10)

    search_button = Button(search_frame, text="Search", font=("Times new roman", 12), width=8, cursor='hand2', fg='white',
                           bg='#0f4d7d',command=lambda :search_product(search_combobox,search_entry,treeview))
    search_button.grid(row=0, column=2, padx=10)

    show_button = Button(search_frame, text="Show All", font=("Times new roman", 12), width=8, cursor='hand2', fg='white',
                          bg='#0f4d7d', command=lambda :show_all(treeview,search_combobox,search_entry))
    show_button.grid(row=0, column=3, padx=10)

    treeview_frame = Frame(product_frame, bg='white')
    treeview_frame.place(x=460, y=130, width=615, height=450)

    horizontal_scrollbar = Scrollbar(treeview_frame, orient=HORIZONTAL)
    vertical_scrollbar = Scrollbar(treeview_frame, orient=VERTICAL)

    treeview = ttk.Treeview(treeview_frame, columns=('id','category', 'supplier', 'name','price','discount','discounted_price','quantity','status'), show='headings',
                            yscrollcommand=vertical_scrollbar.set, xscrollcommand=horizontal_scrollbar.set)
    horizontal_scrollbar.pack(side=BOTTOM, fill=X)
    vertical_scrollbar.pack(side=RIGHT, fill=Y)
    horizontal_scrollbar.config(command=treeview.xview)
    vertical_scrollbar.config(command=treeview.yview)

    treeview.pack(fill=BOTH, expand=1)

    treeview.heading('id', text='ID')
    treeview.heading('category', text='Category')
    treeview.heading('supplier', text='Supplier')
    treeview.heading('name', text='Product Name')
    treeview.heading('price', text='Price')
    treeview.heading('discount', text='Discount')
    treeview.heading('discounted_price', text='Discounted Price')
    treeview.heading('quantity', text='Quantity')
    treeview.heading('status', text='Status')

    fetch_supplier_category(category_combobox, supplier_combobox)
    treeview_data(treeview)
    treeview.bind('<ButtonRelease-1>',lambda event:select_data(event, treeview,category_combobox,supplier_combobox,
                                                               name_entry,price_entry,quantity_entry,status_combobox,
                                                               discount_spinbox))