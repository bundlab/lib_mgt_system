# 📚 Library Management System (Tkinter + PostgreSQL)

A modern and professional **Library Management System** built with **Python**, **Tkinter**, **ttkbootstrap**, and **PostgreSQL**, featuring a clean GUI dashboard, role-based access control, and full book/member management.

---

## 🚀 Features

### ✅ Role-Based Dashboard
- **Admin Panel**
- **Librarian Panel**
- **User Panel**

Each role has access to specific modules and controls.

---

### 📘 Book Management
- Add new books
- Update book records
- Delete books
- Search and pagination support
- Prevent duplicate ISBN entries

---

### 👥 Member Management
- Register new library members
- Update member details
- Delete members
- Faculty & Department tracking

---

### 🔄 Issue & Return System
- Issue books to members
- Return issued books
- Prevent duplicate active issuing
- View all issued/returned history

---

### 🎨 Modern GUI Design
- Powered by **ttkbootstrap**
- Sidebar navigation with icons
- Profile card + Logout button
- Responsive layout

---

## 🛠️ Technologies Used

| Tool/Library | Purpose |
|-------------|---------|
| Python 3.12 | Core Language |
| Tkinter | GUI Framework |
| ttkbootstrap | Modern UI Styling |
| PostgreSQL | Database Backend |
| psycopg2 | PostgreSQL Connector |
| Pillow (PIL) | Image Support |

---

## 📂 Project Structure

```bash
lib_mgt_system/
│
├── assets/
│   ├── library.png
│   ├── watermark.jpg
│
├── book_management.py
├── member_management.py
├── issue_return.py
├── library_dashboard.py
├── db_connection.py
│
├── requirements.txt
├── README.md
└── venv/
