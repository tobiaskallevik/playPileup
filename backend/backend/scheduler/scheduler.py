from django_apscheduler.models import DjangoJobExecution
import sys
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.schedulers.background import BackgroundScheduler
from django.utils import timezone
from apscheduler.jobstores.memory import MemoryJobStore
from django.contrib.auth import get_user_model

User = get_user_model()
   
# Deletes user that haven't verified their email in 1 day
# This is done to prevent spam users from filling up the database
def delete_unauthenticated_users():
    users = User.objects.filter(email_verified=False)
    for user in users:
        if timezone.now() - user.date_joined > timezone.timedelta(days=1):
            user.delete()
            print(f"Deleted user {user.username}")
        else:
            print(f"User {user.username} is not yet 1 day old")


def start():
    executors = {
        'default': ThreadPoolExecutor(20),
        'processpool': ProcessPoolExecutor(5)
    }
    job_defaults = {
        'coalesce': False,
        'max_instances': 1
    }
    
    scheduler = BackgroundScheduler(executors=executors, job_defaults=job_defaults)
    scheduler.add_jobstore(MemoryJobStore(), "default")
    scheduler.add_job(delete_unauthenticated_users, 'interval', hours=12, name='delete_unauthenticated_users', jobstore='default')
    scheduler.start()
    print("Scheduler started...", file=sys.stdout)