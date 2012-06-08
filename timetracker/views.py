from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib import auth

import datetime
import calendar
import time
import uuid
from random import randint

from timetracker.forms import AddForm
from timetracker.models import JobsCalendar, Job, Currency

#render shortcut
def render(request, template, context_dict=None, **kwargs):
    return render_to_response(
        template, context_dict or {}, context_instance=RequestContext(request),
                              **kwargs
    )




def calendar(request, year, month):
  my_jobs = Job.objects.order_by('start_date_time').filter(
    my_date__year=year, my_date__month=month
  )
  cal = WorkoutCalendar(my_workouts).formatmonth(year, month)
  return render_to_response('my_template.html', {'calendar': mark_safe(cal),})


def login_as_anonymous(request):
    
    # still to do
    return


def home(request):
    
    if request.user.is_authenticated():
        
        try:
            year = int(request.GET['year'])
            month = int(request.GET['month'])
            print month
        except:
            year = datetime.datetime.now().year
            month = datetime.datetime.now().month
        
        
        next_month = int(month)+1
        prev_month = int(month)-1
            
        my_jobs = Job.objects.order_by('start_date_time').filter(
            start_date_time__year=year, start_date_time__month=month, owner=request.user
        )
        
        cal = JobsCalendar(my_jobs).formatmonth(year, month)
        
        total_money = 0
        paid = 0
        completed = 0
        total_jobs = len(my_jobs)
        for job in my_jobs:
            if job.completed and not job.paid:
                completed += job.get_total()
            elif job.paid:
                paid += job.get_total()
            
            total_money += job.get_total()
            
    else:
        return render(request, 'timetracker/anon_home.html', locals())


    return render(request, 'timetracker/home.html', locals())
    
    
def addjob(request):
    
    if request.method == 'POST':
        
        form = AddForm(request.POST)
        if form.is_valid():
        
            # turn the date provided by the form into a valid date format
            date = datetime.datetime.strptime(form.cleaned_data['start_date'], "%Y-%m-%d").date()

           
            name = 'Untitled'
            client = None
            length = None
            hours = 9
            minutes = None
            
            details = form.cleaned_data['details'].split()
            for x in details:
                if x.startswith('@'):
                    client = x.replace('@', '')
                else:
                    if x.startswith('#'):
                        name = x.replace('#', '').replace('-', ' ').capitalize()
                    else: 
                        if x[0].isdigit() and x.endswith(('h', 'hr', 'hrs')):
                            length = x.replace('h', '').replace('r', '').replace('s', '')
                        else:
                            if x.endswith(('am', 'pm')):
                                
                                # first lets convert it into 24 hour clock times (only if am or pm has been used)
                                if x.endswith('am'):
                                    number = x.replace('am', '')
                                    afternoon = False
                                elif x.endswith('pm'):
                                    number = x.replace('pm', '')
                                    afternoon = True
                                    
                                # we want to check first if it is a whole number, or a part number (eg. 9 or 9.15)
                                if '.' or ':' in number:
                                    new = str(number).replace(':', '.').split('.')

                                    hours = new[0]
                                    if afternoon:
                                        hours = int(new[0]) + 12
                                        
                                    try:
                                        minutes = new[1]
                                    except:
                                        pass 
                                    print minutes                                  
                                
                            else:
                                if x[0].isdigit() and x.endswith(('RMB', 'GBP', 'USD')):
                                    rate = ''
                                    curr_code = ''
                                    for d in x:
                                        if d.isdigit():
                                            rate += d
                                        else:
                                            curr_code += d
                                            

            if not minutes:
                time_string = "%s-%s" % (form.cleaned_data['start_date'], hours)
                time_format = "%Y-%m-%d-%H"
            else:
                time_string = "%s-%s-%s" % (form.cleaned_data['start_date'], hours, minutes)
                time_format = "%Y-%m-%d-%H-%M"
         
            print time_string
            print time_format
        
            date_time = datetime.datetime.fromtimestamp(time.mktime(time.strptime(time_string, time_format)))
           
            currency = get_object_or_404(Currency, code=curr_code)
            # then create a job object
            new_job = Job.objects.create(
                name = name,
                owner = request.user,
                start_date_time = date_time,
                length = length,
                rate = rate,
                currency = currency,
                client = client,
                hashkey = uuid.uuid1().hex,
            )
            
                        
            if request.is_ajax():
                
                url = reverse('home')
                return HttpResponseRedirect(url)
            
            else:
                url = reverse('home')
                return HttpResponseRedirect(url)
    

    form = AddForm()
    
    return render(request, 'timetracker/home.html', locals())
    
def job(request, hashkey):
    job = get_object_or_404(Job, hashkey=hashkey)
    
    if request.is_ajax():
        text = render_to_string('snippets/job_details.html', {'job': job})
        return HttpResponse(text)
    
    return render(request, 'timetracker/job.html', locals())


def anonymous_login(request):
    
    creation_args = {
        'username': ("%s%s" % ('anonymous', str(randint(100, 999)))),
        'email': 'nothing@nothing.com',
        'password': uuid.uuid1().hex,
    }
    
    this_user = User.objects.create(**creation_args)
    this_user.first_name = ''
    this_user.last_name = ''
    this_user.save()
    
    # we'll secretly log the user in now
    from django.contrib.auth import load_backend, login
    for backend in settings.AUTHENTICATION_BACKENDS:
        if this_user == load_backend(backend).get_user(this_user.pk):
            this_user.backend = backend
    if hasattr(this_user, 'backend'):
        login(request, this_user)
    
    request.session['firsttime'] = 1
    
    url = reverse('home')
    return HttpResponseRedirect(url)


def mark_job_as_done(request, hashkey):
    job = get_object_or_404(Job, hashkey=hashkey)
    job.completed = datetime.datetime.now()
    job.save()
    
    if request.is_ajax(): 
        return HttpResponse('true')
    
    return render(request, 'timetracker/job.html', locals())


def mark_job_as_paid(request, hashkey):
    job = get_object_or_404(Job, hashkey=hashkey)
    job.paid = datetime.datetime.now()
    job.save()
    
    if request.is_ajax():
        return HttpResponse('true')
    
    return render(request, 'timetracker/job.html', locals())
    
def delete_job(request, hashkey):
    job = get_object_or_404(Job, hashkey=hashkey)
    job.delete()
    
    if request.is_ajax(): 
        return HttpResponse('true')
    
    url = reverse('home')
    return HttpResponseRedirect(url)
    