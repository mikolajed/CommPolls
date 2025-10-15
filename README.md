# CommPolls 🗳️

A simple Django-based community polling application.

## Features (planned)
- User login & password reset  
- Role-based access (Regular, Manager, Backend Admin)  
- Polls and Topics with filtering  
- Responsive, Bootstrap-styled UI  
- AJAX voting  
- Docker deployment & tests (to be added)

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
