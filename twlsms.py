# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client
import mysqlactions as mysql


# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure
account_sid = 'AC57752e2d163c71ea1ae87df429664134'
auth_token = 'f4290498f1bf19666ffd5a9088d2113c'
client = Client(account_sid, auth_token)



def sendsms(to,smstext):
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




# sendsms('+972547549039', 'test')
sendsmstousers()
