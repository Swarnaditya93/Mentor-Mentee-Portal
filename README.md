# 🎓 Mentor Connect — Mentor-Mentee Portal

A role-based academic mentorship management system built with **Python** and **Streamlit**. It provides a unified platform for students, faculty mentors, and administrators to manage mentorship activities including academic tracking, leave applications, and direct communication.

---

## ✨ Features

### 👨‍🎓 Mentee
- Personalized dashboard with a semester-wise **SGPA progression chart**
- Submit and track **leave applications**
- View assigned **mentor details** (name, email, phone)
- **Message your mentor** and view full conversation history

### 👨‍🏫 Mentor
- Dashboard overview showing the number of assigned mentees
- View detailed **mentee profiles** (name, roll number, email, parent contact)
- **Approve or reject** pending leave applications
- **Message individual mentees** and view conversation history

### 🛠️ Admin
- **Add new mentors and mentees** with temporary credentials
- **Assign mentees** to mentors
- **Update SGPA records** per semester for any mentee
- **Permanently delete** a mentee and all associated data

---

## 🧰 Tech Stack

| Layer | Technology |
|---|---|
| Frontend / UI | Streamlit |
| Backend / Logic | Python |
| Database | SQLite (via `sqlite3`) |
| Data Handling | Pandas |
| Visualization | Matplotlib |

---

## 📁 Project Structure

```
Mentor-Mentee-Portal/
├── app.py              # Main application (all logic, UI, and DB in one file)
├── requirements.txt    # Python dependencies
└── mentorship.db       # SQLite database (auto-created on first run)
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/Swarnaditya93/Mentor-Mentee-Portal.git
cd Mentor-Mentee-Portal

# 2. (Optional) Create and activate a virtual environment
python -m venv venv
source venv/bin/activate       # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`.

---

## 🔑 Default Login Credentials

The database is seeded with sample data on first launch.

| Role | ID / Roll No. | Password |
|---|---|---|
| Mentee | `101` | `pass123` |
| Mentee | `102` | `pass123` |
| Mentor | `EMP01` | `admin123` |
| Admin | `ADMIN` | `superadmin` |

> ⚠️ **Note:** These are demo credentials. Change passwords before deploying to a production environment.

---

## 🗄️ Database Schema

The app uses a local SQLite database (`mentorship.db`) with the following tables:

| Table | Description |
|---|---|
| `users` | Stores login credentials and roles |
| `mentees` | Student profiles and mentor assignments |
| `mentors` | Faculty mentor profiles |
| `sgpa` | Per-semester SGPA records for each student |
| `leaves` | Leave applications and their approval status |
| `messages` | Messages exchanged between mentors and mentees |

---

## 📸 Application Screens

- **Login Page** — Role-based login (Mentee / Mentor / Admin) with a styled background
- **Mentee Dashboard** — SGPA line chart with annotated data points per semester
- **Leave Application** — Date picker and purpose field with pending/accepted/rejected status
- **Communication Hub** — Chat-style message interface between mentor and mentee
- **Admin Panel** — Tabbed interface for user management, assignments, and academic records

---

## 🔒 Security Notes

- Passwords are stored as **plain text** in the current version — this is suitable for academic demos only.
- For a production deployment, consider hashing passwords with `bcrypt` or `hashlib`, and using environment variables for secrets.
- The SQLite database file (`mentorship.db`) is created locally; ensure it is excluded from public repositories via `.gitignore`.

---

## 🤝 Contributing

Contributions are welcome! To get started:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature-name`)
3. Commit your changes (`git commit -m 'Add some feature'`)
4. Push to the branch (`git push origin feature/your-feature-name`)
5. Open a Pull Request

---

## 📄 License

This project is open source. Feel free to use and adapt it for educational purposes.

---

## 👤 Author

**Swarnaditya93**
[GitHub Profile](https://github.com/Swarnaditya93)
