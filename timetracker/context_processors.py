from timetracker.models import *
from timetracker.views import get_clients
import django_mobile
import datetime


def common(request):
    from tracker import settings
    context = {}
    context['static_url'] = settings.STATIC_URL
    context['flavour'] = django_mobile.get_flavour(request)
    
    context['base_template'] = settings.BASE_TEMPLATE
    if django_mobile.get_flavour(request) == 'mobile':
        context['base_template'] = settings.BASE_TEMPLATE_MOBILE

    
    
    if request.user.is_authenticated():
        context['clientnames'] = get_clients(request)
    
    context['today'] = datetime.datetime.now()
    print datetime.datetime.now()
        
    try:
        firsttime = request.session['firsttime']
        context['firsttime'] = firsttime
    except:
        pass
            
    
    return context