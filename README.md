# CommPolls 🗳️

A simple Django-based community polling application.

## Features

* **User Authentication**: Secure sign-up, login, logout, and password management.
* **Account Management**: Users can view and update their account details.
* **Poll Creation**: Authenticated users can create polls with custom choices.
* **Poll Management**: Users can manage their created polls, including updating the end date, closing the poll, or deleting it.
* **Voting System**: Users can vote on active polls, with safeguards to prevent duplicate voting.
* **Real-Time Results**: Poll results update automatically in real-time using AJAX, without needing a page refresh.
* **Poll Lifecycle**: Polls have a clear lifecycle, with a countdown for upcoming polls, an active voting period, and a final results view.
* **User Dashboards**: Dedicated pages for users to view all the polls they have created ("My Polls") and all the polls they have voted on ("My Votes").
* **Advanced Poll Filtering**: Filter polls on the homepage by creator, start/end date, and voting status.

## Future Enhancements

* **Role-Based Access**: Introduce roles like Regular, Manager, and Backend Admin to manage permissions.
* **Poll Topics**: Organize polls by topics and allow users to filter them.
* **Responsive UI**: Implement a responsive, modern UI using a framework like Bootstrap.
* **Containerization**: Add Docker support for easier deployment and a consistent development environment.
* **Automated Testing**: Expand the test suite to cover all application features.

## Getting Started (Development)

### 1. Clone this repo

```bash
git clone https://github.com/mikolajed/CommPolls.git
cd CommPolls
```

## ⚠️ Python Version

This project currently does **not work with Python 3.14** due to Django compatibility issues.

Please use **Python 3.12** (recommended) or **Python 3.11** when setting up your environment.

You can install it with [pyenv](https://github.com/pyenv/pyenv):

```bash
pyenv install 3.12.6
pyenv local 3.12.6
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Running Tests 🧢

We use Django’s test framework with coverage to ensure all parts of the application work correctly. You can run tests locally and generate reports similar to the GitHub workflow.

### 1. Install testing dependencies

```bash
pip install coverage pytest pytest-django
```

### 2. Run all tests with coverage

```bash
coverage run --source=comm_polls manage.py test
coverage report -m           # shows coverage in the terminal
coverage html                # generates an HTML report at htmlcov/index.html
```

### 3. Run specific test types

You can run only certain types of tests by pointing to the test file:

```bash
# Unit tests
python manage.py test comm_polls.tests

# Integration tests
python manage.py test comm_polls.integration_tests

# End-to-end tests
python manage.py test comm_polls.e2e_tests
```

### 4. View HTML coverage report

Open the generated report in your browser:

```bash
open htmlcov/index.html   # macOS
xdg-open htmlcov/index.html # Linux
```

> Tip: You can combine pytest with coverage for faster test discovery and nicer output:

```bash
pytest --cov=comm_polls --cov-report=term --cov-report=html
```
