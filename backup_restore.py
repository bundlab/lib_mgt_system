import ttkbootstrap as tb
from ttkbootstrap.constants import *
import os
import subprocess
from tkinter import filedialog
from db_connection import DB_NAME, DB_USER, DB_PASSWORD

class BackupRestore:
    def __init__(self, root):
        self.root = root
        self.root.configure(bg="white")

        tb.Label(self.root, text="Backup & Restore Database", font=("Arial", 16, "bold"), bootstyle=INVERSE).pack(pady=10)

        tb.Button(self.root, text="Backup Database", bootstyle=SUCCESS, command=self.backup_database).pack(pady=10)
        tb.Button(self.root, text="Restore Database", bootstyle=WARNING, command=self.restore_database).pack(pady=10)

    def backup_database(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".sql", filetypes=[("SQL Files", "*.sql")])
        if file_path:
            command = f"pg_dump -U {DB_USER} -W {DB_PASSWORD} -F c -d {DB_NAME} -f {file_path}"
            os.system(command)
            tb.Messagebox.show_info("Backup Successful", "Database backup created successfully!")

    def restore_database(self):
        file_path = filedialog.askopenfilename(filetypes=[("SQL Files", "*.sql")])
        if file_path:
            command = f"pg_restore -U {DB_USER} -W {DB_PASSWORD} -d {DB_NAME} -F c {file_path}"
            os.system(command)
            tb.Messagebox.show_info("Restore Successful", "Database restored successfully!")
