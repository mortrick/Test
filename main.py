#!/usr/bin/env python
import utils as cnf
import mysqlactions as mysql
import time
import sys
import twlsms as twl
from keys import conf

env = sys.argv[1]
debugmode = sys.argv[2]
run_id = cnf.getrunid_str()
dist = ["USD", "BTC"]
print("Runid is " + str(run_id))

if 3 < len(sys.argv) < 3:
    print("Please supply env expected to receive 1 env argument test or prod")
else:
    for i in dist:
        cnf.load_cmc_data(i, debugmode=debugmode, run_id=run_id)
    time.sleep(5)
    # Check the inserted run_id in the database
    session_rid_validation = mysql.qryexec(numb=1, retval=1, run_id=run_id, debugmode=debugmode, env=env)[0]
    try:
        # Before executing the other process, this step will validate we have new data
        print("Expect to find in table run id = " , run_id, " but found ", str(session_rid_validation))
        print("Validation check passed - The generated runid found in data ")
    except :
        smsdata = conf.devdata(expected_run_id=run_id, foundrid=session_rid_validation)
        print(smsdata[1])
        twl.sendsms(to=smsdata[0], smstext=smsdata[1])
        # Move to agg tables and operate the last execution data around the system
mysql.qryexec(2, 0, run_id=run_id, debugmode=debugmode, env=env)  # Truncate the hourly percentage table
mysql.qryexec(3, 0, run_id=run_id, debugmode=debugmode, env=env)  # Insert into track percentage table
mysql.qryexec(4, 0, run_id=run_id, debugmode=debugmode, env=env)  # Insert into sms Q
mysql.qryexec(5, 0, run_id=run_id, debugmode=debugmode, env=env)  # Move to msg history
mysql.qryexec(7, 0, run_id=run_id, debugmode=debugmode, env=env)  # Delete msg bulk
mysql.qryexec(8, 0, run_id=run_id, debugmode=debugmode, env=env)  # Insert into mrrh
mysql.qryexec(9, 0, run_id=run_id, debugmode=debugmode, env=env)  # Truncate mrr
mysql.updateprocesslog(run_id=run_id, env=env, debugmode=debugmode)

