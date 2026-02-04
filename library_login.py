import ttkbootstrap as tb
from ttkbootstrap.constants import *
import psycopg2
from db_connection import connect_db

class LibraryLogin:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System - Login")
        self.root.geometry("400x400")
        self.root.configure(bg="#2C3E50")

        # Title Label
        tb.Label(self.root, text="Library Login", font=("Arial", 16, "bold"), bootstyle=PRIMARY).pack(pady=20)

        # Username Entry
        tb.Label(self.root, text="Username:", font=("Arial", 12), bootstyle=PRIMARY).pack()
        self.username_entry = tb.Entry(self.root, width=30)
        self.username_entry.pack(pady=5)

        # Password Entry
        tb.Label(self.root, text="Password:", font=("Arial", 12), bootstyle=PRIMARY).pack()
        self.password_entry = tb.Entry(self.root, width=30, show="*")
        self.password_entry.pack(pady=5)

        # Login Button
        tb.Button(self.root, text="Login", font=("Arial", 12, "bold"), bootstyle=PRIMARY, command=self.login).pack(pady=10)

        # Register Button
        tb.Button(self.root, text="Register", font=("Arial", 10), bootstyle=SUCCESS, command=self.register_window).pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        conn = connect_db()
        if conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
            user = cur.fetchone()
            conn.close()

            if user:
                tb.messagebox.showinfo("Success", "Login Successful!")
                self.root.destroy()
                import library_dashboard  # Open the dashboard
            else:
                tb.messagebox.showerror("Error", "Invalid Username or Password")
        else:
            tb.messagebox.showerror("Error", "Database Connection Failed!")

    def register_window(self):
        self.root.destroy()
        import library_register  # Open registration form

if __name__ == "__main__":
   root = tb.Window(themename="darkly")  # Use any ttkbootstrap theme
   app = LibraryLogin(root)
   root.mainloop()