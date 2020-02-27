#!/usr/bin/env python3

import pymysql
from logs import dynamic_log as dl
from keys import conf

dbconf = conf.dbconf()

def getqrystr(numb,  env='test'):
    if env != 'test':
        sql = "select query_str, query_name from mng.environment_queries where query_id = " + str(numb) + " limit 1"
    else:
        sql = "select query_str, query_name from mng_test.environment_queries where query_id = " + str(numb) + " limit 1"
    db = pymysql.connect(dbconf[0], dbconf[1], dbconf[2])
    cursor = db.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    for row in data:
        qry = row[0]
        qry_name = row[1]
    output = [qry, qry_name]
    if env == 'test':
        output[0] = qry.replace("{env}", '_test')
        db.close()
        return output
    else:
        db.close()
        return output


def qryexec(numb, retval=0, run_id=0, debugmode=0, env='test'):
    if not numb:
        return None
    db = pymysql.connect(dbconf[0], dbconf[1], dbconf[2])
    cursor = db.cursor()
    if type(numb) == int:
        if retval == 1:
            querydetails = getqrystr(numb,  env=env)
            qry = querydetails[0]
            qry_name = querydetails[1]
            print("Next step - ", qry_name)
            cursor.execute(qry)
            # Add Debug
            dl.writelog(dl.logpath(run_id), "Successfully execute the query :" + qry_name + '\n' + qry[:1500], debugmode)
            ans = cursor.fetchone()
            db.close()
            # Add debug
            dl.writelog(dl.logpath(run_id), "Successfully executed and the results are : " + '\n' + str(ans[:1500]), debugmode)
            return ans
        elif retval == 2:
            qry = getqrystr(numb,  env=env)[0]
            qry_name = getqrystr(numb, env=env)[1]
            print("Next step - ", qry_name)
            cursor.execute(qry)
            ans = cursor.fetchall()
            db.close()
            dl.writelog(dl.logpath(run_id), "Successfully executed and the results are : " + '\n' + str(ans[:1500]), debugmode)
            return ans
        else:
            qry = getqrystr(numb,  env=env)[0]
            qry_name = getqrystr(numb, env=env)[1]
            print("Next step - ", qry_name)
            cursor.execute(qry)
            db.commit()
            db.close()
            dl.writelog(dl.logpath(run_id), "Successfully execute and commit the sql : " + '\n' + qry[:1500], debugmode)
    else:
        try:
            cursor.execute(numb)
            dl.writelog(dl.logpath(run_id), 'The query bellow successfully executed \n' + numb[:1500], debugmode)
        except pymysql.err as e :
            msg = "Couldnt execute the query " + 'Failed to execute the the sql ' + numb + '\n Because of an error ' + e
            dl.writelog(dl.logpath(run_id), msg[:1500], debugmode)
            print(msg)
        if retval == 1:
            ans = cursor.fetchone()
            db.close()
            return ans
        elif retval == 2:
            ans = cursor.fetchall()
            db.close()
            return ans
        else:
            db.commit()
            db.close()


def updateprocesslog(run_id=0, env='unknown', debugmode=0):
    sql = 'insert into mng.process_execution_log (run_id, env,debug_mode)'
    values = 'values ('+str(run_id)+',' + "'" +env + "'" +',' + str(debugmode) + ')'
    finsql = sql + values
    qryexec(numb=finsql, retval=0, run_id=run_id, debugmode=debugmode, env=env)
