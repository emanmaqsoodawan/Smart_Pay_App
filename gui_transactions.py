import tkinter as tk
from tkinter import ttk, messagebox

from transaction_controller import TransactionController
# Note: If tkcalendar is not installed, we can fall back to a simple Entry for date, 
# but for "Professional and clean GUI", libraries like tkcalendar are preferred.
# I will use a simple Entry with YYYY-MM-DD validation if import fails to avoid dependency hell for the user 
# unless they installed it, but assuming standard lib or simple requirements:
# Let's stick to standard Entry for date to be safe and compatible without extra pip installs if not requested.
import datetime

class AddTransactionWindow:
    def __init__(self, root, user_id, on_close_callback):
        self.root = root
        self.user_id = user_id
        self.on_close_callback = on_close_callback
        self.root.title("Add Transaction")
        self.root.geometry("400x450")

        self.categories = TransactionController.get_categories()
        # Convert categories to a dict for easy lookup
        self.cat_dict = {cat['name']: cat['id'] for cat in self.categories}
        self.cat_names = list(self.cat_dict.keys())

        self.setup_ui()

    def setup_ui(self):
        tk.Label(self.root, text="Add Income / Expense", font=("Arial", 16, "bold")).pack(pady=15)

        tk.Label(self.root, text="Type").pack()
        self.var_type = tk.StringVar(value="Expense")
        tk.Radiobutton(self.root, text="Expense", variable=self.var_type, value="Expense").pack()
        tk.Radiobutton(self.root, text="Income", variable=self.var_type, value="Income").pack()

        tk.Label(self.root, text="Category").pack(pady=(10,0))
        self.combo_category = ttk.Combobox(self.root, values=self.cat_names, state="readonly")
        self.combo_category.pack()

        tk.Label(self.root, text="Amount").pack(pady=(10,0))
        self.entry_amount = tk.Entry(self.root)
        self.entry_amount.pack()

        tk.Label(self.root, text="Date (YYYY-MM-DD)").pack(pady=(10,0))
        self.entry_date = tk.Entry(self.root)
        self.entry_date.insert(0, datetime.date.today().strftime("%Y-%m-%d"))
        self.entry_date.pack()

        tk.Label(self.root, text="Description (Optional)").pack(pady=(10,0))
        self.entry_desc = tk.Entry(self.root)
        self.entry_desc.pack()

        tk.Button(self.root, text="Save Transaction", command=self.save_transaction, bg="#4CAF50", fg="white", width=20).pack(pady=30)

    def save_transaction(self):
        trans_type = self.var_type.get()
        cat_name = self.combo_category.get()
        amount = self.entry_amount.get()
        date_str = self.entry_date.get()
        description = self.entry_desc.get()

        if not cat_name or not amount or not date_str:
            messagebox.showwarning("Missing Input", "Please fill all fields")
            return

        try:
            amount_val = float(amount)
        except ValueError:
            messagebox.showerror("Invalid Input", "Amount must be a number")
            return

        cat_id = self.cat_dict.get(cat_name)
        if not cat_id:
             messagebox.showerror("Error", "Invalid Category")
             return

        success, message = TransactionController.add_transaction(self.user_id, cat_id, amount_val, trans_type, date_str, description)
        if success:
            messagebox.showinfo("Success", message)
            if self.on_close_callback:
                self.on_close_callback()
            self.root.destroy()
        else:
            messagebox.showerror("Error", message)

class ViewTransactionsWindow:
    def __init__(self, root, user_id):
        self.root = root
        self.user_id = user_id
        self.root.title("Transaction History")
        self.root.geometry("800x450") # Widened for Description

        tk.Label(self.root, text="Your Transaction History", font=("Arial", 14, "bold")).pack(pady=10)

        # Table Frame
        frame_table = tk.Frame(self.root)
        frame_table.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        columns = ("ID", "Category", "Amount", "Type", "Date", "Description")
        self.tree = ttk.Treeview(frame_table, columns=columns, show="headings")
        
        # Define headings
        self.tree.heading("ID", text="ID")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Amount", text="Amount")
        self.tree.heading("Type", text="Type")
        self.tree.heading("Date", text="Date")
        self.tree.heading("Description", text="Description")

        # Column configuration
        self.tree.column("ID", width=40, anchor=tk.CENTER)
        self.tree.column("Category", width=100, anchor=tk.W)
        self.tree.column("Amount", width=80, anchor=tk.E)
        self.tree.column("Type", width=60, anchor=tk.CENTER)
        self.tree.column("Date", width=80, anchor=tk.CENTER)
        self.tree.column("Description", width=200, anchor=tk.W)

        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_table, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Download Button
        tk.Button(self.root, text="Download Receipt for Selected", command=self.download_receipt, bg="#607D8B", fg="white").pack(pady=10)

        self.load_data()

    def download_receipt(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Select Transaction", "Please select a transaction to download receipt.")
            return

        # Get values: ID, Category, Amount, Type, Date, Description
        values = self.tree.item(selected_item, "values")
        
        # Remove '$' and ',' from amount
        try:
            amount_clean = float(values[2].replace('$', '').replace(',', ''))
        except:
            amount_clean = 0.0
        
        desc = values[5]
        sender = "N/A"
        receiver = "Me" # Default if income
        
        # Logic to extract sender/receiver from Description
        if "Received from" in desc:
            sender = desc.replace("Received from", "").strip()
            receiver = "Me"
        elif "Sent to" in desc:
            sender = "Me"
            receiver = desc.replace("Sent to", "").strip()
        else:
            # Generic transaction
            if values[3] == 'Income':
                sender = "Source: " + values[1] # Category as sender
            else:
                receiver = "Merchant: " + values[1] # Category as receiver
        
        details = {
            "id": values[0],
            "date": values[4],
            "sender": sender,
            "receiver": receiver,
            "amount": amount_clean,
        }

        try:
            from utils import generate_pdf_receipt
            import os
            path = generate_pdf_receipt(details)
            if messagebox.askyesno("Receipt Saved", f"Receipt saved at:\n{path}\n\nOpen it now?"):
                os.startfile(path)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate PDF: {e}")

    def load_data(self):
        rows = TransactionController.get_user_transactions(self.user_id)
        for row in rows:
            # row: trans_id, category_name, amount, trans_type, trans_date, description
            # Ensure we handle potential None in description
            desc = row[5] if row[5] else ""
            self.tree.insert("", tk.END, values=(row[0], row[1], f"${row[2]:,.2f}", row[3], row[4], desc))
