import datetime
import smtplib
from email.mime.text import MIMEText
import subprocess

#global variables
me = "christian@csbcd.soest.hawaii.edu"
you = "christian@csbcd.soest.hawaii.edu"
s = smtplib.SMTP('localhost')

#get the time right now
now = datetime.datetime.now()

#get the time of the last successful data
#set the string query
query = "SELECT MAX(datetime) from keller_indoor_data;"
output = subprocess.check_output(['psql','natural_ventilation','-c',query],shell=True)
#parse the datetime string out
lastTime=output.split('\n')[2][1:]

#set comparison time delta
timeDifference = now - lastTime

if timeDifference.total_seconds() > 86400:
	#send an email message to myself
	msg = MIMEText("please check the keller automation system")
	msg['Subject'] = "warning, keller system malfunctioning"
	msg['From'] = me
	msg['To'] = you 
	s.sendmail(me,[you],msg.as_string())
else:
	#in the envent everythin is fine, just append to the log for future ref
	file = open("log","a")
	file.write("everything good as of " + str(datetime.datetime.now()))
	file.close()
		

	

