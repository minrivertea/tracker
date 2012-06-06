from timetracker.models import *


def common(request):
    from tracker import settings
    context = {}
    context['static_url'] = settings.STATIC_URL
    
    
    return context