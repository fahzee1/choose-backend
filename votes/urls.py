from django.conf.urls import include, url
import views

urlpatterns = [
    url(r'^cards/all/$', views.show_cards, name="cards"),
    url(r'^cards/featured/$', views.show_featured, name="featured"),
    url(r'^cards/create/$', views.create_card, name="create_card"),
    url(r'^cards/update/$', views.update_card, name="update_card"),
    url(r'^cards/delete/$', views.delete_card, name="delete_card"),

]
