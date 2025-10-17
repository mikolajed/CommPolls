# CommPolls 🗳️

A simple Django-based community polling application.

## Features (planned)

* User login & password reset
* Role-based access (Regular, Manager, Backend Admin)
* Polls and Topics with filtering
* Responsive, Bootstrap-styled UI
* AJAX voting
* Docker deployment & tests (to be added)

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
