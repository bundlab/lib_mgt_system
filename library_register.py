import ttkbootstrap as tb
from ttkbootstrap.constants import *
import psycopg2
from db_connection import connect_db

class LibraryRegister:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System - Register")
        self.root.geometry("400x450")
        self.root.configure(bg="#2C3E50")

        tb.Label(self.root, text="Library Registration", font=("Arial", 16, "bold"), background="#2C3E50", fg="white").pack(pady=20)

        tb.Label(self.root, text="Username:", font=("Arial", 12), background="#2C3E50", fg="white").pack()
        self.username_entry = tb.Entry(self.root, width=30)
        self.username_entry.pack(pady=5)

        tb.Label(self.root, text="Password:", font=("Arial", 12), background="#2C3E50", fg="white").pack()
        self.password_entry = tb.Entry(self.root, width=30, show="*")
        self.password_entry.pack(pady=5)

        tb.Label(self.root, text="Role (admin/librarian):", font=("Arial", 12), bg="#2C3E50", fg="white").pack()
        self.role_entry = tb.Entry(self.root, width=30)
        self.role_entry.pack(pady=5)

        tb.Button(self.root, text="Register", font=("Arial", 12, "bold"), bg="#27AE60", fg="white", command=self.register).pack(pady=10)
        tb.Button(self.root, text="Back to Login", font=("Arial", 10), bg="#2980B9", fg="white", command=self.back_to_login).pack()

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        role = self.role_entry.get().lower()

        if role not in ["admin", "librarian"]:
            tb.messagebox.showerror("Error", "Role must be 'admin' or 'librarian'")
            return

        conn = connect_db()
        if conn:
            cur = conn.cursor()
            try:
                cur.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)", (username, password, role))
                conn.commit()
                tb.messagebox.showinfo("Success", "Registration Successful!")
                self.root.destroy()
                import library_login  # Go back to login
            except psycopg2.IntegrityError:
                tb.messagebox.showerror("Error", "Username already exists")
            conn.close()
        else:
            tb.messagebox.showerror("Error", "Database Connection Failed!")

    def back_to_login(self):
        self.root.destroy()
        import library_login  # Go back to login screen

if __name__ == "__main__":
    root = tb.Window(themename="darkly")
    LibraryRegister(root)
    root.mainloop()