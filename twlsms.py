from twilio.rest import Client
import mysqlactions as mysql
from keys import conf




def sendsms(to,smstext):
    client = Client(conf.twlheaders()[1],conf.twlheaders()[0])
    message = client.messages \
                    .create(
                         body=smstext,
                         from_='+14696091694',
                         to=str(to)
                 )
    print(message.sid, '\n', ' Message sent to ', str(to) )



def getsmsdetails(run_id, debugmode):
    smsdetails = mysql.qryexec(6, retval=2, run_id=run_id, debugmode=debugmode)
    users_sms_session = []
    if not smsdetails:
        return None
    for userdetails in smsdetails:
        details = []
        username = userdetails[0]
        mobile = userdetails[1]
        msg = userdetails[2]
        msg = "\n Hi " + username+':' + '\n' + msg
        details.append(mobile)
        details.append(msg)
        users_sms_session.append(details)
    return users_sms_session



def sendsmstousers():
    usersarrays = getsmsdetails(run_id=455, debugmode=0)
    if not usersarrays:
        print("No new SMS updates")
        return None
    if len(usersarrays) == 0:
        print("No new SMS to send")
        return None
    for userarr in usersarrays:
        mobile = userarr[0]
        smstxt = userarr[1]
        sendsms(mobile, smstxt)




# sendsms('','Hi Hi')