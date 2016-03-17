import pdb
import logging
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings

logger = logging.getLogger(__name__)

def home(request):
    current_site = get_current_site(request)
    logger.debug(current_site)

    if current_site.domain == 'api.trychoose.com':
        logger.debug('on site choose')
        return HttpResponse()

    elif current_site.domain == 'emekaenterprises.com':
        logger.debug('on site emekaenterprises')
        return render(request,'emeka/index.html',{'foo':'bar'})

    elif current_site.domain == 'teamdestinyfoundation.com':
        logger.debug('on site teamdestinyfoundation')
        return render(request,'destiny/index.html',{'foo':'bar'})
    else:
        logger.debug('no site its a bad request')
        return HttpResponseBadRequest()



def career(request):
    current_site = get_current_site(request)
    if current_site.domain == 'emekaenterprises.com':
        return render(request,'emeka/career.html',{'foo':'bar'})
