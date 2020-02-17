import utils as cnf
import mysqlactions as mysql

dist = ["USD"]


for i in dist:
    cnf.load_cmc_data(i)

mysql.qryexec(2) # Truncate the hourly percentage table
mysql.qryexec(1) # Insert into hourly percentage table
