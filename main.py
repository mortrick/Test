#!/usr/bin/env python

import utils as cnf
import mysqlactions as mysql
import time
from logs import dynamic_log

dist = ["USD"]



for i in dist:
    cnf.load_cmc_data(i, debugmode=0)
time.sleep(5)

mysql.qryexec(2) # Truncate the hourly percentage table
mysql.qryexec(1) # Insert into hourly percentage table
