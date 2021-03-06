from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from registration.views import register


from django.contrib import admin
admin.autodiscover()

from timetracker.views import *

urlpatterns = patterns('',

    url(r'^$', home, name="home"),
    #url(r'^api/next-month/(?P<current>[\w-]+)/$', next_month, name="next_month"),
    
    
    
    url(r'^url/make/$', make_url, name="make_url"),
    url(r'^url/(?P<hashkey>[\w-]+)/$', view_url, name="view_url"),
    url(r'^usersettings/$', usersettings, name="usersettings"),
    url(r'^tour/one/$', direct_to_template, {'template': 'timetracker/tour_1.html',}),
    url(r'^tour/two/$', direct_to_template, {'template': 'timetracker/tour_2.html',}),

    url(r'^ical/(?P<owner_id>\d+)/jobs.ics$', ical, name="jobs_ical"),
    
    url(r'^job/(?P<hashkey>[\w-]+)/delete$', delete_job, name="delete_job"),
    url(r'^job/(?P<hashkey>[\w-]+)/done$', mark_job_as_done, name="job_done"),
    url(r'^job/(?P<hashkey>[\w-]+)/paid$', mark_job_as_paid, name="job_paid"),
    url(r'^job/(?P<hashkey>[\w-]+)/$', job, name="job"),
    url(r'^add-job/$', addjob, name="addjob"),
    url(r'^anonymous-login/$', anonymous_login, name="anonymous_login"),
    
    url(r'^accounts/register/$', register,
        {'backend': 'tracker.regbackend.CustomBackend',},        
        name='registration_register'
    ),
    
    
    # api-like urls
    url(r'^load-stats/$', load_stats, name="load_stats"),
    url(r'^load-jobs/$', load_jobs, name="load_jobs"),
    url(r'^update-job/$', update_job, name="update_job"),
    

    (r'^accounts/', include('registration.backends.default.urls')),


    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()
