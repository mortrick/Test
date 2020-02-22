# Download the helper library from https://www.twilio.com/docs/python/install
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



# msg= "Good night friend, may the force be with the bit :) "
# sendsms(547549039, msg)



def getsmsdetails(run_id, debugmode):
    smsdetails = mysql.qryexec(5, retval=2, run_id=run_id, debugmode=debugmode)
    users_sms_session = []
    if not smsdetails:
        return None
    for userdetails in smsdetails:
        details = []
        username = userdetails[0]
        mobile = userdetails[2]
        msg = userdetails[3]
        msg = "Hi " + username + '...\n' + msg
        details.append(mobile)
        details.append(msg)
        users_sms_session.append(details)
    return users_sms_session



def sendsmstousers():
    usersarrays = getsmsdetails(run_id=455, debugmode=0)
    for userarr in usersarrays:
        mobile = userarr[0]
        smstxt = userarr[1]
        sendsms(mobile, smstxt)




# sendsms('+972528281888', 'test')
# sendsmstousers()
