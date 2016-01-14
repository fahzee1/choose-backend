import pdb
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings


def home(request):
    current_site = get_current_site(request)
    if current_site.domain == 'api.trychoose.com':
        return HttpResponse()

    elif current_site.domain == 'emekaenterprises.com':
        return render(request,'emeka/index.html',{'foo':'bar'})

    else:
        return HttpResponseBadRequest()

