#!/usr/bin/env python

import utils as cnf
import mysqlactions as mysql
import time
from logs import dynamic_log

debugmode = 0
run_id = cnf.getrunid_str()

dist = ["USD", "BTC"]

for i in dist:
    cnf.load_cmc_data(i, debugmode=debugmode, run_id=run_id)
time.sleep(1)

# Move to agg tables and operate the last execution data around the system
mysql.qryexec(1, 0, run_id=run_id, debugmode=debugmode)  # Truncate the hourly percentage table
mysql.qryexec(2, 0, run_id=run_id, debugmode=debugmode)  # Insert into hourly percentage table
mysql.qryexec(3, 0, run_id=run_id, debugmode=debugmode)  # Insert into sms Q
mysql.qryexec(4, 0, run_id=run_id, debugmode=debugmode)  # Move to history


