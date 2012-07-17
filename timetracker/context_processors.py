from timetracker.models import *
import django_mobile

def common(request):
    from tracker import settings
    context = {}
    context['static_url'] = settings.STATIC_URL
    context['flavour'] = settings.FLAVOUR
    
    context['base_template'] = settings.BASE_TEMPLATE
    if django_mobile.get_flavour(request) == 'mobile':
        context['base_template'] = settings.BASE_TEMPLATE_MOBILE

        
    try:
        firsttime = request.session['firsttime']
        context['firsttime'] = firsttime
    except:
        pass
            
    
    return context