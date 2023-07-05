# STEPS
# 1. READ CSV, STORE INTO DATAFRAME
# 2. CREATE NEW ROW IN DATAFRAME, WITH FIRST+LAST NAME
# 3. CONNECT TO MYSQL
# 4. CREATE DATABASE
# 5. CREATE TABLE IN DATABASE WITH COLUMNS MATCHING THE DATAFRAME COLUMNS
# 6. LOOP THROUGH DATAFRAME ROWS AND SAVE TO MYSQL BY CREATING QUERIES

import pandas as pd #module to read csv into dataframe
import mysql.connector # to connect mysql
from mysql.connector import Error
import database_class
from database_class import Database
import logging
import configparser

logging.basicConfig(filename='database.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

try:
    # STEP 1 ====GET DATA FROM CSV INTO DATAFRAME FOR EMPLOYEES===
    data = pd.read_csv('employees.csv')

    df = pd.DataFrame(data)

    print(df.columns)
    print('===')

    # df['new_column'] = df['product_name'] + df['product_id'].astype(str)
    ##2. CREATE NEW ROW IN DATAFRAME, WITH FIRST+LAST NAME
    # ====JOIN 2 COLUMNS, CREATE NEW COLUMN AND ADD TO DATAFRAME===
    df['new_column'] = df['first_name'] + df['last_name']
    # df['doj']= df['doj'].astype(str)
    # df['dob']= df['dob'].astype(str)

    print(df)
    print(df.columns)
    # ====END OF CSV TO DATAFRAME for Employees===

    # STEP 1 ====GET DATA FROM CSV INTO DATAFRAME FOR DEPARTMENT===
    data2 = pd.read_csv('departments.csv')

    # data = pd.read_csv ('products.csv')
    df2 = pd.DataFrame(data2)

    print(df2.columns)
    print('===')


    # ====END OF CSV TO DATAFRAME for DEPARTMENT===

    # 3. SET VARIABLES TO PREPARE TO CONNECT OF MYSQL in config file

    def parse_config():
        config = configparser.ConfigParser()
        config.read('config.ini')
        return config


    # creating an object config and calling it in the method below
    config = parse_config()

    ipaddress = config["ConnectData"]["ipaddress"]
    username = config["ConnectData"]["username"]
    password = config["ConnectData"]["password"]
    dbname = config["ConnectData"]["dbname"]
    port = config["ConnectData"]["port"]  #not used here
    table_name = config["ConnectData"]["table_name"]
    table_name2 = config["ConnectData"]["table_name2"]

    # 3. CONNECT TO MYSQL, saving the "door" handle to variable connection
    #db is the object of class Database()
    #db is cookie and Database is the mould
    db = Database()
    connection = db.create_server_connection(ipaddress,username,password,"NONE")

    print(connection)
    # set up the queries
    # CREATE THE DATABASE, FORM THE QUERY STRING TO CREATE A NEW DATABASE
    create_database_query = "CREATE DATABASE IF NOT EXISTS {dbname}".format(dbname=dbname)
    # CONNECT TO MYSQL USING THE QUERY STRING
    status = db.create_database(connection, create_database_query)

    #overwrite the connection variable to connect to a specific database in this case "testing"
    connection = db.create_server_connection(ipaddress, username, password, dbname)

    #QUERY STRING TO USE TO CREATE TABLE IF IT DOES NOT EXIST
    # employee_id,first_name,last_name,manager_name,salary,age,doj,dob
    # create the query string to create a new EMPLOYEES table with name of the value of variable table_name
    create_product_table_query = """
    CREATE TABLE IF NOT EXISTS {placeholder} (
      employee_id INT PRIMARY KEY,
      first_name VARCHAR(40) NOT NULL,
      last_name VARCHAR(40) NOT NULL,
      manager_name VARCHAR(40) NOT NULL,
      salary INT NOT NULL,
      age INT NOT NULL,
      doj VARCHAR(40) NOT NULL,
      dob VARCHAR(40) NOT NULL,
      dept_id int not null,
      new_column VARCHAR(40) NOT NULL,
      FOREIGN KEY (dept_id) REFERENCES departments(department_id)
      );
     """.format(placeholder=table_name)

    create_department_table_query = """
    CREATE TABLE IF NOT EXISTS {placeholder} (
      department_id INT PRIMARY KEY,
      department_name VARCHAR(40) NOT NULL
      );
     """.format(placeholder=table_name2)


    # THIS ACTUALLY CONNECTS TO MYSQL WITH THE QUERY STRING
    status2 = db.execute_query(connection, create_department_table_query)

    status = db.execute_query(connection, create_product_table_query)

    populate_table = """
    INSERT INTO {table_name} VALUES ({employee_id},'{first_name}','{last_name}','{manager_name}',{salary},{doj},{age},{dob},{dept_id},'{new_column}')
    """

    populate_table2 = """
    INSERT INTO {table_name2} VALUES ({department_id},'{department_name}')
    """
    #print(df2)
    for index, row in df2.iterrows():
        print(index,row)
        print(populate_table2)
        populate_table_query2 = populate_table2.format(table_name2=table_name2, department_id=row['dept_id'],
                                                       department_name=row['dept_name'])
        print(populate_table_query2)
        status2 = db.execute_query(connection, populate_table_query2)

    for index, row in df.iterrows():
        print('in df iterrows')
        #print(row)
        #print(populate_table)
        populate_table_query = populate_table.format(table_name=table_name, employee_id=row['employee_id']+101,
                                                     first_name=row['first_name'], last_name=row['last_name'],
                                                     manager_name=row['manager_name'], salary=row['salary'], age=row['age'],
                                                     doj=row['doj'], dob=row['dob'], dept_id=row['dept_id'],new_column=row['new_column'])
        #print(populate_table_query)
        status = db.execute_query(connection, populate_table_query)



except Exception as e:
    logging.error("Exception occurred", exc_info=True)