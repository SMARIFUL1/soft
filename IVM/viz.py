from tkinter import *
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from IVM.employees import connect_database

def fetch_columns():
    """Fetch column names from the database."""
    cursor, connection = connect_database()
    if not cursor or not connection:
        return []

    try:
        cursor.execute("USE inventory_system")
        cursor.execute("DESCRIBE product_data")
        columns = [row[0] for row in cursor.fetchall()]  # Get column names
        return columns
    except Exception as e:
        messagebox.showerror("Error", str(e))
        return []
    finally:
        cursor.close()
        connection.close()

def column_button_clicked(column_name, window):
    """Handle button click for a specific column."""
    messagebox.showinfo("Info", f"You clicked on column: {column_name}")
    # Perform actions like sorting or filtering here
    visualize_column_data(column_name, window)


def visualize_column_data(column_name, window):
    """Visualize data based on the selected column."""
    cursor, connection = connect_database()
    if not cursor or not connection:
        return

    try:
        cursor.execute("USE inventory_system")
        cursor.execute(f"SELECT {column_name}, COUNT(*) FROM product_data GROUP BY {column_name}")
        data = cursor.fetchall()

        # Process data for visualization
        labels = [row[0] for row in data]
        counts = [row[1] for row in data]

        # Create the plot
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.bar(labels, counts, color='orange')
        ax.set_title(f'Distribution of {column_name}')
        ax.set_xlabel(column_name)
        ax.set_ylabel('Count')
        ax.tick_params(axis='x', rotation=45)

        # Embed the plot in Tkinter
        chart_frame = Frame(window, bg='white', width=600, height=400)
        chart_frame.place(x=200, y=300)

        canvas = FigureCanvasTkAgg(fig, master=chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=BOTH, expand=1)

    except Exception as e:
        messagebox.showerror("Error", str(e))
    finally:
        cursor.close()
        connection.close()


def sales_form(window):
    """Main form for sales with dynamic column buttons."""
    sales_frame = Frame(window, width=1100, height=600, bg='white')
    sales_frame.place(x=200, y=100)
    heading_label = Label(sales_frame, text="Sales Dashboard", font=("Arial", 15, 'bold'),
                          bg="#0f4d7d", fg="white")
    heading_label.place(x=0, y=0, relwidth=1)

    back_button = Button(sales_frame, text="Back", cursor="hand2", bg='white',
                         command=lambda: sales_frame.place_forget())
    back_button.place(x=10, y=30)

    # Fetch column names
    columns = fetch_columns()

    # Create buttons dynamically for each column
    button_frame = Frame(sales_frame, bg='white')
    button_frame.place(x=10, y=60)

    for idx, column in enumerate(columns):
        btn = Button(button_frame, text=column, font=("Times New Roman", 12),
                     bg="#0f4d7d", fg="white", cursor="hand2",
                     command=lambda col=column: column_button_clicked(col, window))
        btn.grid(row=0, column=idx, padx=5, pady=10)

    visualize_column_data(column,window)