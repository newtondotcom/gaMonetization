from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from .mail import send_email
from .jobs import *
from .financials import *
from .linkvertise import linkvertise
from .forms import RegistrationForm

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/panel')
        else:
            #Not valid
            None
    else:
        form = RegistrationForm()

    return render(request, 'registration/register.html', {'form': form})

def offline(request):
    return message(request,"Merci de vous connectez à Internet","/offline",'this page')

def index(request):
    return render(request,'index.html')
    
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
        job = get_job(request.user)
        if  job!= None:
            return message(request, 'Job taken successfully ; here is the link to achieve it : <br> <a href="' + job.link + '">'+ job.link + '</a>', "/panel", "Panel")
        else :
            return message(request, "No jobs available anymore", "/panel", "Panel")

@login_required
def message(request, message, link , name):
    context = { "message" : message, "link" : link, "name" : name }
    return render(request, 'message.html', context=context)

@login_required
def validate(request,id,key):
    job = Job.objects.filter(id=id).get()
    #Check if the job is done by the user
    if jstarted.objects.filter(user=request.user, job=job).get().done == True:
        return message(request, "You have already completed this job", "/panel", "Panel")
    else:
        if key.lower() == job.key.lower():
            amount = job.amount
            update_balance(request.user, amount)
            set_job_done(request.user, id)
            return message(request, "Job validated successfully", "/panel", "Panel")
        else:
            return message(request, "Wrong key", "/panel", "Panel")
        
@permission_required('is_staff')
def legitcheck(request,username):
    user = User.objects.filter(username=username).get()
    if legit_check(user):
        return message(request, "User is legit", "/admin", "Admin")
    else:
        return message(request, "User is not legit", "/admin", "Admin")