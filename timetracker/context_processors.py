from timetracker.models import *
from timetracker.views import get_clients
import django_mobile
import datetime


def common(request):
    from tracker import settings
    context = {}
    context['static_url'] = settings.STATIC_URL
    context['flavour'] = django_mobile.get_flavour(request)
    context['site_url'] = settings.SITE_URL
    
    if request.user.is_authenticated():
        context['base_template'] = settings.BASE_TEMPLATE
    else:
        context['base_template'] = settings.BASE_TEMPLATE_ANON
    if django_mobile.get_flavour(request) == 'mobile':
        context['base_template'] = settings.BASE_TEMPLATE_MOBILE

    
    
    if request.user.is_authenticated():
        context['clientnames'] = get_clients(request)
    
    context['today'] = datetime.datetime.now()
    context['ga_is_on'] = settings.GA_IS_ON
        
    try:
        firsttime = request.session['firsttime']
        context['firsttime'] = firsttime
    except:
        pass
            
    
    return context