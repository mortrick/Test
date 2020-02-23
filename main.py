#!/usr/bin/env python
import utils as cnf
import mysqlactions as mysql
import time
import sys
import twlsms as twl
from keys import conf
import py_etl as etl

env = sys.argv[1]
debugmode = int(sys.argv[2])
run_id = cnf.getrunid_str()
print("Runid is " + str(run_id))
success = 0


if 3 < len(sys.argv) < 3:
    print("Please supply env expected to receive 1 env argument test or prod")
else:
    cnf.load_cmc_data(debugmode=debugmode, run_id=run_id, env=env)
    time.sleep(2)
    # Check the inserted run_id in the database
    session_rid_validation = mysql.qryexec(numb=1, retval=1, run_id=run_id, debugmode=debugmode, env=env)[0]
    try:
        # Before executing the other process, this step will validate we have new data
        assert str(run_id) == str(session_rid_validation)
        print("Validation check passed - The generated runid found in data ")
        success = 1
    except :
        # Update the developer if
        smsdata = conf.devdata(expected_run_id=run_id, foundrid=session_rid_validation)
        print(smsdata[1])
        twl.sendsms(to=smsdata[0], smstext=smsdata[1])
        # Move to agg tables and operate the last execution data around the system

# If the data was extracted and the generated runid observed in the data
# Execute the ETL from py_etl (a series of sqls to be execute by the order)

if success == 1:
    print("Start ETL")
    etl.sql_etl_order(run_id=run_id, debugmode=debugmode, env=env)