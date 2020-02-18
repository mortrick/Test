#!/usr/bin/env python

import utils as cnf
import mysqlactions as mysql
import time
from logs import dynamic_log

run_id = cnf.getrunid_str()


dist = ["USD", "BTC"]

for i in dist:
    cnf.load_cmc_data(i, debugmode=1, run_id=run_id)
time.sleep(2)

mysql.qryexec(2) # Truncate the hourly percentage table
mysql.qryexec(1) # Insert into hourly percentage table
