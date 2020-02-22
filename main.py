#!/usr/bin/env python

import utils as cnf
import mysqlactions as mysql
import time
import sys

env = sys.argv[1]
debugmode = 0
run_id = cnf.getrunid_str()
dist = ["USD", "BTC"]

if len(sys.argv) <2:
    print("Please supply env")
else:
    for i in dist:
        cnf.load_cmc_data(i, debugmode=debugmode, run_id=run_id)
    time.sleep(1)

    # Move to agg tables and operate the last execution data around the system
    mysql.qryexec(1, 0, run_id=run_id, debugmode=debugmode, env=env)  # Truncate the hourly percentage table
    mysql.qryexec(2, 0, run_id=run_id, debugmode=debugmode, env=env)  # Insert into hourly percentage table
    mysql.qryexec(3, 0, run_id=run_id, debugmode=debugmode, env=env)  # Insert into sms Q
    mysql.qryexec(4, 0, run_id=run_id, debugmode=debugmode, env=env)  # Move to msg history
    mysql.qryexec(6, 0, run_id=run_id, debugmode=debugmode, env=env)  # Delete msg bulk
    mysql.qryexec(7, 0, run_id=run_id, debugmode=debugmode, env=env)  # Insert into mrrh
    mysql.qryexec(8, 0, run_id=run_id, debugmode=debugmode, env=env)  # Truncate mrr




