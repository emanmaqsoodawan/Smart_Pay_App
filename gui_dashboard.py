import tkinter as tk
from tkinter import messagebox
from transaction_controller import TransactionController
from gui_transactions import AddTransactionWindow, ViewTransactionsWindow
from gui_transfer import SendMoneyWindow

class DashboardWindow:
    def __init__(self, root, user_data, on_logout):
        self.root = root
        self.user_data = user_data
        self.on_logout = on_logout
        self.root.title(f"Smart Pay App - Dashboard ({user_data['username']})")
        self.root.geometry("500x400")

        self.setup_ui()

    def setup_ui(self):
        # Header
        # Header
        tk.Label(self.root, text=f"Welcome, {self.user_data['username']}", font=("Arial", 18)).pack(pady=(20, 5))
        
        # Account Display & QR Code
        acc_num = self.user_data.get('account_number', 'N/A')
        tk.Label(self.root, text=f"Account #: {acc_num}", font=("Arial", 12), fg="gray").pack(pady=(0, 10))

        # QR Code
        try:
            from utils import generate_qr_code
            from PIL import ImageTk
            
            # Generate QR
            qr_img = generate_qr_code(acc_num)
            qr_img = qr_img.resize((100, 100)) # Resize for dashboard
            self.qr_photo = ImageTk.PhotoImage(qr_img)
            
            lbl_qr = tk.Label(self.root, image=self.qr_photo)
            lbl_qr.pack(pady=5)
            tk.Label(self.root, text="Scan to Pay", font=("Arial", 8), fg="gray").pack()
        except Exception as e:
            print(f"QR Error: {e}")

        # Balance Display
        self.lbl_balance = tk.Label(self.root, text="Current Balance: Loading...", font=("Arial", 14, "bold"), fg="green")
        self.lbl_balance.pack(pady=10)
        self.update_balance()

        # Action Buttons
        frame_buttons = tk.Frame(self.root)
        frame_buttons.pack(pady=20)

        tk.Button(frame_buttons, text="Add Transaction", command=self.open_add_transaction, width=20, bg="#2196F3", fg="white").grid(row=0, column=0, padx=10, pady=5)
        tk.Button(frame_buttons, text="View History", command=self.open_view_transactions, width=20, bg="#FF9800", fg="white").grid(row=0, column=1, padx=10, pady=5)
        tk.Button(frame_buttons, text="Send Money", command=self.open_send_money, width=20, bg="#9C27B0", fg="white").grid(row=1, column=0, columnspan=2, pady=10)
        
        # Refresh Button
        tk.Button(self.root, text="Refresh Balance", command=self.update_balance).pack(pady=5)

        # Logout
        tk.Button(self.root, text="Logout", command=self.on_logout, bg="#f44336", fg="white").pack(pady=20)

    def update_balance(self):
        balance = TransactionController.get_balance(self.user_data['user_id'])
        self.lbl_balance.config(text=f"Current Balance: ${balance:,.2f}")

    def open_add_transaction(self):
        top = tk.Toplevel(self.root)
        AddTransactionWindow(top, self.user_data['user_id'], self.update_balance)

    def open_view_transactions(self):
        top = tk.Toplevel(self.root)
        ViewTransactionsWindow(top, self.user_data['user_id'])

    def open_send_money(self):
        top = tk.Toplevel(self.root)
        SendMoneyWindow(top, self.user_data['user_id'], self.update_balance)
