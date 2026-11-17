# 🎓 Student Record Management System

A web-based Student Record Management System developed using **Python, Streamlit, SQLite, and Pandas**. The application provides a simple, interactive dashboard for managing student information through CRUD (Create, Read, Update, Delete) operations.

## ✨ Features

- **Interactive Dashboard** – View total students, courses, and average student age.
- **Add Students** – Register new students with their details.
- **View Records** – Display all student information in a structured table.
- **Search & Filter** – Find students by name, ID, email, or course.
- **Update Records** – Modify existing student information.
- **Delete Records** – Remove students with confirmation.
- **CSV Export** – Download student records for offline use.
- **Persistent Storage** – Store records locally using SQLite.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Backend logic |
| Streamlit | Web interface |
| SQLite | Database management |
| Pandas | Data handling and processing |
| HTML & CSS | Custom UI styling |

## 📂 Project Structure

```text
Student-Record-Management-System/
│
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

The SQLite database (`students.db`) is generated automatically when the application runs.

## 🚀 Getting Started

**1. Clone the repository**

```bash
git clone https://github.com/anupama-algo/Student-Record-Management-System.git
cd Student-Record-Management-System
```

**2. Create a virtual environment (optional)**

```bash
python -m venv .venv
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Run the application**

```bash
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

## 🔄 CRUD Operations

| Operation | Functionality |
|---|---|
| Create | Add new student records |
| Read | View, search, and filter records |
| Update | Edit student information |
| Delete | Permanently remove selected records |

## 🔮 Future Enhancements

- User authentication and role-based access
- Attendance tracking
- Student performance analytics
- Advanced reporting and data visualization

## 👩‍💻 Author

**Anupama Sethi**

[GitHub](https://github.com/anupama-algo)

---

*Built as a practical implementation of database operations and Python-based web application development.*