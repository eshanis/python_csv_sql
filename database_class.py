import mysql.connector # to connect mysql
from mysql.connector import Error

class Database:

    # FUNCTIONS
    # connect mysql without any particular database.
    def create_server_connection(self, host_name, user_name, user_password, db_name):
        connection = None
        print("the database name is", db_name)
        try:
            # GET HANDLE TO THE MYSQL "DOOR"
            if db_name == "NONE":
                connection = mysql.connector.connect(
                    host=host_name,
                    user=user_name,
                    passwd=user_password
                )
                print("connection set to NONE")
            else:
                connection = mysql.connector.connect(
                    host=host_name,
                    user=user_name,
                    passwd=user_password,
                    database=db_name
                )

            print("MySQL Database connection successful")
        except Error as err:
            print(f"Error: '{err}'")
        # RETURN THE DOOR HANDLE
        return connection

    def create_database(self, connection, query):
        cursor = connection.cursor()
        try:
            cursor.execute(query)
            print("Database created successfully")
        except Error as err:
            print(f"Error: '{err}'")

    # THIS FUNCTION WILL RUN A QUERY TO MYSQL CONNECTION
    def execute_query(self, connection, query):
        cursor = connection.cursor()
        try:
            cursor.execute(query)
            connection.commit()
            print("Query successful")
        except Error as err:
            print(f"Error: '{err}'")
    def read_query(self, connection, query):
        cursor = connection.cursor(buffered=True)
        try:
            cursor.execute(query)
            results=cursor.fetchall()
            connection.commit()
            print(results)
            print("Query successful")
        except Error as err:
            print(f"Error: '{err}'")