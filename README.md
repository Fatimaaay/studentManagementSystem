# Student Management System

A web application built with Django that includes user authentication with email verification and complete student record management.

## 🚀 Features

- User Registration with Email Verification
- Login & Logout
- Add Student
- Update Student
- Delete Student
- View All Students
- Clean and Responsive UI with HTML & CSS

## 🛠️ Technologies Used

- Python
- Django
- HTML & CSS
- SQLite (Database)
- Gmail SMTP (Email Verification)

## ⚙️ Setup & Installation

1. **Clone the repository**
```bash
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name
```

2. **Create virtual environment**
```bash
   python -m venv venv
   venv\Scripts\activate
```

3. **Install dependencies**
```bash
   pip install -r requirements.txt
```

4. **Create a `.env` file in root directory and add:**
```
   EMAIL_HOST_USER=your_email@gmail.com
   EMAIL_HOST_PASSWORD=your_gmail_app_password
```

5. **Run migrations**
```bash
   python manage.py makemigrations
   python manage.py migrate
```

6. **Start the server**
```bash
   python manage.py runserver
```

7. Open your browser and go to `http://127.0.0.1:8000`

## 📌 Notes

- Make sure to enable 2-Step Verification on Gmail and generate an App Password


## 👩‍💻 Author

Fatima Zaman
