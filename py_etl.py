#!/usr/bin/env python3


import mysqlactions as mysql
import twlsms as tw
import time

def sql_etl_order(run_id=0, debugmode=0, env='test'):
    print("Truncate tracking percentage table")
    mysql.qryexec(2, 0, run_id=run_id, debugmode=debugmode, env=env)  # Truncate the hourly percentage table
    time.sleep(3)
    print("Insert into percentage tracking table")
    mysql.qryexec(3, 0, run_id=run_id, debugmode=debugmode, env=env)  # Insert into track percentage table
    time.sleep(3)
    print("Move the tracked rows to SMS table")
    mysql.qryexec(4, 0, run_id=run_id, debugmode=debugmode, env=env)  # Insert into sms Q
    time.sleep(3)
    print("Move to SMS Q")
    mysql.qryexec(5, 0, run_id=run_id, debugmode=debugmode, env=env)  # Move to msg history
    time.sleep(3)
    print("Send SMS Message to the user ")
    tw.sendsmstousers()  # Send sms if need
    time.sleep(3)
    print("delete message bulk")
    mysql.qryexec(7, 0, run_id=run_id, debugmode=debugmode, env=env)  # Delete msg bulk
    time.sleep(3)
    print("Transfer last data from response to MRRH")
    mysql.qryexec(8, 0, run_id=run_id, debugmode=debugmode, env=env)  # Insert into mrrh
    time.sleep(3)
    print("Truncate Snapshot table ")
    mysql.qryexec(9, 0, run_id=run_id, debugmode=debugmode, env=env)  # Truncate dwh snapshot
    time.sleep(3)
    print("Insert into snapshot table Snapshot table ")
    mysql.qryexec(10, 0, run_id=run_id, debugmode=debugmode, env=env)  # insert snapshot to dwh
    time.sleep(3)
    print("Truncate MRR before last execution")
    mysql.qryexec(11, 0, run_id=run_id, debugmode=debugmode, env=env)  # Truncate mrr
    time.sleep(3)
    print("Update execution log")
    mysql.updateprocesslog(run_id=run_id, env=env, debugmode=debugmode)  # Update execution log
    time.sleep(3)
    print("ETL Process finished on " + env + " environment " + ". Run ID: " + run_id)