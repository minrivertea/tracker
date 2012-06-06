from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from registration.views import register


from django.contrib import admin
admin.autodiscover()

from timetracker.views import *

urlpatterns = patterns('',

    url(r'^$', home, name="home"),
    url(r'^job/(?P<hashkey>[\w-]+)/done$', mark_job_as_done, name="job_done"),
    url(r'^job/(?P<hashkey>[\w-]+)/paid$', mark_job_as_paid, name="job_paid"),
    url(r'^job/(?P<hashkey>[\w-]+)/$', job, name="job"),
    #url(r'^url/(?P<hashkey>[\w-]+)/$', views.url, name="url"),
    url(r'^add-job/$', addjob, name="addjob"),
    
    url(r'^accounts/register/$', register,
        {'backend': 'tracker.regbackend.RegBackend',},        
        name='registration_register'
    ),

    (r'^accounts/', include('registration.backends.default.urls')),


    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()
