from datetime import datetime
import psycopg2
from twilio.rest import Client
from db_connection import connect_db

# Twilio credentials (replace with your own or store in environment variables)
TWILIO_ACCOUNT_SID = 'your_account_sid'
TWILIO_AUTH_TOKEN = 'your_auth_token'
TWILIO_PHONE_NUMBER = '+1234567890'  # Twilio phone number

# Initialize Twilio client
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def send_sms(to, message):
    try:
        client.messages.create(
            body=message,
            from_=TWILIO_PHONE_NUMBER,
            to=to
        )
        print(f"SMS sent to {to}")
    except Exception as e:
        print(f"Failed to send SMS to {to}: {str(e)}")

def notify_overdue_users():
    conn = connect_db()
    cur = conn.cursor()
    
    today = datetime.today().date()

    query = """
    SELECT u.username, u.phone, b.title, l.due_date
    FROM loans l
    JOIN users u ON l.user_id = u.id
    JOIN books b ON l.book_id = b.id
    WHERE l.due_date < %s AND l.returned = FALSE;
    """

    cur.execute(query, (today,))
    overdue_records = cur.fetchall()

    for username, phone, book_title, due_date in overdue_records:
        if phone:
            message = f"Hi {username}, your book '{book_title}' was due on {due_date}. Please return it to avoid penalties."
            send_sms(phone, message)

    cur.close()
    conn.close()

if __name__ == "__main__":
    notify_overdue_users()
