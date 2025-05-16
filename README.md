# SQL Project: Online Course Management System

This project is a command-line application designed to manage an online course platform. It provides functionality for learners, instructors, and administrators to interact with an SQL database.

## Features

- **Learner Portal**: View enrolled courses, enroll in new courses, and access course content.
- **Instructor Portal**: Manage assigned courses, lectures, and view learner progress.
- **Administrator Panel**: Manage learners, instructors, courses, enrollments, and generate reports.

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

6. **Run the Application**
   Start the application:
   ```bash
   python main.py
   ```

## Usage

- **Learner Portal**: View enrolled courses, enroll in new courses, and access course content.
- **Instructor Portal**: Manage assigned courses, lectures, and view learner progress.
- **Administrator Panel**: Manage learners, instructors, courses, and enrollments.

## Troubleshooting

- **ModuleNotFoundError**: Ensure the project root is added to the `PYTHONPATH`:
  ```bash
  export PYTHONPATH=/path/to/SQL_Project:$PYTHONPATH
  ```

- **Database Connection Issues**: Verify your database credentials in `config.py` or environment variables.

## License

This project is licensed under the MIT License.