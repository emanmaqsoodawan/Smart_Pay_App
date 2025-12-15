import tkinter as tk
from tkinter import messagebox
import datetime
from transaction_controller import TransactionController
from user_controller import UserController

class SendMoneyWindow:
    def __init__(self, root, sender_id, on_close_callback):
        self.root = root
        self.sender_id = sender_id
        self.on_close_callback = on_close_callback
        self.root.title("Send Money")
        self.root.geometry("400x350")
        
        self.setup_ui()

    def setup_ui(self):
        tk.Label(self.root, text="Send Money", font=("Arial", 16, "bold")).pack(pady=20)

        # Receiver Username
        tk.Label(self.root, text="Receiver Username").pack()
        self.entry_receiver = tk.Entry(self.root)
        self.entry_receiver.pack()

        # Amount
        tk.Label(self.root, text="Amount to Transfer").pack(pady=(10, 0))
        self.entry_amount = tk.Entry(self.root)
        self.entry_amount.pack()

        # Transfer Button
        tk.Button(self.root, text="Transfer Funds", command=self.process_transfer, bg="#FFC107", fg="black", width=20, pady=5).pack(pady=30)
        
        tk.Label(self.root, text="Note: This will be recorded as an Expense.", fg="gray").pack()

    def process_transfer(self):
        receiver_name = self.entry_receiver.get()
        amount_str = self.entry_amount.get()

        if not receiver_name or not amount_str:
            messagebox.showwarning("Missing Input", "Please fill all fields")
            return

        try:
            amount = float(amount_str)
            if amount <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Amount", "Please enter a valid positive number.")
            return

        # 1. Validate Receiver
        receiver_id = UserController.get_user_id_by_username(receiver_name)
        if not receiver_id:
             messagebox.showerror("User Not Found", f"User '{receiver_name}' does not exist.")
             return
        
        if receiver_id == self.sender_id:
            messagebox.showerror("Error", "You cannot send money to yourself.")
            return

        # 2. Confirm
        confirm = messagebox.askyesno("Confirm Transfer", f"Send Pkr {amount:,.2f} to {receiver_name}?")
        if not confirm:
            return

        # 3. Process
        date_str = datetime.date.today().strftime("%Y-%m-%d")
        success, msg = TransactionController.process_transfer(self.sender_id, receiver_id, amount, date_str)

        if success:
            msg = f"Successfully sent Pkr {amount:,.2f} to {receiver_name}!"
            
            # Ask for Receipt
            if messagebox.askyesno("Success", msg + "\n\nDo you want to download the receipt?"):
                try:
                    from utils import generate_pdf_receipt
                    import os
                    # Dummy ID for now or fetch latest ID? 
                    # Ideally backend returns trans ID. For now using timestamp/random or just 'New'
                    details = {
                        "id": "NEW", 
                        "sender": "Me", 
                        "receiver": receiver_name, 
                        "amount": amount, 
                        "date": date_str
                    }
                    path = generate_pdf_receipt(details)
                    messagebox.showinfo("Receipt Saved", f"Receipt saved at:\n{path}")
                    # Open the file
                    os.startfile(path)
                except Exception as e:
                    messagebox.showerror("Receipt Error", f"Could not generate PDF: {e}")

            if self.on_close_callback:
                self.on_close_callback()
            self.root.destroy()
        else:
            messagebox.showerror("Transfer Failed", msg)
