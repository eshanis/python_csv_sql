class Employee:
    #def __init__(self, first_name, last_name, emp_id, dept_id, manager_name, join_date, dob, age, salary):
    def __init__(self, first_name,last_name,salary,age,doj,manager_name,i,dob):
        self.first_name = first_name
        self.last_name = last_name
        self.emp_id = i
        # self.dept_id = dept_id
        self.manager_name = manager_name
        self.doj = doj
        self.dob = dob
        self.age = age
        self.salary = salary


