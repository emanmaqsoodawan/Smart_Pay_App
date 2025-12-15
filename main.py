import tkinter as tk
from gui_auth import LoginWindow
from gui_dashboard import DashboardWindow

class SmartPayApp:
    def __init__(self):
        self.root = tk.Tk()
        self.current_window = None
        self.show_login()

    def show_login(self):
        if self.current_window:
            self.current_window.destroy()  # Use destroy on frame/window appropriately
            # If we are reusing root, we clear children. 
            # But LoginWindow uses root directly in my implementation of show_login below... 
            # Let's clean up root's children to be safe as we are doing single-page-app style within one root or toggling.
            # However, my auth logic used Toplevels or root modification.
            # Let's clean the root window widgets
            for widget in self.root.winfo_children():
                widget.destroy()

        # Login Window setup
        LoginWindow(self.root, self.on_login_success)

    def on_login_success(self, user_data):
        # Clear login screen
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Show Dashboard
        DashboardWindow(self.root, user_data, self.logout)

    def logout(self):
        self.show_login()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = SmartPayApp()
    app.run()
