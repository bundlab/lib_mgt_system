import ttkbootstrap as tb
from ttkbootstrap.constants import *
import psycopg2
from db_connection import connect_db

class Reports:
    def __init__(self, root):
        self.root = root
        self.root.configure(bg="white")

        tb.Label(self.root, text="Library Reports", font=("Arial", 16, "bold"), bootstyle=INVERSE).pack(pady=10)

        # Report Type Selection
        self.report_type = tb.StringVar(value="All Transactions")
        report_options = ["All Transactions", "Issued Books", "Returned Books", "Overdue Books"]

        tb.OptionMenu(self.root, self.report_type, *report_options, command=self.load_report).pack(pady=10)

        # Report Table
        self.report_table = tb.Treeview(self.root, columns=("ID", "Book", "Member", "Issue Date", "Return Date", "Status"), show="headings")
        self.report_table.pack(fill="both", expand=True)

        for col in ("ID", "Book", "Member", "Issue Date", "Return Date", "Status"):
            self.report_table.heading(col, text=col)
            self.report_table.column(col, anchor="center")

        self.load_report()

    def load_report(self, *args):
        report_type = self.report_type.get()

        query = "SELECT issue_id, book_id, member_id, issue_date, return_date, status FROM issued_books"
        if report_type == "Issued Books":
            query += " WHERE status='issued'"
        elif report_type == "Returned Books":
            query += " WHERE status='returned'"
        elif report_type == "Overdue Books":
            query += " WHERE return_date IS NULL AND issue_date < CURRENT_DATE - INTERVAL '30 days'"

        conn = connect_db()
        if conn:
            cur = conn.cursor()
            cur.execute(query)
            records = cur.fetchall()
            conn.close()

            # Clear existing table data
            for row in self.report_table.get_children():
                self.report_table.delete(row)

            for record in records:
                self.report_table.insert("", "end", values=record)
