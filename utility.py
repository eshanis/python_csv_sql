from config import *

# creating an object config
config = parse_config()

ipaddress = config["ConnectData"]["ipaddress"]
username = config["ConnectData"]["username"]
password = config["ConnectData"]["password"]
dbname = config["ConnectData"]["dbname"]
port = config["ConnectData"]["port"]  # not used here
table_name = config["ConnectData"]["table_name"]
table_name2 = config["ConnectData"]["table_name2"]

employeescsv = config["filename"]["employees"]
departmentscsv = config["filename"]["departments"]