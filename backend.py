# backend_fin.py

import psycopg2
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    """Establishes and returns a database connection."""
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("practise"),
            user=os.getenv("postgres"),
            password=os.getenv("tiwari"),
            host=os.getenv("local"),
            port=os.getenv("5432")
        )
        return conn
    except psycopg2.OperationalError as e:
        print(f"Error connecting to database: {e}")
        return None

def create_employee_table():
    """Creates the employees table if it doesn't exist."""
    conn = get_db_connection()
    if conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS employees (
                    employee_id VARCHAR(255) PRIMARY KEY,
                    first_name VARCHAR(255) NOT NULL,
                    last_name VARCHAR(255) NOT NULL,
                    department VARCHAR(50),
                    hire_date DATE,
                    salary DECIMAL(10, 2)
                );
            """)
            conn.commit()
        conn.close()

def seed_database():
    """Inserts sample data into the employees table."""
    conn = get_db_connection()
    if conn:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM employees;")
            if cur.fetchone()[0] == 0:
                sample_data = [
                    ('E101', 'John', 'Doe', 'Engineering', datetime(2020, 1, 15), 95000.00),
                    ('E102', 'Jane', 'Smith', 'Sales', datetime(2019, 5, 20), 80000.00),
                    ('E103', 'Peter', 'Jones', 'Engineering', datetime(2021, 3, 10), 110000.00),
                    ('E104', 'Mary', 'Brown', 'HR', datetime(2018, 9, 5), 75000.00),
                    ('E105', 'David', 'Garcia', 'Sales', datetime(2022, 2, 28), 85000.00)
                ]
                for record in sample_data:
                    cur.execute(
                        "INSERT INTO employees (employee_id, first_name, last_name, department, hire_date, salary) VALUES (%s, %s, %s, %s, %s, %s);",
                        record
                    )
                conn.commit()
        conn.close()

def get_all_employees(department=None, sort_by=None):
    """
    Retrieves a list of all employees, with optional filtering and sorting.
    """
    conn = get_db_connection()
    employees = []
    if conn:
        with conn.cursor() as cur:
            query = "SELECT * FROM employees"
            params = []
            if department and department != 'All':
                query += " WHERE department = %s"
                params.append(department)
            
            if sort_by == 'salary':
                query += " ORDER BY salary DESC"
            elif sort_by == 'hire_date':
                query += " ORDER BY hire_date DESC"
            
            cur.execute(query, params)
            employees = cur.fetchall()
        conn.close()
    return employees

def get_departments():
    """Retrieves a list of unique departments."""
    conn = get_db_connection()
    departments = []
    if conn:
        with conn.cursor() as cur:
            cur.execute("SELECT DISTINCT department FROM employees ORDER BY department;")
            departments = [d[0] for d in cur.fetchall()]
        conn.close()
    return departments

def get_employee_metrics():
    """Calculates and returns various employee metrics."""
    conn = get_db_connection()
    metrics = {
        'total_employees': 0,
        'total_salary_expense': 0,
        'avg_salary': 0,
        'min_salary': 0,
        'max_salary': 0
    }
    if conn:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*), SUM(salary), AVG(salary), MIN(salary), MAX(salary) FROM employees;")
            result = cur.fetchone()
            if result and result[0] is not None:
                metrics['total_employees'] = result[0]
                metrics['total_salary_expense'] = result[1] or 0
                metrics['avg_salary'] = result[2] or 0
                metrics['min_salary'] = result[3] or 0
                metrics['max_salary'] = result[4] or 0
        conn.close()
    return metrics