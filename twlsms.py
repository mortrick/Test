# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client


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
                         to='+972'+str(to)
                 )
    print(message.sid, '\n', ' Message sent to ', str(to) )



msg= "Good night friend, may the force be with the bit :) "
sendsms(547549039, msg)

