# SQL Project: Online Course Management System

This project is designed to manage and interact with an SQL database for an online course platform. It includes utilities for database connection, learner management, and more.

## Project Structure

```
SQL_Project/
├── managers/               # Contains modules for managing learners, courses, etc.
│   ├── __init__.py
│   ├── learner_manager.py
│   ├── enrollment_manager.py
├── tests/                  # Contains test scripts
│   ├── test_connection.py  # Tests database connection
├── utils/                  # Utility modules
│   ├── __init__.py
│   ├── db_connector.py     # Handles database connections
├── config.py               # Configuration file for database settings
├── requirements.txt        # Python dependencies
├── venv/                   # Virtual environment
```

## Prerequisites

- Python 3.8 or higher
- MySQL server
- MySQL Workbench (optional)

## Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd SQL_Project
   ```

2. **Set Up Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up the Database**
   - Ensure your MySQL server is running.
   - Create the database if it doesn't exist:
     ```sql
     CREATE DATABASE onlinecourse;
     ```

5. **Configure Environment Variables**
   Add the following environment variables to your shell configuration file (`~/.bashrc` or `~/.zshrc`):
   ```bash
   export DB_HOST=localhost
   export DB_NAME=onlinecourse
   export DB_USER=root
   export DB_PASSWORD=your_password
   ```
   Reload the shell:
   ```bash
   source ~/.zshrc  # Or ~/.bashrc
   ```

6. **Run Tests**
   Test the database connection:
   ```bash
   python -m tests.test_connection
   ```

## Usage

- **Database Connection**
  The `utils/db_connector.py` module provides a `create_connection` function to establish a connection to the database.

- **Learner Management**
  Use the `managers/learner_manager.py` module to manage learners.

## Troubleshooting

- If you encounter `ModuleNotFoundError`, ensure the project root is added to the `PYTHONPATH`:
  ```bash
  export PYTHONPATH=/path/to/SQL_Project:$PYTHONPATH
  ```

- If the database connection fails, verify your database credentials in `config.py` or environment variables.

## License

This project is licensed under the MIT License.