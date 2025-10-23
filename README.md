# 🗳️ CommPolls

A simple **Django-based community polling application** that allows users to create, vote, and manage polls.

---

## 🚀 Features

- **Single Page Application** – Smooth navigation and dynamic content loading.
- **User Authentication** – Sign-up, login, logout, and password management.  
- **Account Management** – Update username, email, and avatar.  
- **Poll Creation** – Authenticated users can create polls with multiple choices.  
- **Poll Management** – Close or delete polls.  
- **Voting System** – One vote per user per poll.  
- **Poll Lifecycle** – Upcoming, active, and completed polls.  
- **Advanced Filtering** – Filter polls by creator, date, and status.  
- **Mobile Responsive** – View polls on mobile devices.
- **Timer** – Countdown timer for upcoming polls and till poll closes.
- **Role-based permissions** – Regular users, managers, and admins.
- **Docker** – Run the app in a container.

---

## 🧑‍💻 Getting Started (Development)

### 1. Clone the repository
```bash
git clone https://github.com/mikolajed/CommPolls.git
cd CommPolls
```

---

## 🧪 Running Tests

We use Django’s built-in test runner and `coverage` for detailed reporting.

### 1. Install test dependencies
```bash
pip install -r requirements.txt
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
```

### 4. View HTML coverage report
```bash
open htmlcov/index.html      # macOS
xdg-open htmlcov/index.html  # Linux
```

---

## 🐳 Run with Docker

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
# Django settings
DEBUG=True
SECRET_KEY=your-super-secret-key-for-development-change-for-prod
ALLOWED_HOSTS=localhost,127.0.0.1

# Email backend (optional)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend

# PostgreSQL Database settings
DB_NAME=commpolls_db
DB_USER=commpolls_user
DB_PASSWORD=commpolls_pass
DB_HOST=db       
DB_PORT=5432
```
