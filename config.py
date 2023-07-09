import configparser


def parse_config():
	config = configparser.ConfigParser()
	config.read('config.ini')
	return config