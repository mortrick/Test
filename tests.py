import mysqlactions as mysql

debugmode = 0
env = 'test'
run_id = 333


a = mysql.qryexec(6, 2, run_id=run_id, debugmode=1, env=env)

print(a[0])  # Truncate the hourly percentage table
print(a[1])