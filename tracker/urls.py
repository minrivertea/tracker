from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from registration.views import register


from django.contrib import admin
admin.autodiscover()

from timetracker.views import *

urlpatterns = patterns('',

    url(r'^$', home, name="home"),
    
    url(r'^url/make$', make_url, name="make_url"),
    url(r'^url/(?P<hashkey>[\w-]+)/$', view_url, name="view_url"),
    
    url(r'^job/(?P<hashkey>[\w-]+)/delete$', delete_job, name="delete_job"),
    url(r'^job/(?P<hashkey>[\w-]+)/done$', mark_job_as_done, name="job_done"),
    url(r'^job/(?P<hashkey>[\w-]+)/paid$', mark_job_as_paid, name="job_paid"),
    url(r'^job/(?P<hashkey>[\w-]+)/$', job, name="job"),
    #url(r'^url/(?P<hashkey>[\w-]+)/$', views.url, name="url"),
    url(r'^add-job/$', addjob, name="addjob"),
    url(r'^anonymous-login/$', anonymous_login, name="anonymous_login"),
    
    url(r'^accounts/register/$', register,
        {'backend': 'tracker.regbackend.RegBackend',},        
        name='registration_register'
    ),

    (r'^accounts/', include('registration.backends.default.urls')),


    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()
