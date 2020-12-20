import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
def job2(text):
    print('job2', datetime.datetime.now(), text)
scheduler = BlockingScheduler()
scheduler.add_job(job2, 'interval', seconds=2, args=['text'], id='job2')
scheduler.start()