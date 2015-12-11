from django.contrib import admin
from models import Tag, Card, ShareText, CardList
# Register your models here.


admin.site.register(Tag)
admin.site.register(Card)
admin.site.register(CardList)
admin.site.register(ShareText)