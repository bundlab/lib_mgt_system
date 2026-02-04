# issue_return.py
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
from ttkbootstrap.widgets.tableview import Tableview
from db_connection import connect_db
from datetime import date


class IssueReturn:
    def __init__(self, parent):
        self.parent = parent

        self.frame = tb.Frame(parent, padding=10)
        self.frame.pack(fill="both", expand=True)

        tb.Label(
            self.frame,
            text="Issue / Return Books",
            font=("Arial", 18, "bold"),
            bootstyle=PRIMARY
        ).pack(pady=10)

        form = tb.Frame(self.frame)
        form.pack(pady=10)

        # Book ID
        tb.Label(form, text="Book ID", bootstyle=INFO).grid(row=0, column=0, padx=5, pady=5)
        self.entry_book_id = tb.Entry(form, width=30)
        self.entry_book_id.grid(row=0, column=1, padx=5, pady=5)

        # Member ID
        tb.Label(form, text="Member ID", bootstyle=INFO).grid(row=1, column=0, padx=5, pady=5)
        self.entry_member_id = tb.Entry(form, width=30)
        self.entry_member_id.grid(row=1, column=1, padx=5, pady=5)

        # Buttons
        btns = tb.Frame(self.frame)
        btns.pack(pady=10)

        tb.Button(btns, text="Issue Book", bootstyle=SUCCESS, command=self.issue_book)\
            .grid(row=0, column=0, padx=10)
        tb.Button(btns, text="Return Book", bootstyle=WARNING, command=self.return_book)\
            .grid(row=0, column=1, padx=10)

        # Table
        self.table = Tableview(
            self.frame,
            coldata=[
                {"text": "Issue ID"},
                {"text": "Book ID"},
                {"text": "Member ID"},
                {"text": "Issue Date"},
                {"text": "Return Date"},
                {"text": "Status"},
            ],
            rowdata=self.fetch_issues(),
            paginated=True,
            searchable=True,
            bootstyle=PRIMARY
        )
        self.table.pack(fill="both", expand=True, pady=10)

    # ---------------- DB ----------------
    def fetch_issues(self):
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("""
            SELECT issue_id, book_id, member_id, issue_date, return_date, status
            FROM issued_books
            ORDER BY issue_id DESC
        """)
        rows = cur.fetchall()
        conn.close()
        return rows

    def refresh_table(self):
        self.table.delete_rows()
        rows = self.fetch_issues()
        if rows:
            self.table.insert_rows("end", rows)

    # ---------------- LOGIC ----------------
    def issue_book(self):
        book_id = self.entry_book_id.get().strip()
        member_id = self.entry_member_id.get().strip()

        if not book_id or not member_id:
            Messagebox.show_warning("Missing Data", "Book ID and Member ID are required")
            return

        conn = connect_db()
        cur = conn.cursor()

        # Check quantity
        cur.execute("SELECT quantity FROM books WHERE book_id=%s", (book_id,))
        result = cur.fetchone()

        if not result:
            Messagebox.show_error("Error", "Book not found")
            conn.close()
            return

        if result[0] <= 0:
            Messagebox.show_warning("Unavailable", "No copies available")
            conn.close()
            return

        # Issue book
        cur.execute("""
            INSERT INTO issued_books (book_id, member_id)
            VALUES (%s, %s)
        """, (book_id, member_id))

        cur.execute("""
            UPDATE books SET quantity = quantity - 1
            WHERE book_id=%s
        """, (book_id,))

        conn.commit()
        conn.close()

        self.refresh_table()
        Messagebox.show_info("Success", "Book issued successfully")

    def return_book(self):
        selected = self.table.get_rows(selected=True)

        if not selected:
            Messagebox.show_warning("Select Record", "Select an issued book to return")
            return

        issue_id, book_id, *_ = selected[0].values

        conn = connect_db()
        cur = conn.cursor()

        cur.execute("""
            UPDATE issued_books
            SET return_date=%s, status='RETURNED'
            WHERE issue_id=%s
        """, (date.today(), issue_id))

        cur.execute("""
            UPDATE books SET quantity = quantity + 1
            WHERE book_id=%s
        """, (book_id,))

        conn.commit()
        conn.close()

        self.refresh_table()
        Messagebox.show_info("Returned", "Book returned successfully")
