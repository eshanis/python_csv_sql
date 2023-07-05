import csv
import logging
import time
import datetime
from random import randrange
from datetime import timedelta
from datetime import date
import random

# ========
import configparser
import department
import employees_no_dept_id
from department import Department
from employees_no_dept_id import Employee

def parse_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config
# creating an object config and calling it in the method below
config = parse_config()
dept_list = []
emp_list = []
logging.basicConfig(filename='employee_data.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')
def department_info():
    dept_names = config["DepartmentData"]["name"].split(',')
    dept_no_min = config["EmployeeData"]["dept_no_min"]
    dept_no_max = config["EmployeeData"]["dept_no_max"]
    print(int(dept_no_min),int(dept_no_max)+1)
    for i in range(int(dept_no_min),int(dept_no_max)+1):
        #print(i)
        name = dept_names[i-1]
        # i += 1
        dept = Department(name, i)
        dept_list.append(dept)

def employee_info():
    emp_names = config["EmployeeData"]["fname"].split(',')
    emp_lnames = config["EmployeeData"]["lname"].split(',')
    salary_min = config["EmployeeData"]["salary_min"]
    salary_max = config["EmployeeData"]["salary_max"]
    age_min = config["EmployeeData"]["age_min"]
    age_max = config["EmployeeData"]["age_max"]
    # for date of joining
    doj_min_year = config["EmployeeData"]["doj_min_year"]  # 1995
    doj_max = datetime.date.today()  # 2023-6-9
    doj_min = datetime.date(year=int(doj_min_year), month=1, day=1)  # 1995-1-1
    man_name = config["EmployeeData"]["mname"].split(',')
    # for date of birth
    dobirth_min_year = config["EmployeeData"]["dobirth_min_year"]  # 1963
    dept_no_min = config["EmployeeData"]["dept_no_min"]
    dept_no_max = config["EmployeeData"]["dept_no_max"]

    #dept_names = config["DepartmentData"]["name"].split(',')
    #no_of_departments = len(dept_names)


    salary_list = range(int(salary_min), int(salary_max) + 1, 10000)
    dept_id_list = range(int(dept_no_min), int(dept_no_max)+1,1)

    age_list = range(int(age_min), int(age_max) + 1, 1)
    base = doj_max  # today's date

    doj_list = [base - datetime.timedelta(days=x) for x in range((doj_max - doj_min).days)]

    for i in range(1000):
        empname = emp_names[i % len(emp_names)]
        emplname = emp_lnames[i % len(emp_lnames)]
        salary = salary_list[i % len(salary_list)]
        age = age_list[i % len(age_list)]
        dept_id = dept_id_list[i % len(dept_id_list)]

        year_of_birth = datetime.date.today().year - age

        month_of_birth = (i) % 12
        day_of_birth = (i) % 31
        if month_of_birth == 0:
            month_of_birth = 1
        if day_of_birth == 0:
            day_of_birth = 1
        if month_of_birth == 2 and day_of_birth > 28:
            day_of_birth = 28
        #print("month_of_birth:", month_of_birth)
        dob = datetime.date(year_of_birth, month_of_birth, day_of_birth)
        #print("dob:", dob)
        k = i
        doj = doj_list[i * 30 % len(doj_list)]
        #print("original doj.year", doj.year, "year_of_birth:", year_of_birth)
        while (doj.year - year_of_birth < 21):
            # print("k:",k,"doj.year-year_of_birth <0:",doj.year-year_of_birth,doj.year,year_of_birth)
            k = k + 1
            doj = doj_list[k * 30 % len(doj_list)]

        #print("revised doj.year", doj.year, "year_of_birth:", year_of_birth)
        mname = man_name[i % len(man_name)]


        # i += 1
        e = Employee(empname, emplname, salary, age, doj, mname, i+101, dob,dept_id)
        emp_list.append(e)
        #print(emp_list[i].first_name, emp_list[i].last_name, emp_list[i].salary, emp_list[i].age, emp_list[i].doj,
        #      emp_list[i].manager_name, emp_list[i].emp_id, emp_list[i].dob,emp_list[i].dept_id)



def generate_data():
    try:
        department_info()
        employee_info()

        # writes to csv file
        # creates headers
        with open('departments.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["dept_id", "dept_name"])
        # appends the file to add data
        with open('departments.csv', 'a', newline='') as file:
            # loop through department list and print dept info
            i = 0
            for dept in dept_list:
                # Write to CSV department
                writer = csv.writer(file)
                writer.writerow([dept_list[i].dept_id, dept_list[i].dept_name])
                i += 1
        ## end of department ==========================

        with open('employees.csv', 'w', newline='') as file2:
            writer2 = csv.writer(file2)
            #make sure the heading are all lower case or there are sql errors
            writer2.writerow(["first_name", "last_name", "salary", "age", "doj", "manager_name", "employee_id", "dob","dept_id"])
        with open('employees.csv', 'a', newline='') as file2:
            # loop through employee list and print employee info
            i = 0
            for i in range(len(emp_list)):
                # Write to CSV employee
                writer2 = csv.writer(file2)
                writer2.writerow(
                    [emp_list[i].first_name, emp_list[i].last_name, emp_list[i].salary, emp_list[i].age,
                     emp_list[i].doj,
                     emp_list[i].manager_name, emp_list[i].emp_id, emp_list[i].dob,emp_list[i].dept_id])
                i += 1

    except Exception as e:
        logging.error("Exception occurred", exc_info=True)



generate_data()