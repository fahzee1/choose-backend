from django.conf.urls import include, url
import views

urlpatterns = [
    url(r'^votes/category/(?P<pk>[0-9]+)$', views.show_categories, name="category"),
    url(r'^votes/featured/$', views.show_featured, name="featured"),
    url(r'^votes/create/$', views.create_vote, name="create_vote"),

]
