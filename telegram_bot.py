from telegram import Update
import subprocess
from passlib.hash import sha256_crypt
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from datetime import datetime
import io

PROJECT_LOCATION = '/root/occtl_telegram_bot'
CHANNEL_ID = 'YOUR CHANNEL ID'
ADMIN_ID = 'YOUR ADMIN ID'
BOT_TOKEN = 'YOUR BOT TOKEN'



# this message shows the user's options when user starts your bot.
'''
input:
/start
result: 
you must write this command to see your network usage:
/disconnect username password
you must write this command to disconnect all of your devices:
/get_bandwidth username password
'''
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
	await context.bot.send_message(chat_id=update.effective_chat.id, text='you must write this command to see your network usage:\n/disconnect username password'
	                                                                      '\nyou must write this command to disconnect all of your devices:\n/get_bandwidth username password')

# this function let the ADMIN knows a specific date bandwidth (e.g: /get_stat May 08 or /get_stat May (sum of whole May))
# this will get you 6 users that used the most in that date time
'''
input:
/get_stat Jun
result: 
Jun
username1 123.71
username2 110.6
username3 107.46
username4 106.39
username5 105.55
username6 102.08
'''
async def get_stat(update: Update, context: ContextTypes.DEFAULT_TYPE):
	if update.effective_chat.id == ADMIN_ID:
		try:
			date = ""
			if len(context.args) != 0:
				for message in context.args:
					date = date + " " + message
				date = date[1:]
			awk_command = r"""awk '/user:::/ && /""" + date + r"""/{ split($3, a, ":::"); users[a[2]] += $4 } END { for (user in users) print user, users[user] }' """ + PROJECT_LOCATION + r"""/users_traffic.txt | sort -k2nr"""
			message = subprocess.check_output(awk_command, shell=True)
			message = message.decode()
			if (len('\n'.join(message.splitlines())) > 6):
				message = '\n'.join(message.splitlines()[:6])
			message = date + '\n' + message
			print(message)
			await context.bot.send_message(chat_id=CHANNEL_ID, text=message)

		except Exception as e:
			print(e)
	else:
		message = 'method not allowed'
		await context.bot.send_message(chat_id=CHANNEL_ID, text=message + '\n' + str(update.effective_chat.id))
		await context.bot.send_message(chat_id=update.effective_chat.id, text=message)

# this function let the ADMIN knows a specific user's bandwidth in special day (e.g: /get_stat May 08 username or /get_stat May username (sum of whole May))
'''
input:
/get_user_stat Jun username1
result:
Jun
username1 20.4
'''
async def get_user_stat(update: Update, context: ContextTypes.DEFAULT_TYPE):
	if len(context.args) != 0:
		if update.effective_chat.id == ADMIN_ID:
			try:
				date = ""
				for i in range(len(context.args) - 1):
					message = context.args[i]
					date = date + " " + message
				date = date[1:]
				awk_command = r"""awk '/user:::""" + context.args[-1] + r""" / && /""" + date + r"""/{ split($3, a, ":::"); users[a[2]] += $4 } END { for (user in users) print user, users[user] }' """ + PROJECT_LOCATION + r"""/users_traffic.txt | sort -k2nr"""
				message = subprocess.check_output(awk_command, shell=True)
				message = message.decode()
				if (len('\n'.join(message.splitlines())) > 6):
					message = '\n'.join(message.splitlines()[:6])
				message = date + '\n' + message
				print(message)
				await context.bot.send_message(chat_id=CHANNEL_ID, text=message)

			except Exception as e:
				print(e)
		else:
			message = 'method not allowed'
			await context.bot.send_message(chat_id=CHANNEL_ID, text=message + '\n' + str(update.effective_chat.id))
			await context.bot.send_message(chat_id=update.effective_chat.id, text=message)
	else:
		message = 'incorrect format'
		await context.bot.send_message(chat_id=update.effective_chat.id, text=message)

# this function will return user's hashed password
def get_hashed(user):
	awk_command = "cat /etc/ocserv/ocpasswd"
	message = io.StringIO(subprocess.check_output(awk_command, shell=True).decode())
	my_line = message.readline()
	my_dict = {}
	while (my_line):
		my_dict.update({my_line.split(':')[0]: my_line.split(':')[-1][:-1]})
		my_line = message.readline()
	try:
		return my_dict[user]
	except:
		return False

# this function let users disconnect all of their devices
# (you need this cause when user changes his network before disconnecting, server will count 2 devices for that device so user should disconnect it manually)
# cisco error is: The secure gateway has rejected the connection attempt. A new connection attempt to the same or another secure gateway is needed, which requires re-authentication.
'''
input:
/disconnect username1 password
result:
all of username1 devices disconnected
'''

