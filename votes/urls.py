from django.conf.urls import include, url
import views

urlpatterns = [

    url(r'^cards$', views.cards, name="cards"),
    url(r'^cards/(?P<id>[0-9]+)$', views.cards_object, name="cards_object"),
    url(r'^cards/(?P<id>[0-9]+)/(?P<vote>[1-2]+)$', views.card_vote, name="card_vote"),
    url(r'^shareText$', views.share_text, name="share_text"),
]
