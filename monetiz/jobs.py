from jobs.models import Job
from django.contrib.auth.models import User
from jstarted.models import jstarted
from payout.models import payout
from django.utils import timezone
from django.db.models import Avg, Count, Min, Sum
from .financials import *

##Create a job 
def create_job(link, amount, key):
    req = Job(link=link, amount=amount, key=key)
    req.save()
    
#Set a job as started for a user
def set_job(user, job):
    req = jstarted.objects.create(user=user, job=job)
    req.save()
    
#Get a random job for a user
def get_job(user):
    #Search for a rendom job, not already taken by the user
    if Job.objects.exclude(jstarted__user=user).count() > 0:
        req = Job.objects.exclude(jstarted__user=user).order_by('?').first()
        set_job(user, req)
        return True
    else:
        return False
    
#Set a job as done for a user
def set_job_done(user, id):
    req = jstarted.objects.filter(user=user, job__id=id).get()
    req.done = True
    req.finished_at = timezone.now()
    req.save()
    
#List all current jobs for a user 
def list_current_jobs(user,limit=5):
    req = jstarted.objects.all().filter(user=user, done=False)[:limit]
    arr = []
    for i in req:
        temp = {}
        temp['surname']= i.job.surname
        temp['taken_at'] = i.taken_at
        temp['link'] = i.job.link
        temp['amount'] = i.job.amount
        temp['id']= i.id
        arr.append(temp)
    return arr

#List all done jobs for a user 
def list_done_jobs(user,limit=5):
    req = jstarted.objects.all().filter(user=user, done=True)[:limit]
    arr = []
    for i in req:
        temp = {}
        temp['surname']= i.job.surname
        temp['finished_at'] = i.finished_at
        temp['link'] = i.job.link
        temp['amount'] = i.job.amount
        arr.append(temp)
    return arr

#Legit check a user
def legit_check(user):
    money_won = jstarted.objects.all().filter(user=user, done=True).aggregate(Sum('job__amount'))['job__amount__sum']
    money_posted = int(payout.objects.all().filter(user=user, status="paid").aggregate(Sum('amount'))['amount__sum']) + get_balance(user)
    if money_won == money_posted:
        return True
    else :
        return False