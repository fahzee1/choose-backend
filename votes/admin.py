from django.contrib import admin
from models import Tag, Card, ShareText, CardList,Choose
import random
# Register your models here.


class CardAdmin(admin.ModelAdmin):
    list_display = ('question','string_question_type','image_link','id','user')
    list_display_links = ('question',)
    list_filter = ('question','user__username')
    search_fields = ('question','user__username')
    ordering = ('created',)
    filter_horizontal = ('tags',)
    fields = ('user',
              'image_url',
              'question',
              'question_type',
              ('left_votes_count','right_votes_count'),
              ('left_votes_fake','right_votes_fake'),
              'branch_link',
              'featured',
              'tags')
    readonly_fields = ('image_link','image_url','branch_link')
    actions = ['set_random_user','set_random_votes']

    def save_model(self,request,obj,form,change):
        if not obj.image_url:
            if obj.image:
                obj.image_url = obj.image.url
        obj.save()

    def delete_model(request,obj):
        obj.image.delete()

    def image_link(self,obj):
      if obj.image_url:
        return u'<a href="%s">%s</a>' % (obj.image_url,obj.image_url)
    image_link.allow_tags = True

    def string_question_type(self,obj):
      if obj.question_type == 101:
        return 'YES/NO'
      elif obj.question_type == 100:
        return 'A/B'
      else:
        return 'Impropery configured'

    def set_random_user(self,request,queryset):
        for i in queryset:
            random_user = self.get_my_random_object(i.user.__class__)
            i.user = random_user
            i.save()
        self.message_user(request,'Succesfully changed %s cards with new names' % queryset.count())

    set_random_user.short_description = 'Add random user to selected cards'

    def get_my_random_object(self,model):
        theObject = random.choice(model.objects.all())
        return theObject

    def set_random_votes(self,request,queryset):
        for i in queryset:
            i.fake_votes()
        self.message_user(request,'Succesfully changed %s cards with random votes' % queryset.count())

    set_random_votes.short_description = 'Add fake votes to selected cards'





class CardListAdmin(admin.ModelAdmin):
    list_display = ('name','approved','active','last_display','total_cards','uuid')
    list_editable = ('active','approved')
    list_filter = ('name',)
    search_fields = ('name',)
    filter_horizontal = ('cards',)
    readonly_fields = ('last_display','uuid')
    actions = ['new_uuid_action']

    def total_cards(self,obj):
      return '%s cards' % obj.cards.all().count()

    def new_uuid_action(self,request,queryset):
      for i in queryset:
        i.new_uuid(save=True)

      self.message_user(request,'Succesfully changed %s uuids' % queryset.count())
    new_uuid_action.short_description = 'Create new uuid for selected card lists'


    #raw_id_fields = ('cards',)

admin.site.register(Tag)
admin.site.register(Card,CardAdmin)
admin.site.register(CardList,CardListAdmin)
admin.site.register(ShareText)
admin.site.register(Choose)
admin.site.empty_value_display = 'Nothing here'