from crontab import CronTab

# create a new cron job
cron = CronTab(user='root')


job = cron.find_comment('write users traffics daily')
cron.remove_all(comment='write users traffics daily')
# remove the cron job
cron.write()
