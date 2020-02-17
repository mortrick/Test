import utils as cnf
import connect as con

dist = ["USD", "BTC"]


for i in dist:
    cnf.load_cmc_data(i)

cnf.execmngsql(2) # Truncate the hourly percentage table
cnf.execmngsql(1) # Insert into hourly percentage table
