from django.conf.urls import include, url
import views

urlpatterns = [
    url(r'^votes/(?P<pk>[0-9]+)$', views.votes, name="votes"),
    url(r'^votes/category/(?P<pk>[0-9]+)$', views.show_categories, name="category_object"),
    url(r'^votes/category/$', views.category, name="category"),
    url(r'^votes/featured/$', views.show_featured, name="featured"),
    url(r'^votes/create/$', views.create_vote, name="create_vote"),

]
