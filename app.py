import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3

# --- Page Configuration ---
st.set_page_config(page_title="Mentor Connect", layout="wide", initial_sidebar_state="expanded")

# --- Dynamic Background & UI Readability Styling ---
def set_background(theme):
    if theme == "login":
        bg_img = "https://images.unsplash.com/photo-1519681393784-d120267933ba?q=80&w=2070&auto=format&fit=crop"
        bg_color = "transparent"
        form_css = """
        [data-testid="stForm"] {
            background-color: rgba(15, 15, 15, 0.95);
            padding: 2rem;
            border-radius: 15px;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        """
    else:
        bg_img = "https://images.unsplash.com/photo-1456324504439-367cee3b3c32?q=80&w=2070&auto=format&fit=crop"
        bg_color = "rgba(18, 18, 18, 0.9)"
        form_css = "" 

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: linear-gradient({bg_color}, {bg_color}), url('{bg_img}');
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            color: white;
        }}
        [data-testid="stAppViewBlockContainer"] {{
            background-color: rgba(18, 18, 18, 0.85) !important;
            padding: 2rem;
            border-radius: 15px;
            margin-top: 2rem;
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5);
        }}
        [data-testid="stSidebar"] {{
            background-color: rgba(15, 15, 15, 0.95);
        }}
        h1, h2, h3, p, label, .stMarkdown {{
            color: #E0E0E0 !important;
        }}
        div[data-testid="stButton"] button, 
        div[data-testid="stFormSubmitButton"] button {{
            background-color: #2e7d32 !important; 
            color: white !important;
            border: none !important;
            border-radius: 5px !important;
            font-weight: bold !important;
        }}
        div[data-testid="stButton"] button:hover, 
        div[data-testid="stFormSubmitButton"] button:hover {{
            background-color: #1b5e20 !important; 
            border: none !important;
        }}
        {form_css}
        </style>
        """,
        unsafe_allow_html=True
    )

# --- Database Initialization ---
def init_db():
    conn = sqlite3.connect('mentorship.db')
    c = conn.cursor()
    
    # Removed attendance from mentees table
    c.execute('''CREATE TABLE IF NOT EXISTS users (role TEXT, user_id TEXT, password TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS mentees (roll TEXT, name TEXT, email TEXT, parents_contact TEXT, mentor_id TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS sgpa (roll TEXT, semester INTEGER, sgpa REAL)''')
    c.execute('''CREATE TABLE IF NOT EXISTS mentors (emp_id TEXT, name TEXT, email TEXT, phone TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS leaves (id INTEGER PRIMARY KEY AUTOINCREMENT, roll TEXT, start_date TEXT, end_date TEXT, purpose TEXT, status TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY AUTOINCREMENT, sender_id TEXT, receiver_id TEXT, message TEXT)''')
    
    c.execute("SELECT COUNT(*) FROM users")
    if c.fetchone()[0] == 0:
        c.executemany("INSERT INTO users VALUES (?, ?, ?)", [
            ('Mentee', '101', 'pass123'), 
            ('Mentee', '102', 'pass123'), 
            ('Mentor', 'EMP01', 'admin123'),
            ('Admin', 'ADMIN', 'superadmin')
        ])
        c.executemany("INSERT INTO mentees VALUES (?, ?, ?, ?, ?)", [
            ('101', 'Ethan', 'ethan@student.edu', '9876543210', 'EMP01'),
            ('102', 'Nancy', 'nancy@student.edu', '9876543211', 'EMP01')
        ])
        c.executemany("INSERT INTO sgpa VALUES (?, ?, ?)", [
            ('101', 1, 8.2), ('101', 2, 8.5), ('101', 3, 8.86),
            ('102', 1, 8.5), ('102', 2, 8.7), ('102', 3, 8.86)
        ])
        c.execute("INSERT INTO mentors VALUES (?, ?, ?, ?)", ('EMP01', 'Prof. Alan Turing', 'alan.t@university.edu', '+91 98765 12345'))
        conn.commit()
    conn.close()

init_db()

# --- Helper DB Functions ---
def query_db(query, params=()):
    conn = sqlite3.connect('mentorship.db')
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df

def execute_db(query, params=()):
    conn = sqlite3.connect('mentorship.db')
    c = conn.cursor()
    c.execute(query, params)
    conn.commit()
    conn.close()

# --- Visualization Helpers ---
def draw_sgpa_graph(df):
    fig, ax = plt.subplots(figsize=(8, 4))
    if df.empty:
        ax.text(0.5, 0.5, "No SGPA Data Available", ha='center', va='center', color='white', fontsize=12)
        ax.axis('off')
    else:
        ax.plot(df['semester'], df['sgpa'], marker='o', color='#00BCD4', linewidth=2, markersize=8)
        ax.set_ylim(0, 10)
        ax.set_xticks(df['semester'])
        ax.set_xticklabels([f"Sem {int(s)}" for s in df['semester']])
        
        # Add exact SGPA text at each plotted point
        for index, row in df.iterrows():
            ax.annotate(f"{row['sgpa']:.2f}",
                        (row['semester'], row['sgpa']),
                        textcoords="offset points",
                        xytext=(0,10), 
                        ha='center', 
                        color='white',
                        fontweight='bold')

        ax.grid(True, linestyle='--', alpha=0.3)
        ax.set_ylabel("SGPA", color='white')
        ax.tick_params(colors='white')
        for spine in ax.spines.values():
            spine.set_edgecolor('#555555')
    fig.patch.set_facecolor('none')
    ax.set_facecolor('none')
    return fig

# --- Session State Management ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# --- Login System ---
if not st.session_state.logged_in:
    set_background("login")
    st.markdown("<h1 style='text-align: center; margin-top: 5vh;'>Welcome to Portal</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("login_form"):
            role = st.selectbox("Select Role", ["Mentee", "Mentor", "Admin"])
            user_id = st.text_input("Roll Number / Employee ID")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Log In", use_container_width=True)
            
            if submit:
                user = query_db("SELECT * FROM users WHERE role=? AND user_id=? AND password=?", (role, user_id, password))
                if not user.empty:
                    st.session_state.logged_in = True
                    st.session_state.current_user = user_id
                    st.session_state.role = role
                    st.rerun()
                else:
                    st.error("Invalid ID or Password")

# --- Main Application ---
else:
    set_background("dashboard")
    st.sidebar.title(f"{st.session_state.role} Panel")
    
    # --- MENTEE VIEW ---
    if st.session_state.role == "Mentee":
        options = ["Dashboard", "1. Leave Application", "2. Mentor Details", "3. Communication Hub"]
        choice = st.sidebar.radio("Navigation", options)
        user_roll = st.session_state.current_user
        student_info = query_db("SELECT * FROM mentees WHERE roll=?", (user_roll,)).iloc[0]
        
        if choice == "Dashboard":
            st.title(f"Welcome, {student_info['name']}")
            st.subheader("Academic Progression (SGPA)")
            sgpa_data = query_db("SELECT semester, sgpa FROM sgpa WHERE roll=? ORDER BY semester", (user_roll,))
            st.pyplot(draw_sgpa_graph(sgpa_data))
                
        elif choice == "1. Leave Application":
            st.header("Apply for Leave")
            with st.form("leave_form"):
                start_date = st.date_input("Start Date")
                end_date = st.date_input("End Date")
                purpose = st.text_area("Leave Purpose")
                if st.form_submit_button("Submit Application"):
                    execute_db("INSERT INTO leaves (roll, start_date, end_date, purpose, status) VALUES (?, ?, ?, ?, ?)",
                               (user_roll, start_date, end_date, purpose, 'Pending'))
                    st.success("Leave application submitted successfully!")
                    
        elif choice == "2. Mentor Details":
            st.header("Assigned Mentor Information")
            if student_info['mentor_id'] != 'Unassigned':
                mentor = query_db("SELECT * FROM mentors WHERE emp_id=?", (student_info['mentor_id'],)).iloc[0]
                st.write(f"**Name:** {mentor['name']}")
                st.write(f"**Email:** {mentor['email']}")
                st.write(f"**Phone:** {mentor['phone']}")
            else:
                st.info("You have not been assigned a mentor yet.")
            
        elif choice == "3. Communication Hub":
            st.header("Mentor Communication")
            tab1, tab2 = st.tabs(["Send Message", "View Messages"])
            
            with tab1:
                if student_info['mentor_id'] != 'Unassigned':
                    msg = st.text_area("Write your request or message here:")
                    if st.button("Send Message"):
                        execute_db("INSERT INTO messages (sender_id, receiver_id, message) VALUES (?, ?, ?)",
                                   (user_roll, student_info['mentor_id'], msg))
                        st.success("Message sent to mentor!")
                else:
                    st.warning("You must be assigned a mentor before sending messages.")
                    
            with tab2:
                msgs = query_db("SELECT * FROM messages WHERE sender_id=? OR receiver_id=? ORDER BY id ASC", (user_roll, user_roll))
                if msgs.empty:
                    st.info("No message history found.")
                else:
                    for idx, row in msgs.iterrows():
                        if row['sender_id'] == user_roll:
                            with st.chat_message("user"):
                                st.write(f"**You:** {row['message']}")
                        else:
                            with st.chat_message("assistant"):
                                mentor_name = query_db("SELECT name FROM mentors WHERE emp_id=?", (row['sender_id'],)).iloc[0]['name']
                                st.write(f"**{mentor_name}:** {row['message']}")

    # --- MENTOR VIEW ---
    elif st.session_state.role == "Mentor":
        options = ["Dashboard", "1. Mentee Details", "2. Leave Management", "3. Communication Hub"]
        choice = st.sidebar.radio("Navigation", options)
        mentor_id = st.session_state.current_user
        my_mentees = query_db("SELECT * FROM mentees WHERE mentor_id=?", (mentor_id,))
        
        if choice == "Dashboard":
            st.title("Mentor Dashboard Overview")
            st.metric("Total Mentees Assigned", len(my_mentees))
            
        elif choice == "1. Mentee Details":
            st.header("Your Mentees")
            if not my_mentees.empty:
                st.dataframe(my_mentees[['name', 'roll', 'email', 'parents_contact']], hide_index=True, use_container_width=True)
            else:
                st.info("No mentees assigned yet.")
            
        elif choice == "2. Leave Management":
            st.header("Pending Leave Applications")
            pending_leaves = query_db("SELECT l.*, m.name FROM leaves l JOIN mentees m ON l.roll = m.roll WHERE l.status='Pending' AND m.mentor_id=?", (mentor_id,))
            if pending_leaves.empty:
                st.info("No pending leave applications.")
            else:
                for index, row in pending_leaves.iterrows():
                    with st.expander(f"Leave Request from {row['name']} ({row['start_date']} to {row['end_date']})"):
                        st.write(f"**Purpose:** {row['purpose']}")
                        col1, col2 = st.columns([1, 10])
                        if col1.button("Accept", key=f"acc_{row['id']}"):
                            execute_db("UPDATE leaves SET status='Accepted' WHERE id=?", (row['id'],))
                            st.rerun()
                        if col2.button("Reject", key=f"rej_{row['id']}"):
                            execute_db("UPDATE leaves SET status='Rejected' WHERE id=?", (row['id'],))
                            st.rerun()
                                
        elif choice == "3. Communication Hub":
            st.header("Mentee Communication")
            tab1, tab2 = st.tabs(["Send Message", "View Messages"])
            
            with tab1:
                if not my_mentees.empty:
                    selected_mentee_name = st.selectbox("Search and Select Mentee", my_mentees['name'].tolist())
                    selected_roll = my_mentees[my_mentees['name'] == selected_mentee_name].iloc[0]['roll']
                    msg = st.text_area("Write your message:")
                    if st.button("Send Message"):
                        execute_db("INSERT INTO messages (sender_id, receiver_id, message) VALUES (?, ?, ?)",
                                   (mentor_id, selected_roll, msg))
                        st.success(f"Message sent to {selected_mentee_name}!")
                else:
                    st.warning("You have no mentees to message.")
                    
            with tab2:
                msgs = query_db("SELECT * FROM messages WHERE sender_id=? OR receiver_id=? ORDER BY id ASC", (mentor_id, mentor_id))
                if msgs.empty:
                    st.info("No message history found.")
                else:
                    for idx, row in msgs.iterrows():
                        if row['sender_id'] == mentor_id:
                            with st.chat_message("user"):
                                mentee_name = query_db("SELECT name FROM mentees WHERE roll=?", (row['receiver_id'],)).iloc[0]['name']
                                st.write(f"**You (to {mentee_name}):** {row['message']}")
                        else:
                            with st.chat_message("assistant"):
                                mentee_name = query_db("SELECT name FROM mentees WHERE roll=?", (row['sender_id'],)).iloc[0]['name']
                                st.write(f"**{mentee_name}:** {row['message']}")

    # --- ADMIN VIEW ---
    elif st.session_state.role == "Admin":
        options = ["Add New Users", "Assign Mentees", "Update Academic Records", "Delete Users"]
        choice = st.sidebar.radio("Admin Navigation", options)
        
        if choice == "Add New Users":
            st.title("User Management")
            tab1, tab2 = st.tabs(["Add Mentor", "Add Mentee"])
            
            with tab1:
                st.subheader("Register New Mentor")
                with st.form("add_mentor_form"):
                    m_name = st.text_input("Full Name")
                    m_emp_id = st.text_input("Employee ID")
                    m_email = st.text_input("Email")
                    m_phone = st.text_input("Phone Number")
                    m_pass = st.text_input("Temporary Password", type="password")
                    if st.form_submit_button("Create Mentor"):
                        execute_db("INSERT INTO users (role, user_id, password) VALUES (?, ?, ?)", ('Mentor', m_emp_id, m_pass))
                        execute_db("INSERT INTO mentors (emp_id, name, email, phone) VALUES (?, ?, ?, ?)", (m_emp_id, m_name, m_email, m_phone))
                        st.success(f"Mentor {m_name} added successfully!")
                        
            with tab2:
                st.subheader("Register New Mentee")
                with st.form("add_mentee_form"):
                    s_name = st.text_input("Full Name")
                    s_roll = st.text_input("Roll Number")
                    s_email = st.text_input("Email")
                    s_parents = st.text_input("Parents Contact")
                    s_pass = st.text_input("Temporary Password", type="password")
                    if st.form_submit_button("Create Mentee"):
                        execute_db("INSERT INTO users (role, user_id, password) VALUES (?, ?, ?)", ('Mentee', s_roll, s_pass))
                        # Attendance removed from database insertion
                        execute_db("INSERT INTO mentees (roll, name, email, parents_contact, mentor_id) VALUES (?, ?, ?, ?, ?)", 
                                   (s_roll, s_name, s_email, s_parents, 'Unassigned'))
                        st.success(f"Mentee {s_name} added successfully!")

        elif choice == "Assign Mentees":
            st.title("Mentor-Mentee Allocation")
            all_mentees = query_db("SELECT roll, name, mentor_id FROM mentees")
            all_mentors = query_db("SELECT emp_id, name FROM mentors")
            
            if not all_mentees.empty and not all_mentors.empty:
                with st.form("assignment_form"):
                    mentee_dict = dict(zip(all_mentees['name'] + " (" + all_mentees['roll'] + ")", all_mentees['roll']))
                    mentor_dict = dict(zip(all_mentors['name'] + " (" + all_mentors['emp_id'] + ")", all_mentors['emp_id']))
                    selected_mentee = st.selectbox("Select Mentee", list(mentee_dict.keys()))
                    selected_mentor = st.selectbox("Assign to Mentor", list(mentor_dict.keys()))
                    
                    if st.form_submit_button("Assign"):
                        execute_db("UPDATE mentees SET mentor_id=? WHERE roll=?", (mentor_dict[selected_mentor], mentee_dict[selected_mentee]))
                        st.success(f"Successfully assigned {selected_mentee} to {selected_mentor}!")
            else:
                st.warning("Ensure you have added at least one mentor and one mentee first.")

        elif choice == "Update Academic Records":
            st.title("Update Mentee SGPA")
            all_mentees = query_db("SELECT roll, name FROM mentees")
            
            if not all_mentees.empty:
                mentee_dict = dict(zip(all_mentees['name'] + " (" + all_mentees['roll'] + ")", all_mentees['roll']))
                selected_mentee = st.selectbox("Select Mentee", list(mentee_dict.keys()))
                roll = mentee_dict[selected_mentee]
                
                existing_sgpa = query_db("SELECT semester, sgpa FROM sgpa WHERE roll=? ORDER BY semester", (roll,))
                if not existing_sgpa.empty:
                    st.write(f"**Current Records for {selected_mentee}:**")
                    st.dataframe(existing_sgpa, hide_index=True)
                
                with st.form("sgpa_form"):
                    sem = st.number_input("Semester", min_value=1, max_value=8, step=1)
                    sgpa_val = st.number_input("SGPA", min_value=0.0, max_value=10.0, step=0.01)
                    
                    if st.form_submit_button("Add / Update Record"):
                        check = query_db("SELECT * FROM sgpa WHERE roll=? AND semester=?", (roll, sem))
                        if check.empty:
                            execute_db("INSERT INTO sgpa (roll, semester, sgpa) VALUES (?, ?, ?)", (roll, sem, sgpa_val))
                            st.success(f"Added Semester {sem} SGPA for {selected_mentee}.")
                        else:
                            execute_db("UPDATE sgpa SET sgpa=? WHERE roll=? AND semester=?", (sgpa_val, roll, sem))
                            st.success(f"Updated Semester {sem} SGPA for {selected_mentee}.")
                        st.rerun()

        elif choice == "Delete Users":
            st.title("Delete Mentee Records")
            st.write("Removing a mentee here will permanently delete their login, profile, grades, and messages.")
            all_mentees = query_db("SELECT roll, name FROM mentees")
            
            if not all_mentees.empty:
                mentee_dict = dict(zip(all_mentees['name'] + " (" + all_mentees['roll'] + ")", all_mentees['roll']))
                selected_mentee = st.selectbox("Select Mentee to Remove", list(mentee_dict.keys()))
                
                st.warning("⚠️ Warning: This action cannot be undone.")
                
                if st.button("Permanently Delete Mentee"):
                    roll = mentee_dict[selected_mentee]
                    execute_db("DELETE FROM mentees WHERE roll=?", (roll,))
                    execute_db("DELETE FROM users WHERE user_id=? AND role='Mentee'", (roll,))
                    execute_db("DELETE FROM sgpa WHERE roll=?", (roll,))
                    execute_db("DELETE FROM leaves WHERE roll=?", (roll,))
                    execute_db("DELETE FROM messages WHERE sender_id=? OR receiver_id=?", (roll, roll))
                    st.success(f"Successfully deleted all records for {selected_mentee}.")
                    st.rerun()
            else:
                st.info("No mentees currently exist in the database.")

    # --- Logout ---
    st.sidebar.markdown("---")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.current_user = None
        st.session_state.role = None
        st.rerun()
