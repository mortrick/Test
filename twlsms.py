#!/usr/bin/env python3


from twilio.rest import Client
import mysqlactions as mysql
from keys import conf
from logs import dynamic_log as dl



def sendsms(to,smstext):
    client = Client(conf.twlheaders()[1],conf.twlheaders()[0])
    message = client.messages \
                    .create(
                         body=smstext,
                         from_='+14696091694',
                         to=str(to)
                 )
    print(message.sid, '\n', ' Message sent to ', str(to) )



def getsmsdetails(run_id, debugmode,env='test'):
    smsdetails = mysql.qryexec(6, retval=2, run_id=run_id, debugmode=debugmode, env=env)
    users_sms_session = []
    if not smsdetails:
        return None
    for userdetails in smsdetails:
        details = []
        if not userdetails:
            print('No user to be alerted received from query_id 6, try to keep it full and check')
            return None
        else:
            username = userdetails[0]
        mobile = userdetails[1]
        msg = userdetails[2]
        newalerts = userdetails[3]
        alerttypes = userdetails[4]
        msg = "\n- \n\n\n Hi " + username+':' + '\n' + msg
        details.append(mobile)
        details.append(msg)
        users_sms_session.append(details)
        print(str(newalerts), " Alerts found for user " + username, 'and with '+ str(alerttypes) + " alert types")
        dl.writelog(dl.logpath(run_id), str(newalerts) + " Alerts found for user " + username + ' and with ' + str(alerttypes) + "alert types", debugmode)
    return users_sms_session



def sendsmstousers(env='test'):
    usersarrays = getsmsdetails(run_id=455, debugmode=0,env=env)
    if not usersarrays:
        print("Empty param received for user array function")
        return None
    if len(usersarrays) == 0:
        print("No new SMS to send")
        return None
    for userarr in usersarrays:
        mobile = userarr[0]
        smstxt = userarr[1]
        sendsms(mobile, smstxt)