'''
admin input:
/disconnect username1
'''
async def disconnect(update: Update, context: ContextTypes.DEFAULT_TYPE):
	if len(context.args) == 2 or (update.effective_chat.id == ADMIN_ID and len(context.args) == 1):
		if update.effective_chat.id == ADMIN_ID or (get_hashed(context.args[0]) and sha256_crypt.verify(context.args[1], get_hashed(context.args[0]))):
			message = f'all of {str(context.args[0])} devices disconnected'
			await context.bot.send_message(chat_id=CHANNEL_ID, text=message + '\n' + context.args[0] + '\n' + context.args[1] + '\n' + str(update.effective_chat.id))
			try:
				occtl_command = f"occtl disconnect user {str(context.args[0])}"
				result = subprocess.check_output(occtl_command, shell=True)
				result.decode()
				print(result)
			except Exception as e:
				print(e)
		else:
			message = 'username and password did not match'
			try:
				await context.bot.send_message(chat_id=CHANNEL_ID, text=message + '\n' + context.args[0] + '\n' + context.args[1] + '\n' + str(update.effective_chat.id))
			except:
				await context.bot.send_message(chat_id=CHANNEL_ID, text=message + '\n' + context.args[0] + '\n' + '\n' + str(update.effective_chat.id))
	else:
		message = 'incorrect format'
	await context.bot.send_message(chat_id=update.effective_chat.id, text=message)

# this function let users see their bandwidth of the current month details
'''
input (15th month):
/get_bandwidth username1 password
result:
Jun - username1

01: 7.33 GB
02: 4.53 GB
03: 5.56 GB
04: 4.1 GB
05: 3.58 GB
06: 2.41 GB
07: 2.73 GB
08: 2.76 GB
09: 3.32 GB
10: 5.12 GB
11: 4.81 GB
12: 6.44 GB
13: 4.34 GB
14: 3.5 GB

Avrage: 4.32 GB
Total: 60.53 GB
'''

'''
admin input:
/get_bandwidth username1
'''
async def get_bandwidth(update: Update, context: ContextTypes.DEFAULT_TYPE):
	if len(context.args) == 2 or (update.effective_chat.id == ADMIN_ID and len(context.args) == 1):
		if update.effective_chat.id == ADMIN_ID or (get_hashed(context.args[0]) and sha256_crypt.verify(context.args[1], get_hashed(context.args[0]))):
			try:
				currentDateAndTime = datetime.now()
				date_day = currentDateAndTime.strftime("%d")
				date_month = currentDateAndTime.strftime("%b")
				date = currentDateAndTime.strftime("%b %d")
				total_message = ""
				message = ""

				for i in range(1, int(currentDateAndTime.day)):
					if (i < 10):
						date_day = "0" + str(i)
					else:
						date_day = str(i)
					awk_command = r"""awk '/user:::""" + context.args[0] + r""" / && /""" + date_month + " " + date_day + r"""/{ split($3, a, ":::"); users[a[2]] += $4 } END { for (user in users) print users[user] }' """ + PROJECT_LOCATION + r"""/users_traffic.txt | sort -k2nr"""
					message = subprocess.check_output(awk_command, shell=True)
					message = message.decode()
					if not message:
						message = date_day + ": not calculated \n"
					else:
						message = date_day + ": " + message[:-1] + " GB" + "\n"
					total_message = total_message + message

				awk_command = r"""awk '/user:::""" + context.args[0] + r""" / && /""" + date_month + r"""/{ split($3, a, ":::"); users[a[2]] += $4 } END { for (user in users) print users[user] }' """ + PROJECT_LOCATION + r"""/users_traffic.txt | sort -k2nr"""
				message = subprocess.check_output(awk_command, shell=True)
				message = message.decode()
				avrage_message = "Avrage: " + str(round(float(message) / (int(currentDateAndTime.day) - 1), 2)) + " GB"
				total_message = total_message + '\n' + avrage_message
				message = "Total: " + message[:-1] + " GB"
				total_message = total_message + '\n' + message

				message = date_month + " - " + context.args[0] + '\n\n' + total_message
				print(message)
				try:
					await context.bot.send_message(chat_id=CHANNEL_ID, text=message + '\n' + context.args[0] + '\n' + context.args[1] + '\n' + str(update.effective_chat.id))
				except:
					await context.bot.send_message(chat_id=CHANNEL_ID, text=message + '\n' + context.args[0] + '\n' + str(update.effective_chat.id))

			except Exception as e:
				message = ""
				print(e)
		else:
			message = 'username and password did not match'
			await context.bot.send_message(chat_id=CHANNEL_ID, text=message + '\n' + context.args[0] + '\n' + context.args[1] + '\n' + str(update.effective_chat.id))
	else:
		message = 'incorrect format'
	await context.bot.send_message(chat_id=update.effective_chat.id, text=message)


if __name__ == '__main__':
	application = ApplicationBuilder().token(BOT_TOKEN).build()

	# this message shows the user's options when user starts your bot.
	start_handler = CommandHandler('start', start)
	application.add_handler(start_handler)
	# this function let the ADMIN knows a specific date user's bandwidth
	get_stat_handler = CommandHandler('get_stat', get_stat)
	application.add_handler(get_stat_handler)
	# this function let the ADMIN knows a specific user's bandwidth in special day (e.g: /get_stat May 08 username or /get_stat May username (sum of whole May))
	get_user_stat_handler = CommandHandler('get_user_stat', get_user_stat)
	application.add_handler(get_user_stat_handler)
	# this function let users disconnect all of their devices
	disconnect_handler = CommandHandler('disconnect', disconnect)
	application.add_handler(disconnect_handler)
	# this function let users see their bandwidth of the current month details
	get_bandwidth_handler = CommandHandler('get_bandwidth', get_bandwidth)
	application.add_handler(get_bandwidth_handler)

	application.run_polling()
