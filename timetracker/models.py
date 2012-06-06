from django.db import models
from django.utils.html import conditional_escape as esc
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User


from itertools import groupby
import calendar
from datetime import date, datetime



LONGRE = 'longre'
EFLY = 'efly'
CLIENT_CHOICES = (
    (LONGRE, u'Longre'),
    (EFLY, u'eFly'),
)


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
    rate = models.IntegerField()
    currency = models.ForeignKey('Currency')
    client = models.CharField(max_length=200)
    completed = models.DateTimeField(blank=True, null=True)
    paid = models.DateTimeField(blank=True, null=True)
    
    def __unicode__(self):
        hour = self.start_date_time.strftime('%H:%M')
        date_time = "%s %s" % (hour, self.name)
        return date_time
    
    def get_total(self):
        cost = self.rate * float(self.length)
        return cost
    
    def get_absolute_url(self):
        url = reverse('job', args=[self.hashkey])
        return url




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
                body = ['<ul>']
                for job in self.jobs[day]:
                    body.append('<li>')
                    body.append('<span class="link" href="%s">' % job.get_absolute_url())
                    body.append(esc(job))
                    body.append('</span></li>')
                body.append('</ul>')
                return self.day_cell(cssclass, day, ''.join(body))
            return self.day_cell(cssclass, day)
        return self.day_cell('noday', '&nbsp;')

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
