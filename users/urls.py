from django.conf.urls import include, url
import views

"""
Remember to run python manage.py clearsessions in a cron job for expired sessions
"""

urlpatterns = [
    url(r'^users/me/$', views.get_me,name="get_me"),
    url(r'^users/login/$', views.login,name="login"),
    url(r'^users/search/$', views.user_search,name="search"),

]
