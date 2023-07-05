from datetime import datetime
import subprocess

LOG_FILE_LOCATION = '/var/log/messages'
PROJECT_LOCATION = '/root/occtl_telegram_bot'

#you should write your date here
#Apr 12
#Apr  8 (one more space)
DATE = 'May  8'

# this function will get all data from log file (/var/log/messages) and save it to users_traffic.txt file for specific date
# you may change LOG_FILE_LOCATION
def users_traffic_cron_function():
	try:
		awk_command = r"""awk '/ocserv.* user disconnected/ && /""" + DATE + r""" / && /main\[/ {match($0, /main\[(.*)\]/, a); user=a[1]; split($0,b,"[ =]"); rx_bytes=b[length(b)-2]; tx_bytes=b[length(b)]; data[user]+=rx_bytes; data[user]+=tx_bytes} END {for (user in data) {printf ("%s %.2f GB\n", user, data[user]/1024/1024/1024)}}' """ + LOG_FILE_LOCATION + r""" | sort -k2nr"""
		message = subprocess.check_output(awk_command, shell=True)
		message = message.decode()
		final_message = ""
		for line in (message.splitlines()):
			final_message = final_message + f"{DATE} user:::" + line + "\n"
		with open(f'{PROJECT_LOCATION}/users_traffic.txt', 'a') as f:
			f.write(final_message)
	except Exception as e:
		print('Error:', e)

users_traffic_cron_function()
