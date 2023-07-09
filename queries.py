
import pandas as pd #module to read csv into dataframe
import mysql.connector # to connect mysql
from mysql.connector import Error
import database_class
from database_class import Database
import logging
import configparser
import config
from config import *
from utility import *
import pandas as pd #module to read csv into dataframe
import sqlalchemy

logging.basicConfig(filename='database.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

try:

    # STEP 1 ====GET DATA FROM CSV INTO DATAFRAME FOR DEPARTMENT===

    #data = pd.read_csv('departments.csv')

    #below pandas is reading from utilities.py file not hard coded.
    data = pd.read_csv(departmentscsv)
    # data = pd.read_csv ('products.csv')
    df = pd.DataFrame(data)

    #print(df)
    print('===')

    # def parse_config():
    #     config = configparser.ConfigParser()
    #     config.read('config.ini')
    #     return config


    # creating an object config and calling it in the method below

    # config = parse_config()
    #
    # ipaddress = config["ConnectData"]["ipaddress"]
    # username = config["ConnectData"]["username"]
    # password = config["ConnectData"]["password"]
    # dbname = config["ConnectData"]["dbname"]
    # port = config["ConnectData"]["port"]  #not used here
    # table_name = config["ConnectData"]["table_name"]
    # table_name2 = config["ConnectData"]["table_name2"]

    # 3. CONNECT TO MYSQL, saving the "door" handle to variable connection
    #db is the object of class Database()
    #db is cookie and Database is the mould
    db = Database()

    #getting the server_connection info from database_class.py which gets it from config.ini
    connection = db.create_server_connection(ipaddress, username, password, dbname)


    get_info = """select * from  {placeholder};""".format(placeholder=table_name2)
    get_info = """ select * FROM employees LEFT JOIN departments ON employees.dept_id = departments.dept_id;"""
    get_info = """ select employee_id, new_column, salary, dept_id from employees where salary = (select max(salary) from employees where salary < (select max(salary) from employees));"""

    query = """
    	select employees.employee_id, employees.new_column, employees.salary, 
    	departments.dept_id, departments.dept_name from employees 
    	join departments on employees.dept_id = departments.dept_id 
    	where salary = (select max(salary) from employees where salary < (select max(salary) 
    	from employees));
    """
    query3 = """
        	select * from employees 
        	where salary = (select max(salary) from employees where salary < (select max(salary) 
        	from employees));
        """

    query3 = """
            	with res as (select salary, dept_id, employee_id, new_column, 
            	rank() over (partition by dept_id order by salary desc) x_rank from employees)
            	select res.employee_id, res.new_column, res.dept_id, res.salary from res where x_rank = 2; 
            """

    #use pandas to read the sql query and save in variable emps, requires two parameters :connection and query
    emps = pd.read_sql_query(con=connection, sql=query3)
    #print(get_info)
    #print(query)
    print("printing emps below")
    print(emps.to_string())

    # assigning a new value to df and merging the emps and department tables on dept_id
    df = df.merge(emps, on="dept_id")
    print(df)

    # THIS ACTUALLY CONNECTS TO MYSQL WITH THE QUERY STRING

    #status = db.read_query(connection, get_info)
    #status2 = db.read_query(connection, query)
    # status3 = db.read_query(connection, query3)
    # print(status3)


except Exception as e:
    logging.error("Exception occurred", exc_info=True)