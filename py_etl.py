#!/usr/bin/env python3


import mysqlactions as mysql
import twlsms as tw
import time

def sql_etl_order(run_id=0, debugmode=0, env='test'):
    mysql.qryexec(2, 0, run_id=run_id, debugmode=debugmode, env=env)
    mysql.qryexec(3, 0, run_id=run_id, debugmode=debugmode, env=env)
    time.sleep(2)
    print("Move the tracked rows to SMS table")
    mysql.qryexec(4, 0, run_id=run_id, debugmode=debugmode, env=env)
    time.sleep(2)
    # Move to SMS Q
    mysql.qryexec(5, 0, run_id=run_id, debugmode=debugmode, env=env)
    time.sleep(3)
    tw.sendsmstousers()
    time.sleep(1)
    mysql.qryexec(7, 0, run_id=run_id, debugmode=debugmode, env=env)
    time.sleep(1)
    mysql.qryexec(8, 0, run_id=run_id, debugmode=debugmode, env=env)
    time.sleep(2)
    mysql.qryexec(9, 0, run_id=run_id, debugmode=debugmode, env=env)
    time.sleep(3)
    mysql.qryexec(10, 0, run_id=run_id, debugmode=debugmode, env=env)
    time.sleep(2)
    mysql.qryexec(11, 0, run_id=run_id, debugmode=debugmode, env=env)
    time.sleep(3)
    mysql.updateprocesslog(run_id=run_id, env=env, debugmode=debugmode)
    time.sleep(3)
    print("ETL Process finished on " + env + " environment " + ". Run ID: " + run_id)