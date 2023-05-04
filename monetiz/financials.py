from jobs.models import Job
from django.contrib.auth.models import User
from jstarted.models import jstarted
from payout.models import payout
from datas.models import datas
from django.utils import timezone

#List all payouts for a user
def list_payouts(user,limit=5):
    req = payout.objects.all().filter(user=user)[:limit]
    arr = []
    for i in req:
        temp = {}
        temp['date'] = i.created_at
        temp['amount'] = i.amount
        if i.status == 'pending':
            temp['status'] = 'Pending'
            temp['paid_at'] = "N/A"
        else:
            temp['status'] = i.status
            temp['paid_at'] = i.paid_at
        arr.append(temp)
    return arr

#Get the balance of a user
def get_balance(user):
    if datas.objects.filter(user=user).count() == 0:
        req = datas.objects.create(user=user, balance=0)
        req.save()
        return 0
    else:
        req = datas.objects.filter(user=user).get()
        return req.balance

#Update the balance of a user
def update_balance(user,amount):
    req = datas.objects.filter(user=user)[0]
    req.balance = req.balance + amount
    req.save()

#Update the status of a payout
def set_payout_paid(user, amount):
    req = payout.objects.filter(user=user, amount=amount).get()
    req.status = "paid"
    req.paid_at = timezone.now()
    req.save()

#Get a payout status
def get_payout_status(user, amount):
    req = payout.objects.filter(user=user, amount=amount).get()
    return req.status

#Create a payout
def create_payout(user, amount):
    req = payout.objects.create(user=user, amount=amount, status="pending")
    req.save()
