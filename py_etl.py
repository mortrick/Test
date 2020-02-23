import mysqlactions as mysql

def sql_etl_order(run_id=0, debugmode=0, env='test'):
    mysql.qryexec(2, 0, run_id=run_id, debugmode=debugmode, env=env)  # Truncate the hourly percentage table
    mysql.qryexec(3, 0, run_id=run_id, debugmode=debugmode, env=env)  # Insert into track percentage table
    mysql.qryexec(4, 0, run_id=run_id, debugmode=debugmode, env=env)  # Insert into sms Q
    mysql.qryexec(5, 0, run_id=run_id, debugmode=debugmode, env=env)  # Move to msg history
    mysql.qryexec(7, 0, run_id=run_id, debugmode=debugmode, env=env)  # Delete msg bulk
    mysql.qryexec(8, 0, run_id=run_id, debugmode=debugmode, env=env)  # Insert into mrrh
    mysql.qryexec(9, 0, run_id=run_id, debugmode=debugmode, env=env)  # Truncate dwh snapshot
    mysql.qryexec(10, 0, run_id=run_id, debugmode=debugmode, env=env)  # insert snapshot to dwh
    mysql.qryexec(11, 0, run_id=run_id, debugmode=debugmode, env=env)  # Truncate mrr
    mysql.updateprocesslog(run_id=run_id, env=env, debugmode=debugmode)  # Update execution log
    print("ETL Process finished on " + env + " environment " + ". Run ID: " + run_id)