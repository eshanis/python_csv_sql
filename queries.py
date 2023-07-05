
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

    #overwrite the connection variable to connect to a specific database in this case "testing"
    connection = db.create_server_connection(ipaddress, username, password, dbname)


    get_info = """select * from  {placeholder};""".format(placeholder=table_name2)
    get_info = """ select * FROM employees LEFT JOIN departments ON employees.dept_id = departments.department_id;"""



    print(get_info)
    # THIS ACTUALLY CONNECTS TO MYSQL WITH THE QUERY STRING

    status = db.read_query(connection, get_info)



except Exception as e:
    logging.error("Exception occurred", exc_info=True)