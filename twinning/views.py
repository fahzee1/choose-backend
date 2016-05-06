import pdb
import logging
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt


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
    elif current_site.domain == 'genysolutions.co':
        logger.debug('on site genysolutions')
        return render(request,'genysolutions/index.html',{'foo':'bar'})
    else:
        logger.debug('no site its a bad request')
        return HttpResponseBadRequest()



def career(request):
    current_site = get_current_site(request)
    if current_site.domain == 'emekaenterprises.com':
        return render(request,'emeka/career.html',{'foo':'bar'})

def submit(request):
    if request.is_ajax():
        subscribe = request.POST.get('subscribe',0)
        email = request.POST.get('email','No email')

        if not subscribe:
            name = request.POST.get('name', 'No name')
            message = request.POST.get('message','No message')

            subject = 'New Email for Gen Y!'
            message = 'Name:%s\nEmail:%s\nMessage:%s\n' % (name,email,message)
        else:
            subject = 'New subscriber for Gen Y!'
            message = 'Add %s to subscriber list' % email

        send_mail(subject,message,settings.SERVER_EMAIL,['fahzee1@gmail.com'],fail_silently=False)
        return HttpResponse('success')
    else:
        return HttpResponseBadRequest('No good')
