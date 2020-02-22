#!/usr/bin/env python
import utils as cnf
import mysqlactions as mysql
import time
import sys
import twlsms as twl
from keys import conf

env = sys.argv[1]
debugmode = 0
run_id = cnf.getrunid_str()
dist = ["USD", "BTC"]
print("Runid is " + str(run_id))

if len(sys.argv) < 2:
    print("Please supply env")
else:
    for i in dist:
        cnf.load_cmc_data(i, debugmode=debugmode, run_id=run_id)
    time.sleep(1)
    # Check the inserted run_id in the database
    session_rid_validation = mysql.qryexec(numb=1, retval=1, run_id=run_id, debugmode=debugmode, env=env)[0]
    try:
        # Before executing the other process, this step will validate we have new data
        assert str(session_rid_validation) == str(run_id)
        print("Validation check passed - The generated runid found in data ")
        # Move to agg tables and operate the last execution data around the system
        mysql.qryexec(2, 0, run_id=run_id, debugmode=debugmode, env=env)  # Truncate the hourly percentage table
        mysql.qryexec(3, 0, run_id=run_id, debugmode=debugmode, env=env)  # Insert into hourly percentage table
        mysql.qryexec(4, 0, run_id=run_id, debugmode=debugmode, env=env)  # Insert into sms Q
        mysql.qryexec(5, 0, run_id=run_id, debugmode=debugmode, env=env)  # Move to msg history
        mysql.qryexec(6, 0, run_id=run_id, debugmode=debugmode, env=env)  # Delete msg bulk
        mysql.qryexec(7, 0, run_id=run_id, debugmode=debugmode, env=env)  # Insert into mrrh
        mysql.qryexec(8, 0, run_id=run_id, debugmode=debugmode, env=env)  # Truncate mrr
    except:
        print("The expected run_id didn't found in the data")
        twl.sendsms(conf.devdata()[0], conf.devdata()[1])





