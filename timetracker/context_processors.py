from timetracker.models import *


def common(request):
    from tracker import settings
    context = {}
    context['static_url'] = settings.STATIC_URL
    try:
        firsttime = request.session['firsttime']
        context['firsttime'] = firsttime
    except:
        pass
            
    
    return context