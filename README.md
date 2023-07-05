# About

This program is a telegram bot to monitor openconnect VPN server (ocserv) user's network usage and other functions

this bot now has 5 function

1- /start

    this function will help users to use your bot

    input:
    /start

    result:
    you must write this command to see your network usage:
    /disconnect username password
    you must write this command to disconnect all of your devices:
    /get_bandwidth username password

2- /disconnect

    this function let users disconnect all of their devices
    (you need this cause when user changes his network before disconnecting, server will count 2 devices for that device so user should disconnect it manually)
    cisco error is: The secure gateway has rejected the connection attempt. A new connection attempt to the same or another secure gateway is needed, which requires re-authentication.

    input:
    /disconnect username1 password
    result:
    all of username1 devices disconnected
    
    admin input:
    /disconnect username1

3- /get_bandwidth 

    this function let users see their bandwidth of the current month details
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
    14: 3.5` GB
    
    Avrage: 4.32 GB
    Total: 60.53 GB
    
    admin input:
    /get_bandwidth username1

4 - /get_stat

    only admin can use this function
    this function let the ADMIN knows a specific date bandwidth GB (e.g: /get_stat May 08 or /get_stat May (sum of whole May))
    this will get you 6 users that used the most traffic in that date

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

5- /get_user_stat

    only admin can use this function
    this function let the ADMIN knows a specific user's bandwidth GB in special day (e.g: /get_stat May 08 username or /get_stat May username (sum of whole May))
    
    input:
    /get_user_stat Jun username1
    result:
    Jun
    username1 20.4

note: all inputs and results will send to you telegram channel with sender's telegram id

# Getting started
you must add this line to end of /etc/ocserv/ocserv.conf
```
log-level=4
```
then restart your ocserv
```
$ sudo systemctl restart ocserv
```
then connect to your VPN, download some data and disconnect from your VPN

then you must find ocserv log location (it may be in /var/log/messages)

you can check it with:
```
grep 'ocserv' /var/log/messages
```
if your log location was not in /var/log/messages, you should find your log location

if you found location, you should get some logs in this format:
```
Jun 25 21:32:42 sct ocserv[836]: main[your_username]:***.***.***.***:***** user disconnected (reason: unspecified error, rx: 159868, tx: 111153)
```
you can check it with this code: (change location if your log location address is not /var/log/messages)
```
grep 'disconnected' /var/log/messages
```
if you found it, continue

you should write your log location in LOG_FILE_LOCATION field in users_traffic_cron.py file (LOG_FILE_LOCATION field)

default is '/var/log/messages'

then you should override project location field in cron.py, users_traffic_cron.py, users_traffic_cron_manual.py and telegram_bot.py files (PROJECT_LOCATION field)

default is '/root/occtl_telegram_bot'
___

then you must create a telegram bot with @BotFather bot in telegram
and replace your bot token in telegram_bot.py file (BOT_TOKEN field)

then you must get your telegram id (you can use @getidsbot)
and replace your telegram id in telegram_bot.py file (ADMIN_ID field)

then you must create a channel in telegram and add your bot to the channel as administrator
then get your channel id (you can open your channel in telegram web, the number after # in url is your channel id)
replace your channel id in telegram_bot.py file (CHANNEL_ID field)

***code is ready***

___

now you must run the code with python 3.7 or later
install these pakages
```
$ pip install passlib
$ pip install python-crontab
$ pip install pyTelegramBotAPI
$ pip install python-telegram-bot
```
now run cron file
this cron will run users_traffic_cron.py every day at 23:55 to get all data from log file (/var/log/messages) and save it to users_traffic.txt file
```
$ python {your_project_location}/cron.py
```

run your telegram bot in background
```
$ nohup python {your_project_location}/telegram_bot.py &
```
***now all things must work well*** 
___
you can disable cron job by run the cron_disabler.py
```
$ python {your_project_location}/cron_disabler.py
```
if your cron did not run in a day for any reason, you should run users_traffic_cron_manual.py to update users_traffic.txt

but first you must edit DATE field in the file:
```
$ vim {your_project_location}/users_traffic_cron_manual.py
```
change DATE field
```
$ python {your_project_location}/users_traffic_cron_manual.py
```
