
import streamlit as st
import sqlite3
import pandas as pd

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="StudentHub | Management System",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- DATABASE ----------------
def connect():
    return sqlite3.connect("students.db")

def setup_database():
    with connect() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                course TEXT NOT NULL,
                email TEXT NOT NULL
            )
        """)

def get_students():
    with connect() as conn:
        return pd.read_sql_query(
            "SELECT * FROM students ORDER BY id", conn
        )

def add_student(sid, name, age, course, email):
    try:
        with connect() as conn:
            conn.execute(
                "INSERT INTO students VALUES (?, ?, ?, ?, ?)",
                (sid, name, age, course, email)
            )
        return True
    except sqlite3.IntegrityError:
        return False

def update_student(sid, name, age, course, email):
    with connect() as conn:
        conn.execute("""
            UPDATE students
            SET name=?, age=?, course=?, email=?
            WHERE id=?
        """, (name, age, course, email, sid))

def delete_student(sid):
    with connect() as conn:
        conn.execute(
            "DELETE FROM students WHERE id=?", (sid,)
        )

setup_database()

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
    .stApp {
        background-color: #F5F7FB;
        color: #172033;
    }

    [data-testid="stSidebar"] {
        background: #111C35;
    }

    [data-testid="stSidebar"] * {
        color: #F8FAFC;
    }

    [data-testid="stSidebar"] .stRadio label {
        padding: 8px;
        border-radius: 8px;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    h1, h2, h3 {
        color: #172033;
        font-family: 'Segoe UI', sans-serif;
    }

    .page-subtitle {
        color: #64748B;
        font-size: 15px;
        margin-bottom: 25px;
    }

    .stat-card {
        background: white;
        padding: 22px;
        border-radius: 14px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 3px 12px rgba(0,0,0,0.03);
        margin-bottom: 12px;
    }

    .stat-label {
        color: #64748B;
        font-size: 14px;
        font-weight: 500;
    }

    .stat-value {
        color: #172033;
        font-size: 30px;
        font-weight: 750;
        margin-top: 8px;
    }

    div.stButton > button[kind="primary"],
    div.stFormSubmitButton > button[kind="primary"] {
        background-color: #4F46E5;
        color: white;
        border: none;
        border-radius: 9px;
    }

    div.stButton > button,
    div.stFormSubmitButton > button {
        border-radius: 9px;
        font-weight: 600;
    }

    [data-testid="stForm"] {
        background: white;
        padding: 22px;
        border-radius: 14px;
        border: 1px solid #E2E8F0;
    }

    [data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
    }
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown("## 🎓 StudentHub")
    st.caption("STUDENT MANAGEMENT SYSTEM")
    st.divider()

    menu = st.radio(
        "NAVIGATION",
        [
            "Dashboard",
            "Add Student",
            "View Students",
            "Update Student",
            "Delete Student"
        ]
    )

    st.divider()
    st.caption("StudentHub • Version 1.0")
    st.caption("Built with Python & Streamlit")

# ---------------- DATA ----------------
df = get_students()

# ---------------- DASHBOARD ----------------
if menu == "Dashboard":
    st.title("Student Dashboard")
    st.markdown(
        '<p class="page-subtitle">'
        'Welcome to StudentHub. Manage all student records '
        'from one place.</p>',
        unsafe_allow_html=True
    )

    total_students = len(df)
    total_courses = df["course"].nunique() if not df.empty else 0
    average_age = df["age"].mean() if not df.empty else 0

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">👨‍🎓 Total Students</div>
            <div class="stat-value">{total_students}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">📚 Total Courses</div>
            <div class="stat-value">{total_courses}</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">📊 Average Age</div>
            <div class="stat-value">{average_age:.1f}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### Recent Student Records")

    if df.empty:
        st.info("No students added yet. Start by adding a student.")
    else:
        st.dataframe(
            df.tail(5).iloc[::-1],
            use_container_width=True,
            hide_index=True
        )

        st.markdown("### Students by Course")
        course_counts = df["course"].value_counts()
        st.bar_chart(course_counts)

# ---------------- CREATE ----------------
elif menu == "Add Student":
    st.title("Add New Student")
    st.markdown(
        '<p class="page-subtitle">'
        'Enter the student information below.</p>',
        unsafe_allow_html=True
    )

    with st.form("add_student_form", clear_on_submit=True):
        col1, col2 = st.columns(2)

        with col1:
            sid = st.number_input(
                "Student ID", min_value=1, step=1
            )
            name = st.text_input(
                "Full Name", placeholder="Enter student name"
            )
            age = st.number_input(
                "Age", min_value=1, max_value=100, value=18
            )

        with col2:
            course = st.text_input(
                "Course", placeholder="e.g. B.Tech CSE"
            )
            email = st.text_input(
                "Email Address",
                placeholder="student@example.com"
            )

        submitted = st.form_submit_button(
            "➕ Add Student", type="primary",
            use_container_width=True
        )

        if submitted:
            if not name.strip() or not course.strip() or not email.strip():
                st.warning("Please fill in all fields.")
            elif "@" not in email or "." not in email.split("@")[-1]:
                st.error("Please enter a valid email address.")
            else:
                success = add_student(
                    sid, name.strip(), age,
                    course.strip(), email.strip()
                )

                if success:
                    st.success("Student added successfully!")
                else:
                    st.error("This Student ID already exists.")

# ---------------- READ ----------------
elif menu == "View Students":
    st.title("Student Records")
    st.markdown(
        '<p class="page-subtitle">'
        'Browse, search and filter student information.</p>',
        unsafe_allow_html=True
    )

    if df.empty:
        st.info("No student records available.")
    else:
        col1, col2 = st.columns([2, 1])

        with col1:
            search = st.text_input(
                "Search Students",
                placeholder="Search by name, ID or email"
            )

        with col2:
            courses = ["All Courses"] + sorted(
                df["course"].unique().tolist()
            )
            selected_course = st.selectbox(
                "Filter by Course", courses
            )

        filtered = df.copy()

        if search:
            mask = (
                filtered["name"].str.contains(
                    search, case=False, regex=False
                )
                | filtered["id"].astype(str).str.contains(
                    search, regex=False
                )
                | filtered["email"].str.contains(
                    search, case=False, regex=False
                )
            )
            filtered = filtered[mask]

        if selected_course != "All Courses":
            filtered = filtered[
                filtered["course"] == selected_course
            ]

        st.write(f"Showing **{len(filtered)}** students")

        st.dataframe(
            filtered,
            use_container_width=True,
            hide_index=True
        )

        st.download_button(
            "⬇ Download CSV",
            data=filtered.to_csv(index=False),
            file_name="student_records.csv",
            mime="text/csv"
        )

# ---------------- UPDATE ----------------
elif menu == "Update Student":
    st.title("Update Student")
    st.markdown(
        '<p class="page-subtitle">'
        'Select a student and modify their information.</p>',
        unsafe_allow_html=True
    )

    if df.empty:
        st.info("No students available to update.")
    else:
        student_ids = df["id"].tolist()

        sid = st.selectbox(
            "Select Student ID", student_ids
        )

        student = df[df["id"] == sid].iloc[0]

        with st.form(f"update_form_{sid}"):
            col1, col2 = st.columns(2)

            with col1:
                name = st.text_input(
                    "Full Name", value=student["name"]
                )
                age = st.number_input(
                    "Age", min_value=1, max_value=100,
                    value=int(student["age"])
                )

            with col2:
                course = st.text_input(
                    "Course", value=student["course"]
                )
                email = st.text_input(
                    "Email", value=student["email"]
                )

            submitted = st.form_submit_button(
                "💾 Save Changes",
                type="primary",
                use_container_width=True
            )

            if submitted:
                if not name.strip() or not course.strip() or not email.strip():
                    st.warning("All fields are required.")
                elif "@" not in email or "." not in email.split("@")[-1]:
                    st.error("Please enter a valid email address.")
                else:
                    update_student(
                        sid, name.strip(), age,
                        course.strip(), email.strip()
                    )
                    st.success("Student updated successfully!")
                    st.rerun()

# ---------------- DELETE ----------------
elif menu == "Delete Student":
    st.title("Delete Student")
    st.markdown(
        '<p class="page-subtitle">'
        'Remove a student record from the database.</p>',
        unsafe_allow_html=True
    )

    if df.empty:
        st.info("No students available to delete.")
    else:
        sid = st.selectbox(
            "Select Student ID",
            df["id"].tolist()
        )

        student = df[df["id"] == sid].iloc[0]

        st.markdown("### Selected Student")
        st.write(f"**Name:** {student['name']}")
        st.write(f"**Course:** {student['course']}")
        st.write(f"**Email:** {student['email']}")

        st.warning(
            "This action will permanently delete the student record."
        )

        confirm = st.checkbox(
            "I confirm that I want to delete this student."
        )

        if st.button(
            "🗑 Delete Student",
            type="primary",
            disabled=not confirm
        ):
            delete_student(sid)
            st.success("Student deleted successfully!")
            st.rerun()
            