# book_management.py
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
from ttkbootstrap.widgets.tableview import Tableview
from tkinter import END
from db_connection import connect_db


class BookManagement:
    def __init__(self, parent):
        self.parent = parent
        self.selected_book_id = None
        self.user_selecting = False

        self.frame = tb.Frame(parent, padding=10)
        self.frame.pack(fill="both", expand=True)

        # Title
        tb.Label(
            self.frame,
            text="Book Management",
            font=("Arial", 18, "bold"),
            bootstyle=PRIMARY
        ).pack(pady=10)

        # ================= FORM =================
        form = tb.Frame(self.frame)
        form.pack(pady=10)

        self.entry_title = self._field(form, "Title", 0)
        self.entry_author = self._field(form, "Author", 1)
        self.entry_isbn = self._field(form, "ISBN", 2)
        self.entry_quantity = self._field(form, "Quantity", 3)

        # ================= BUTTONS =================
        btns = tb.Frame(self.frame)
        btns.pack(pady=10)

        tb.Button(btns, text="Add Book", bootstyle=SUCCESS, command=self.add_book).grid(row=0, column=0, padx=5)
        tb.Button(btns, text="Update Book", bootstyle=WARNING, command=self.update_book).grid(row=0, column=1, padx=5)
        tb.Button(btns, text="Delete Book", bootstyle=DANGER, command=self.delete_book).grid(row=0, column=2, padx=5)
        tb.Button(btns, text="Clear", bootstyle=SECONDARY, command=self.clear_form).grid(row=0, column=3, padx=5)

        # ================= TABLE =================
        self.table = Tableview(
            self.frame,
            coldata=[
                {"text": "ID", "stretch": False},
                {"text": "Title"},
                {"text": "Author"},
                {"text": "ISBN"},
                {"text": "Quantity"},
            ],
            rowdata=self.fetch_books(),
            paginated=True,
            searchable=True,
            bootstyle=PRIMARY
        )
        self.table.pack(fill="both", expand=True, pady=10)
        self.table.view.bind("<ButtonRelease-1>", self._user_clicked)
        self.table.view.bind("<<TreeviewSelect>>", self.on_select)


    # ---------- helpers ----------
    def _user_clicked(self, _):
        self.user_selecting = True

    def _field(self, parent, label, row):
        tb.Label(parent, text=label, bootstyle=INFO).grid(row=row, column=0, sticky="e", padx=5, pady=5)
        entry = tb.Entry(parent, width=40)
        entry.grid(row=row, column=1, padx=5, pady=5)
        return entry

    # ---------- DB ----------
    def fetch_books(self):
        try:
            with connect_db() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT book_id, title, author, isbn, quantity
                        FROM books
                        ORDER BY book_id
                    """)
                    return cur.fetchall()

        except Exception as e:
            Messagebox.show_error("Database Error", str(e))
            return []


    def refresh_table(self):
        try:
            self.user_selecting = False
            self.table.load_table_data(self.fetch_books())
        except Exception as e:
            Messagebox.show_error("UI Error", str(e))


    # ---------- EVENTS ----------
    def on_select(self, _):
        if not self.user_selecting:
            return

        row = self.table.get_rows(selected=True)
        if not row:
            return

        r = row[0].values
        self.selected_book_id = r[0]

        self.entry_title.delete(0, END)
        self.entry_title.insert(0, r[1])

        self.entry_author.delete(0, END)
        self.entry_author.insert(0, r[2])

        self.entry_isbn.delete(0, END)
        self.entry_isbn.insert(0, r[3])

        self.entry_quantity.delete(0, END)
        self.entry_quantity.insert(0, r[4])


    def add_book(self):
        title = self.entry_title.get().strip()
        author = self.entry_author.get().strip()
        isbn = self.entry_isbn.get().strip()
        quantity = self.entry_quantity.get().strip()

        if not all([title, author, isbn, quantity]):
            Messagebox.show_warning("Missing Data", "All fields are required!")
            return

        try:
            quantity = int(quantity)
        except ValueError:
            Messagebox.show_error("Invalid Quantity", "Quantity must be a number")
            return

        try:
            with connect_db() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        "INSERT INTO books (title, author, isbn, quantity) VALUES (%s,%s,%s,%s)",
                        (title, author, isbn, quantity)
                    )
                conn.commit()

            self.refresh_table()
            self.clear_form()
            Messagebox.show_info("Success", "Book added successfully!")

        except Exception as e:
            if "unique" in str(e).lower():
                Messagebox.show_error(
                    "Duplicate ISBN",
                    "A book with this ISBN already exists."
                )
            else:
                Messagebox.show_error("Database Error", str(e))


    def update_book(self):
        if not self.selected_book_id:
            Messagebox.show_warning("Select Book", "No book selected")
            return

        conn = connect_db()
        cur = conn.cursor()
        cur.execute("""
            UPDATE books
            SET title=%s, author=%s, isbn=%s, quantity=%s
            WHERE book_id=%s
        """, (
            self.entry_title.get(),
            self.entry_author.get(),
            self.entry_isbn.get(),
            self.entry_quantity.get(),
            self.selected_book_id
        ))
        conn.commit()
        conn.close()
        self.refresh_table()

    def delete_book(self):
        if not self.selected_book_id:
            return

        conn = connect_db()
        cur = conn.cursor()
        cur.execute("DELETE FROM books WHERE book_id=%s", (self.selected_book_id,))
        conn.commit()
        conn.close()
        self.refresh_table()
        self.clear_form()

    def clear_form(self):
        for e in (
            self.entry_title,
            self.entry_author,
            self.entry_isbn,
            self.entry_quantity
        ):
            e.delete(0, END)
        self.selected_book_id = None
