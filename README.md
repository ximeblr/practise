# practise
domain
HR Employee Directory & Analytics
This is a full-stack, data-driven Human Resources application built with Python. It provides a simple, interactive dashboard for an HR department to manage employee data and gain quick business insights. The application uses Streamlit for the frontend and connects to a PostgreSQL database for data storage.

Features
Employee Directory: View a complete list of all employees in a clean, interactive table.

Filtering & Sorting: Easily filter the employee list by department and sort it by salary or hire date.

Business Insights: Get at-a-glance analytics with key metrics, including:

Total number of employees (COUNT)

Total monthly salary expense (SUM)

Average salary (AVG)

Lowest and highest salaries (MIN and MAX)

CRUD Operations: Manage employee data directly from the frontend with dedicated tabs for:

Create: Add new employees to the database.

Update: Modify existing employee records.

Delete: Remove employees from the directory.

Prerequisites
Before running the application, ensure you have the following installed:

Python 3.x

PostgreSQL

pip (Python package installer)

Setup and Installation
Follow these steps to get the application running on your local machine.

Clone the Repository

git clone https://github.com/your-username/your-repo.git
cd your-repo

Create a Virtual Environment (Recommended)

python -m venv venv
source venv/bin/activate   # On Windows, use `venv\Scripts\activate`

Install Dependencies

pip install streamlit psycopg2-binary pandas python-dotenv

Configure the Database

Set up a PostgreSQL database.

Create a .env file in the project's root directory and add your database credentials. This keeps your sensitive information secure.

DB_NAME=your_db_name
DB_USER=your_username
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

Run the Application
From the project's root directory, run the Streamlit application. This will automatically create the employees table and seed it with sample data if it's empty.

streamlit run frontend_fin.py

File Structure
├── .env                  # Environment file for database credentials
├── frontend_fin.py       # Streamlit application UI (Frontend)
├── backend_fin.py        # PostgreSQL database operations (Backend)
└── README.md             # This file
