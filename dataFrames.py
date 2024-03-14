import pandas as pd
import sqlite3

# Load CSV data into Pandas data frames
df_employee = pd.read_csv('Relations/employee.csv')
df_salary = pd.read_csv('Relations/salary.csv')
df_department = pd.read_csv('Relations/department.csv')
df_female = pd.read_csv('Relations/female.csv')
df_male = pd.read_csv('Relations/male.csv')
df_project = pd.read_csv('Relations/project.csv')
df_supervise = pd.read_csv('Relations/supervise.csv')
df_workson = pd.read_csv('Relations/workson.csv')

# Connect to the SQLite database

conn = sqlite3.connect('company.db')

# Drop existing tables if they exist
conn.execute("DROP TABLE IF EXISTS employee;")
conn.execute("DROP TABLE IF EXISTS salary;")
conn.execute("DROP TABLE IF EXISTS department;")
conn.execute("DROP TABLE IF EXISTS female;")
conn.execute("DROP TABLE IF EXISTS male;")
conn.execute("DROP TABLE IF EXISTS project;")
conn.execute("DROP TABLE IF EXISTS supervise;")
conn.execute("DROP TABLE IF EXISTS workson;")

# Load DataFrames into SQLite tables
df_employee.to_sql('employee', conn, index=False)
df_salary.to_sql('salary', conn, index=False)
df_department.to_sql('department', conn, index=False)
df_female.to_sql('female', conn, index=False)
df_male.to_sql('male', conn, index=False)
df_project.to_sql('project', conn, index=False)
df_supervise.to_sql('supervise', conn, index=False)
df_workson.to_sql('workson', conn, index=False)

# Define the SQL query
q1_query = """
           SELECT e.*
           FROM employee e
           JOIN workson w ON e.EMPLOYEE_NAME = w.NAME
           JOIN supervise s ON e.EMPLOYEE_NAME = s.SUBORDINATE
           WHERE w.PROJECT = 'computerization'
           AND w.EFFORT = 10
           AND s.SUPERVISOR = 'jennifer'
           """
q2_query = """
           SELECT e.*
           FROM employee e
           JOIN salary s ON e.EMPLOYEE_NAME = s.EMPLOYEE_NAME
           JOIN department d ON e.EMPLOYEE_NAME = d.EMPLOYEE_NAME
           WHERE s.SALARY > 40000
           AND d.DEPARTMENT = 'research';
           """
q3_query = """
           SELECT e.*
           FROM employee e
           WHERE e.EMPLOYEE_NAME NOT IN (
               SELECT SUBORDINATE
               FROM supervise);
           """
q4_query = """
           SELECT e.*
           FROM employee e
           JOIN workson w ON e.EMPLOYEE_NAME = w.NAME
           WHERE w.PROJECT = 'productx' AND w.EFFORT >= 20;
           """

# Execute the query
q1_result = conn.execute(q1_query).fetchall()
q2_result = conn.execute(q2_query).fetchall()
q3_result = conn.execute(q3_query).fetchall()
q4_result = conn.execute(q4_query).fetchall()

# Print the result
print("Employees who meet the criteria for Q1:")
for row in q1_result:
    print(row)
print("Employees who meet the criteria for Q2:")
for row in q2_result:
    print(row)
print("Employees who meet the criteria for Q3:")
for row in q3_result:
    print(row)
print("Employees who meet the criteria for Q3:")
for row in q4_result:
    print(row)


# Close the database connection
conn.close()
