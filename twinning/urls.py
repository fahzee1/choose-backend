"""twinning URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from users import urls as user_urls
from votes import urls as vote_urls
from django.views.generic import TemplateView

admin.site.site_header = 'Choose Admin'

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

    url(r'^api/', include(user_urls)),
    url(r'^api/', include(vote_urls)),

    url(r'^appLink$',TemplateView.as_view(template_name='facebook/index.html')),


]


if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += [url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT})]