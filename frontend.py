# frontend_fin.py

import streamlit as st
import pandas as pd
from backend import (
    get_all_employees,
    get_departments,
    get_employee_metrics,
    create_employee_table,
    seed_database
)

# --- App Setup ---
st.set_page_config(
    page_title="HR Employee Directory & Analytics",
    page_icon="📊",
    layout="wide"
)

# --- Initial Database Setup (Run once) ---
create_employee_table()
seed_database()

# --- Functions for CRUD Operations (simulated) ---
# NOTE: In a real app, these would call corresponding backend functions.
def create_employee_in_db(employee_data):
    """Simulates creating an employee in the database."""
    st.success(f"Successfully added new employee: {employee_data['first_name']} {employee_data['last_name']}")
    st.info("Remember to add a real backend function to handle this!")

def update_employee_in_db(employee_id, employee_data):
    """Simulates updating an employee in the database."""
    st.success(f"Successfully updated employee: {employee_id}")
    st.info("Remember to add a real backend function to handle this!")

def delete_employee_from_db(employee_id):
    """Simulates deleting an employee from the database."""
    st.success(f"Successfully deleted employee: {employee_id}")
    st.info("Remember to add a real backend function to handle this!")


# --- UI Layout and Components ---
st.title("HR Employee Directory & Analytics 📊")
st.markdown("A simple application to manage employee data and gain quick insights.")
st.markdown("---")

# --- Business Insights Section ---
st.header("Quick Business Insights ✨")
metrics = get_employee_metrics()
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric(label="Total Employees", value=metrics['total_employees'])
with col2:
    st.metric(label="Total Salary Expense", value=f"${metrics['total_salary_expense']:,.2f}")
with col3:
    st.metric(label="Average Salary", value=f"${metrics['avg_salary']:,.2f}")
with col4:
    st.metric(label="Minimum Salary", value=f"${metrics['min_salary']:,.2f}")
with col5:
    st.metric(label="Maximum Salary", value=f"${metrics['max_salary']:,.2f}")
st.markdown("---")

# --- CRUD Operations Section ---
st.header("Employee Management (CRUD)")
crud_tab = st.tabs(["Create Employee", "Update Employee", "Delete Employee"])

# Tab for CREATE operation
with crud_tab[0]:
    st.subheader("Create a New Employee")
    with st.form("create_form"):
        employee_id = st.text_input("Employee ID", key="create_id")
        first_name = st.text_input("First Name", key="create_first")
        last_name = st.text_input("Last Name", key="create_last")
        department = st.selectbox("Department", get_departments(), key="create_dept")
        hire_date = st.date_input("Hire Date", key="create_date")
        salary = st.number_input("Salary", min_value=0.00, format="%.2f", key="create_salary")
        
        create_button = st.form_submit_button("Add Employee")
        if create_button:
            if not employee_id or not first_name or not last_name:
                st.error("Employee ID, First Name, and Last Name are required.")
            else:
                new_employee = {
                    'employee_id': employee_id,
                    'first_name': first_name,
                    'last_name': last_name,
                    'department': department,
                    'hire_date': hire_date,
                    'salary': salary
                }
                create_employee_in_db(new_employee)

# Tab for UPDATE operation
with crud_tab[1]:
    st.subheader("Update an Existing Employee")
    with st.form("update_form"):
        employees = get_all_employees()
        if employees:
            employee_ids = [emp[0] for emp in employees]
            selected_id = st.selectbox("Select Employee to Update", employee_ids)

            # Pre-populate form with selected employee's data
            selected_employee = next((emp for emp in employees if emp[0] == selected_id), None)
            if selected_employee:
                st.text_input("First Name", value=selected_employee[1], key="update_first")
                st.text_input("Last Name", value=selected_employee[2], key="update_last")
                st.selectbox("Department", get_departments(), index=get_departments().index(selected_employee[3]) if selected_employee[3] in get_departments() else 0, key="update_dept")
                st.date_input("Hire Date", value=selected_employee[4], key="update_date")
                st.number_input("Salary", value=float(selected_employee[5]), min_value=0.00, format="%.2f", key="update_salary")
        
                update_button = st.form_submit_button("Update Employee")
                if update_button:
                    # Collect updated data from form inputs
                    updated_data = {
                        'first_name': st.session_state['update_first'],
                        'last_name': st.session_state['update_last'],
                        'department': st.session_state['update_dept'],
                        'hire_date': st.session_state['update_date'],
                        'salary': st.session_state['update_salary']
                    }
                    update_employee_in_db(selected_id, updated_data)
        else:
            st.warning("No employees found to update.")

# Tab for DELETE operation
with crud_tab[2]:
    st.subheader("Delete an Employee")
    with st.form("delete_form"):
        employees = get_all_employees()
        if employees:
            employee_ids = [emp[0] for emp in employees]
            selected_id_to_delete = st.selectbox("Select Employee to Delete", employee_ids)
            delete_button = st.form_submit_button("Delete Employee")
            
            if delete_button:
                st.warning(f"Are you sure you want to delete employee {selected_id_to_delete}?")
                if st.button("Confirm Delete"):
                    delete_employee_from_db(selected_id_to_delete)
        else:
            st.warning("No employees found to delete.")

st.markdown("---")

# --- Employee Directory & Analytics Table (Read) ---
st.header("Employee Directory")
st.markdown("Use the sidebar to filter and sort employees.")
employees_data = get_all_employees(
    department=st.sidebar.selectbox("Filter by Department", ['All'] + get_departments()),
    sort_by=st.sidebar.selectbox("Sort by", ["None", "salary", "hire_date"]) if st.sidebar.checkbox("Enable Sorting") else None
)

if employees_data:
    df = pd.DataFrame(
        employees_data,
        columns=["Employee ID", "First Name", "Last Name", "Department", "Hire Date", "Salary"]
    )
    df['Salary'] = df['Salary'].apply(lambda x: f"${x:,.2f}")
    st.dataframe(df, use_container_width=True)
else:
    st.info("No employees found with the selected criteria.")
