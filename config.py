import psycopg2 as pysql
from configparser import ConfigParser

# conn = pysql.connect(host="localhost", database="postgres", user="admin", password="admin")


def config(filename = 'database.ini', section ='postgresql' ):
    parser = ConfigParser()
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))
    return db


