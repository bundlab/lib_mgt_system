import ttkbootstrap as tb
from ttkbootstrap.constants import PRIMARY, SECONDARY, SUCCESS, DANGER, WARNING, INFO, LIGHT, DARK
from tkinter import END
from db_connection import connect_db
from library_dashboard import LibraryDashboard
import psycopg2

class UserAuth:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Login")
        self.root.geometry("400x300")

        tb.Label(root, text="Library Login", font=("Arial", 16, "bold"), bootstyle=PRIMARY).pack(pady=10)

        tb.Label(root, text="Username:", bootstyle=INFO).pack()
        self.username_entry = tb.Entry(root, bootstyle=SUCCESS, width=30)
        self.username_entry.pack()

        tb.Label(root, text="Password:", bootstyle=INFO).pack()
        self.password_entry = tb.Entry(root, show="*", bootstyle=SUCCESS, width=30)
        self.password_entry.pack()

        self.login_btn = tb.Button(root, text="Login", bootstyle=SUCCESS, command=self.login)
        self.login_btn.pack(pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        conn = connect_db()
        cur = conn.cursor()
        cur.execute("SELECT role FROM users WHERE username=%s AND password=%s", (username, password))
        user = cur.fetchone()
        conn.close()

        if user:
            role = user[0]
            self.root.destroy()
            main_root = tb.Window(themename="darkly")
            LibraryDashboard(main_root, role)
            main_root.mainloop()
        else:
            tb.Messagebox.show_error("Login Failed", "Invalid credentials!", bootstyle=DANGER)

if __name__ == "__main__":
    root = tb.Window(themename="darkly")
    UserAuth(root)
    root.mainloop()