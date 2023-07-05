from crontab import CronTab

PROJECT_LOCATION = '/root/occtl_telegram_bot'

# Create a new cron job
cron = CronTab(user='root')
job = cron.new(command=f'python3 {PROJECT_LOCATION}/users_traffic_cron.py users_traffic_cron_function', comment='write users traffics daily')

# Set the job to run every day at 23:55
job.setall('55 23 * * *')

# Save the cron job
cron.write()


