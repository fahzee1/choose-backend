from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
import views

admin.site.site_header = 'Team Destiny Inc Admin'

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.home,name='home'),

]


if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += [url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT})]