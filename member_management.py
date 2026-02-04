# member_management.py
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap.widgets.tableview import Tableview
from ttkbootstrap.dialogs import Messagebox
from tkinter import END
from db_connection import connect_db


class MemberManagement:
    def __init__(self, parent):
        self.parent = parent
        self.selected_member_id = None

        # Main container for this module
        self.frame = tb.Frame(parent, padding=10)
        self.frame.pack(fill="both", expand=True)

        # Title
        tb.Label(
            self.frame,
            text="Manage Members",
            font=("Arial", 18, "bold"),
            bootstyle=PRIMARY
        ).pack(pady=15)

        # Form Frame
        form_frame = tb.Frame(self.frame)
        form_frame.pack(pady=10)

        # Name
        tb.Label(form_frame, text="Name:", bootstyle=INFO).grid(row=0, column=0, sticky="e", padx=10, pady=5)
        self.entry_name = tb.Entry(form_frame, width=40)
        self.entry_name.grid(row=0, column=1, padx=10, pady=5)

        # Email
        tb.Label(form_frame, text="Email:", bootstyle=INFO).grid(row=1, column=0, sticky="e", padx=10, pady=5)
        self.entry_email = tb.Entry(form_frame, width=40)
        self.entry_email.grid(row=1, column=1, padx=10, pady=5)

        # Phone
        tb.Label(form_frame, text="Phone:", bootstyle=INFO).grid(row=2, column=0, sticky="e", padx=10, pady=5)
        self.entry_phone = tb.Entry(form_frame, width=40)
        self.entry_phone.grid(row=2, column=1, padx=10, pady=5)

        # Faculty
        tb.Label(form_frame, text="Faculty:", bootstyle=INFO).grid(row=3, column=0, sticky="e", padx=10, pady=5)
        self.entry_faculty = tb.Entry(form_frame, width=40)
        self.entry_faculty.grid(row=3, column=1, padx=10, pady=5)

        # Department
        tb.Label(form_frame, text="Department:", bootstyle=INFO).grid(row=4, column=0, sticky="e", padx=10, pady=5)
        self.entry_department = tb.Entry(form_frame, width=40)
        self.entry_department.grid(row=4, column=1, padx=10, pady=5)

        # Buttons
        btn_frame = tb.Frame(self.frame)
        btn_frame.pack(pady=15)

        tb.Button(btn_frame, text="Add Member", bootstyle=SUCCESS, command=self.add_member).grid(row=0, column=0, padx=10)
        tb.Button(btn_frame, text="Update Member", bootstyle=WARNING, command=self.update_member).grid(row=0, column=1, padx=10)
        tb.Button(btn_frame, text="Delete Member", bootstyle=DANGER, command=self.delete_member).grid(row=0, column=2, padx=10)
        tb.Button(btn_frame, text="Clear Form", bootstyle=SECONDARY, command=self.clear_form).grid(row=0, column=3, padx=10)

        # Table
        self.setup_table()

    # ---------------- TABLE ---------------- #

    def setup_table(self):
        self.table = Tableview(
            self.frame,
            coldata=[
                {"text": "ID", "stretch": False},
                {"text": "Name"},
                {"text": "Email"},
                {"text": "Phone"},
                {"text": "Faculty"},
                {"text": "Department"},
            ],
            rowdata=self.fetch_members(),
            paginated=True,
            searchable=True,
            bootstyle=PRIMARY
        )
        self.table.pack(fill="both", expand=True, pady=10)
        self.table.view.bind("<<TreeviewSelect>>", self.on_member_select)

    def fetch_members(self):
        try:
            conn = connect_db()
            cur = conn.cursor()
            cur.execute("""
                SELECT member_id, name, email, phone, faculty, department
                FROM members
                ORDER BY member_id
            """)
            rows = cur.fetchall()
            conn.close()
            return rows
        except Exception as e:
            Messagebox.show_error("Database Error", str(e))
            return []

    # ---------------- EVENTS ---------------- #

    def on_member_select(self, event=None):
        selected = self.table.get_rows(selected=True)
        if not selected:
            return

        row = selected[0]
        self.selected_member_id = row.values[0]

        self.entry_name.delete(0, END)
        self.entry_name.insert(0, row.values[1])
        self.entry_email.delete(0, END)
        self.entry_email.insert(0, row.values[2])
        self.entry_phone.delete(0, END)
        self.entry_phone.insert(0, row.values[3])
        self.entry_faculty.delete(0, END)
        self.entry_faculty.insert(0, row.values[4])
        self.entry_department.delete(0, END)
        self.entry_department.insert(0, row.values[5])

    # ---------------- CRUD ---------------- #

    def add_member(self):
        data = self.get_form_data()
        if not data:
            return

        try:
            conn = connect_db()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO members (name, email, phone, faculty, department) VALUES (%s, %s, %s, %s, %s)",
                data
            )
            conn.commit()
            conn.close()

            self.refresh_table()
            self.clear_form()
            Messagebox.show_info("Success", "Member added successfully!")
        except Exception as e:
            Messagebox.show_error("Error", str(e))

    def update_member(self):
        if not self.selected_member_id:
            Messagebox.show_warning("Select Member", "Please select a member to update.")
            return

        data = self.get_form_data()
        if not data:
            return

        try:
            conn = connect_db()
            cur = conn.cursor()
            cur.execute(
                """
                UPDATE members
                SET name=%s, email=%s, phone=%s, faculty=%s, department=%s
                WHERE member_id=%s
                """,
                (*data, self.selected_member_id)
            )
            conn.commit()
            conn.close()

            self.refresh_table()
            self.clear_form()
            Messagebox.show_info("Updated", "Member updated successfully!")
        except Exception as e:
            Messagebox.show_error("Error", str(e))

    def delete_member(self):
        if not self.selected_member_id:
            Messagebox.show_warning("Select Member", "Please select a member to delete.")
            return

        if not Messagebox.yesno("Confirm", "Delete selected member?"):
            return

        try:
            conn = connect_db()
            cur = conn.cursor()
            cur.execute("DELETE FROM members WHERE member_id=%s", (self.selected_member_id,))
            conn.commit()
            conn.close()

            self.refresh_table()
            self.clear_form()
            Messagebox.show_info("Deleted", "Member deleted successfully!")
        except Exception as e:
            Messagebox.show_error("Error", str(e))

    # ---------------- HELPERS ---------------- #

    def get_form_data(self):
        values = (
            self.entry_name.get().strip(),
            self.entry_email.get().strip(),
            self.entry_phone.get().strip(),
            self.entry_faculty.get().strip(),
            self.entry_department.get().strip(),
        )
        if not all(values):
            Messagebox.show_warning("Input Error", "All fields are required.")
            return None
        return values

    def clear_form(self):
        for entry in (
            self.entry_name,
            self.entry_email,
            self.entry_phone,
            self.entry_faculty,
            self.entry_department,
        ):
            entry.delete(0, END)
        self.selected_member_id = None

    def refresh_table(self):
        self.table.destroy()
        self.setup_table()
