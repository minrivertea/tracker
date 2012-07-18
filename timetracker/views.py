from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib import auth
from django.utils import simplejson
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers
import django_mobile

import datetime
import calendar
import time
import uuid
from random import randint

from timetracker.forms import AddForm, MakeURLForm
from timetracker.models import JobsCalendar, Job, Currency, URL

#render shortcut
def render(request, template, context_dict=None, **kwargs):
    
    if is_mobile_ajax(request):
        template = template.replace('.html', '_fragment.html')
    
    return render_to_response(
        template, context_dict or {}, context_instance=RequestContext(request),
                              **kwargs
    )


def is_mobile_ajax(request):
    result = False   
    if request.is_ajax() and django_mobile.get_flavour(request) == 'mobile':
        result = True        
    
    return result


def home(request):
    
    if request.user.is_authenticated():
        
        try:
            year = int(request.GET['year'])
            month = int(request.GET['month'])
        except:
            year = datetime.datetime.now().year
            month = datetime.datetime.now().month
        
        
        date = datetime.datetime(year, month, day=1)
        
        next_month = int(month)+1
        prev_month = int(month)-1
        next_year = year
        prev_year = year
        
        if next_month == 13:
            next_month = 1
            next_year = int(year)+1
        
        if prev_month == 0:
            prev_month = 12
            prev_year = int(year)-1
            
        my_jobs = Job.objects.order_by('start_date_time').filter(
            start_date_time__year=year, start_date_time__month=month, owner=request.user
        )
        
        cal = JobsCalendar(my_jobs).formatmonth(year, month)
        
        total_money = 0
        paid = 0
        completed = 0

        seen = {}
        clients = []
        
        total_jobs = len(my_jobs)
        for job in my_jobs:
            if job.completed and not job.paid:
                completed += job.get_total()
            elif job.paid:
                paid += job.get_total()
            
            total_money += job.get_total()
            
            
            
            
            marker = job.client
            if marker in seen: 
                for x in clients:
                    if x['name'] == marker:
                        x['money'] = x['money']+job.get_total()
                continue
            seen[marker] = 1
            clients.append(dict(name=marker, money=job.get_total()))
            
            
        av = total_money / 30
                   
    else:
        return render(request, 'timetracker/anon_home.html', locals())

    form = MakeURLForm()
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
            curr_code = None
            rate = 0
            
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
        
        
            date_time = datetime.datetime.fromtimestamp(time.mktime(time.strptime(time_string, time_format)))
           
            if curr_code:
                currency = get_object_or_404(Currency, code=curr_code)
            else:
                currency = None
                
            # then create a job object
            creation_args = {
                'name': name,
                'owner': request.user,
                'start_date_time': date_time,
                'length': length,
                'rate': rate,
                'currency': currency,
                'client': client,
                'hashkey': uuid.uuid1().hex,
            }
            
            new_job = Job.objects.create(**creation_args)
                                    
            if is_mobile_ajax(request):
                url = reverse('home')
                return HttpResponseRedirect(url)
            
            
            if request.is_ajax():
                html = render_to_string('snippets/job_link.html', {'job': new_job})
                json =  simplejson.dumps((dict(html=html, date=form.cleaned_data['start_date'])), cls=DjangoJSONEncoder)
                return HttpResponse(json)
            
            else:
                url = reverse('home')
                return HttpResponseRedirect(url)
    
    else:
        url = reverse('home')
        return HttpResponseRedirect(url)
        
    form = AddForm()
    
    return render(request, 'timetracker/home.html', locals())
    
def job(request, hashkey):
    job = get_object_or_404(Job, hashkey=hashkey)
    
    if is_mobile_ajax(request):
        return render(request, 'timetracker/job.html', locals())
    
    if request.is_ajax():
        text = render_to_string('snippets/job_details.html', {'job': job})
        return HttpResponse(text)
    
    return render(request, 'timetracker/job.html', locals())


def anonymous_login(request):
    
    new_username = "%s%s" % ('anonymous', str(randint(100, 999)))
    if len(User.objects.filter(username=new_username)):
        new_username = "%s%s" % ('anonymous', str(randint(100, 999)))
    
    creation_args = {
        'username': new_username,
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
    if job.completed:
        job.completed = None
        job.save()
        response = 'false'
    else:
        job.completed = datetime.datetime.now()
        job.save()
        response = 'true'
    
    if request.is_ajax(): 
        return HttpResponse(response)
    
    return render(request, 'timetracker/job.html', locals())


def mark_job_as_paid(request, hashkey):
    job = get_object_or_404(Job, hashkey=hashkey)
    if job.paid:
        job.paid = None
        job.save()
        response = 'false'
    else:
        job.paid = datetime.datetime.now()
        job.save()
        response = 'true'
    
    if request.is_ajax():
        return HttpResponse(response)
    
    return render(request, 'timetracker/job.html', locals())
    
def delete_job(request, hashkey):
    job = get_object_or_404(Job, hashkey=hashkey)
    job.delete()
    
    if request.is_ajax(): 
        return HttpResponse(job.hashkey)
    
    url = reverse('home')
    return HttpResponseRedirect(url)


def make_url(request):
    owner = request.user
    if request.method == "POST":
        form = MakeURLForm(request.POST)
        if form.is_valid():
            
            new_url = URL.objects.create(
                related_owner = owner, 
                hashkey = uuid.uuid1().hex,
                can_write = form.cleaned_data['can_write'],
                can_see_names = form.cleaned_data['can_see_names'],
                can_see_details = form.cleaned_data['can_see_details'],
            )
            
            new_url.save()
            
            if request.is_ajax():
                url = reverse('view_url', args=[new_url.hashkey])
                return HttpResponse(url)
            else:        
                return render(request, 'timetracker/url.html', locals())
        
    else:
        form = MakeURLForm()
            
    return render(request, 'timetracker/url.html', locals())

def view_url(request, hashkey):
    link = get_object_or_404(URL, hashkey=hashkey)    
    return render(request, 'timetracker/url.html', locals())
    
    
# API CALLS FOR MOBILE
    
def get_clients(request):
    user = request.user
    jobs = Job.objects.filter(owner=user)

    seen = {}
    result = []
    for item in jobs:
        marker = item.client
        if marker in seen: continue
        seen[marker] = 1
        result.append(item.client)

    return result    