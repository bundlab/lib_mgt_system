import smtplib
import psycopg2
from email.mime.text import MIMEText
from db_connection import connect_db

SMTP_SERVER = "smtp.yourmail.com"
SMTP_PORT = 587
EMAIL_SENDER = "library@yourdomain.com"
EMAIL_PASSWORD = "yourpassword"

def send_overdue_notifications():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT users.email, books.title, issued_books.return_date 
        FROM issued_books
        JOIN users ON issued_books.member_id = users.id
        JOIN books ON issued_books.book_id = books.id
        WHERE issued_books.status='issued' AND issued_books.return_date < CURRENT_DATE
    """)
    overdue_books = cur.fetchall()
    conn.close()

    for email, book_title, return_date in overdue_books:
        message = MIMEText(f"Dear User,\n\nThe book '{book_title}' was due on {return_date}. Please return it immediately.\n\nLibrary Team")
        message["Subject"] = "Overdue Book Reminder"
        message["From"] = EMAIL_SENDER
        message["To"] = email

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, email, message.as_string())

if __name__ == "__main__":
    send_overdue_notifications()
