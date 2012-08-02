from django.db import models
from django.utils.html import conditional_escape as esc
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User


from itertools import groupby
import calendar
from datetime import date, datetime, timedelta


# Create your models here.

class Currency(models.Model):
    name = models.CharField(max_length=200)
    symbol = models.CharField(max_length=10)
    code = models.CharField(max_length=5)
    exchange_rate = models.IntegerField()
    
    def __unicode__(self):
        return self.name
    

class Job(models.Model):
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(User)
    hashkey = models.CharField(max_length=100)
    start_date_time = models.DateTimeField()
    length = models.DecimalField(max_digits=4, decimal_places=2)
    rate = models.IntegerField(blank=True, null=True) # I want to change this to a decimal field and allow for split numbers
    currency = models.ForeignKey('Currency', blank=True, null=True)
    client = models.CharField(max_length=200, blank=True, null=True)
    completed = models.DateTimeField(blank=True, null=True)
    paid = models.DateTimeField(blank=True, null=True)
    
    def __unicode__(self):
        hour = self.start_date_time.strftime('%H:%M')
        name = "%s %s" % (hour, self.name)
        return name
    
    def get_total(self):
        cost = self.rate * float(self.length)
        return cost
    
    def get_absolute_url(self):
        url = reverse('job', args=[self.hashkey])
        return url
        
    def get_end_time(self):
        duration = str(self.length).split('.')
        end_time = self.start_date_time + timedelta(hours=int(duration[0]), minutes=int(duration[1]))
        return end_time
        
        

class URL(models.Model):
    name = models.CharField(max_length=255)
    hashkey = models.CharField(max_length=200)
    related_owner = models.ForeignKey(User)
    can_write = models.BooleanField(default=False)
    can_see_names = models.BooleanField(default=True)
    can_see_details = models.BooleanField(default=True)
    needs_login = models.BooleanField(default=False)
    
    


class JobsCalendar(calendar.HTMLCalendar):

    def __init__(self, jobs):
        super(JobsCalendar, self).__init__()
        self.jobs = self.group_by_day(jobs)

    def formatday(self, day, weekday):
        if day != 0:
            cssclass = self.cssclasses[weekday]
            if date.today() == date(self.year, self.month, day):
                cssclass += ' today'
            if day in self.jobs:
                cssclass += ' filled'
                body = ['<ul class="jobslist" data-role="listview">']
                for job in self.jobs[day]:
                    link = render_to_string('snippets/job_link.html', {'job': job})
                    body.append(link)
                body.append('</ul>')
                return self.day_cell(cssclass, day, ''.join(body))
            return self.day_cell(cssclass, day)
        return self.day_cell('noday', '')

    def formatmonth(self, year, month):
        self.year, self.month = year, month
        return super(JobsCalendar, self).formatmonth(year, month)

    def group_by_day(self, jobs):
        field = lambda job: job.start_date_time.day
        return dict(
            [(day, list(items)) for day, items in groupby(jobs, field)]
        )

    def day_cell(self, cssclass, day, body=None):
        return render_to_string('snippets/day_cell.html', {'year': self.year, 'month': self.month, 'day': day, 'body': body, 'cssclass': cssclass,})
