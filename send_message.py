# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client

# Your Account Sid and Auth Token from twilio.com/console
account_sid = 'AC8374e3e36336912fa96d26ef37f53ebc'
auth_token = '63d68c8915d21c771debcdb9176d7eef'
client = Client(account_sid, auth_token)
from_ = '+16613472841'
to_ = '+16508625835'

def send_message(file_name, size, totalSize):
	message = client.messages \
	                .create(
	                     body="Someone just uploaded a file, called {} having size {},  to NoteDex! You have used {} \
	                      since last restart".format(file_name, size, totalSize),
	                     from_=from_,
	                     to=to_
	                 )

	print(message.sid)
