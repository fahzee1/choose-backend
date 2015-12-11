from django.conf.urls import include, url
import views

"""
Remember to run python manage.py clearsessions in a cron job for expired sessions
"""

urlpatterns = [
    url(r'^users/me$', views.get_me,name="get_me"),
    url(r'^users/login$', views.login,name="login"),

    url(r'^users$', views.users,name="users"),
    url(r'^users/(?P<facebook_id>[0-9]+)$', views.user_object,name="user_object"),
    url(r'^users/(?P<facebook_id>[0-9]+)/cards$', views.user_cards,name="user_cards"),
]
