import tkinter as tk
from tkinter import messagebox
from user_controller import UserController

class LoginWindow:
    def __init__(self, root, on_login_success):
        self.root = root
        self.on_login_success = on_login_success
        self.root.title("Smart Pay App - Login")
        self.root.geometry("400x350")
        
        tk.Label(root, text="Smart Pay App", font=("Arial", 20, "bold"), pady=20).pack()
        
        tk.Label(root, text="Username").pack()
        self.entry_username = tk.Entry(root)
        self.entry_username.pack()

        tk.Label(root, text="Password").pack(pady=(10, 0))
        self.entry_password = tk.Entry(root, show="*")
        self.entry_password.pack()

        tk.Button(root, text="Login", command=self.login, bg="#4CAF50", fg="white", width=20, pady=5).pack(pady=20)
        tk.Button(root, text="Register New Account", command=self.open_register, width=20).pack()

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        if not username or not password:
            messagebox.showwarning("Input Error", "Please fill all fields")
            return

        user_data, message = UserController.login_user(username, password)
        if user_data:
            messagebox.showinfo("Success", message)
            self.on_login_success(user_data)
        else:
            messagebox.showerror("Error", message)

    def open_register(self):
        top = tk.Toplevel(self.root)
        RegisterWindow(top)

class RegisterWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Register")
        self.root.geometry("300x300")

        tk.Label(root, text="Create Account", font=("Arial", 16, "bold"), pady=10).pack()

        tk.Label(root, text="Username").pack()
        self.entry_username = tk.Entry(root)
        self.entry_username.pack()

        tk.Label(root, text="Password").pack(pady=(10, 0))
        self.entry_password = tk.Entry(root, show="*")
        self.entry_password.pack()

        tk.Button(root, text="Register", command=self.register, bg="#008CBA", fg="white", width=15, pady=5).pack(pady=20)

    def register(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        if not username or not password:
            messagebox.showwarning("Input Error", "Please fill all fields")
            return

        success, message = UserController.register_user(username, password)
        if success:
            messagebox.showinfo("Success", message)
            self.root.destroy()
        else:
            messagebox.showerror("Error", message)
