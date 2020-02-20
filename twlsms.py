# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client
import mysqlactions as mysql


# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure
account_sid = 'ACb352b34e2bb687283c79e99d96034490'
auth_token = '496d2ec9629ca1a251426cafb9fc88c2'
client = Client(account_sid, auth_token)



def sendsms(to,smstext):
    message = client.messages \
                    .create(
                         body=smstext,
                         from_='+18317039336',
                         to=+str(to)
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


#
# mobile = details[2]
# msg = details[3]

# mysql.qryexec(3, 0, run_id=3423, debugmode=0)  # Insert into sms Q
print(getsmsdetails(run_id=455, debugmode=0))
