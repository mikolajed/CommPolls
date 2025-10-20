# 🗳️ CommPolls

A simple **Django-based community polling application** that allows users to create, vote, and manage polls.

---

## 🚀 Features

- 🔐 **User Authentication** – Sign-up, login, logout, and password management.  
- 👤 **Account Management** – Update username, email, and avatar.  
- 📊 **Poll Creation** – Authenticated users can create polls with multiple choices.  
- 🗑️ **Poll Management** – Edit, close, or delete polls.  
- ✅ **Voting System** – One vote per user per poll.  
- ⚡ **Real-Time Results** – Live poll updates via AJAX.  
- 🕒 **Poll Lifecycle** – Upcoming, active, and completed polls.  
- 🧍 **User Dashboards** – View "My Polls" and "My Votes."  
- 🔍 **Advanced Filtering** – Filter polls by creator, date, and status.  

---

## 🧭 Future Enhancements

- Role-based permissions (Regular, Manager, Admin)  
- Poll topics and tags  
- Responsive UI (Bootstrap / Tailwind)  
- Full test coverage & CI/CD improvements  

---

## 🧑‍💻 Getting Started (Development)

### 1. Clone the repository
```bash
git clone https://github.com/mikolajed/CommPolls.git
cd CommPolls
```

### 2. Set up Python environment
> ⚠️ Django 4.2 is **not compatible with Python 3.14**.  
Use **Python 3.12** (recommended) or **Python 3.11**.

```bash
pyenv install 3.12.6
pyenv local 3.12.6
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 🧪 Running Tests

We use Django’s built-in test runner and `coverage` for detailed reporting.

### 1. Install test dependencies
```bash
pip install coverage pytest pytest-django
```

### 2. Run all tests with coverage
```bash
coverage run --source=comm_polls manage.py test
coverage report -m
coverage html
```

### 3. Run specific test types
```bash
# Unit tests
python manage.py test comm_polls.tests

# Integration tests
python manage.py test comm_polls.integration_tests

# End-to-End (E2E) tests
python manage.py test comm_polls.e2e_tests
```

### 4. View HTML coverage report
```bash
open htmlcov/index.html      # macOS
xdg-open htmlcov/index.html  # Linux
```

---

## 🐳 Deploying with Docker

You can run CommPolls entirely in Docker — no local setup needed.

### 1. Build and start the app
```bash
docker compose up --build
```

This will:
- Build the Django app container  
- Run the dev server on [http://localhost:8000](http://localhost:8000)

### 2. Run migrations (if needed)
```bash
docker compose exec web python manage.py migrate
```

### 3. Create a superuser (admin)
```bash
docker compose exec web python manage.py createsuperuser
```

Then log in at:
```
http://localhost:8000/admin/
```

### 4. Run tests in Docker
```bash
docker compose exec web coverage run --source=comm_polls manage.py test
docker compose exec web coverage report -m
```

---

## ⚙️ Environment Variables

Create a `.env` file in your project root:

```
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
```

---

## 💡 Quick Start Summary

```bash
# Setup
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate

# Run locally
python manage.py runserver

# Create superuser
python manage.py createsuperuser
```

Then open:  
👉 **http://127.0.0.1:8000/**

---

## 🧠 License

This project is licensed under the **MIT License** — free to use and modify.

---

**CommPolls** — Simple, scalable, and community-driven polls for everyone 🗳️
