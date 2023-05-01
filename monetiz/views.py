from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from .mail import send_email
from .jobs import *
from .financials import *

from .forms import RegisterForm

@login_required
def panel(request):
    #send_email('Test', 'Test', 'asphalt8fr@gmail.com')
    context = {
        "current_jobs"  : list_current_jobs(request.user),
        "completed_jobs" : list_done_jobs(request.user),
        "recent_payouts"  : list_payouts(request.user),
        "earnings" : get_balance(request.user),
    }
    return render(request, 'panel.html', context=context)

@login_required
def getajob(request):
    number_of_job_taken = jstarted.objects.filter(user=request.user).count()
    number_of_jobs_not_done = jstarted.objects.filter(user=request.user, done=False).count()
    if number_of_job_taken - number_of_jobs_not_done >= 5:
        return message(request, "You have already 5 jobs uncompleted", "/panel", "Panel")
    else:
        if  get_job(request.user):
            return message(request, "Job taken successfully", "/panel", "Panel")
        else :
            return message(request, "No jobs available anymore", "/panel", "Panel")

@login_required
def message(request, message, link , name):
    context = { "message" : message, "link" : link, "name" : name }
    return render(request, 'message.html', context=context)

@login_required
def validate(request,id):
    #Check if the job is done by the user
    if jstarted.objects.filter(user=request.user, id=id).get().done == True:
        return message(request, "You have already completed this job", "/panel", "Panel")
    else:
        return render(request, 'validate.html',context={"id":id})
    
@login_required
def isvalid(request):
    trY = request.GET.get('token')
    id = request.GET.get('id')
    key = Job.objects.filter(id=id).get().key
    if key.lower() == trY.lower():
        update_balance(request.user, Job.objects.filter(id=id).get().amount)
        set_job_done(request.user, id)
        return message(request, "Job validated successfully", "/panel", "Panel")
    else:
        return message(request, "Job validation failed", "/panel", "Panel") 
    
@permission_required('is_staff')
def legitcheck(request,username):
    user = User.objects.filter(username=username).get()
    if legit_check(user):
        return message(request, "User is legit", "/admin", "Admin")
    else:
        return message(request, "User is not legit", "/admin", "Admin")