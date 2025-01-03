# pip install apscheduler
""" apscheduler use example
def task_X():
    print("Do this")
    
scheduler = BlockingScheduler()

# Schedule tasks
scheduler.add_job(task_x, 'cron', hour=14, minute=0)  # 2 PM
scheduler.add_job(task_x, 'cron', hour=18, minute=0)  # 6 PM
scheduler.add_job(task_x, 'cron', hour=20, minute=0)  # 8 PM
scheduler.add_job(task_x, 'cron', hour=1, minute=0)   # 1 AM

scheduler.start()
"""
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime

# Day task for morning hours: 0700-1900
def task_day():
    print("Day task begin")
    
    print("Day task end")
    
# Night task for evening: 1900 - 0700
def task_night():
    print("Night task begin")
    
    print("Night task end")

def main():
    scheduler = BlockingScheduler()
    #scheduler.add_job(task_day, 'cron', hour=7, minute=0) # 7 AM
    
    # Do task at every hour from 0700 to 1900
    # for i in range(7, 20):
    #     scheduler.add_job(task_day, 'cron', hour=i, minute=0)
    
    # Do task every 2 hours from 0700 to 1900
    for i in range(7, 20, 2):
        scheduler.add_job(task_day, 'cron', hour=i, minute=0)
        
    scheduler.start()
    
    
if __name__ == "__main__":
    main()