from django.contrib import admin
from models import Tag, Card, ShareText, CardList,Choose
import random
# Register your models here.


class CardListInline(admin.TabularInline):
    model = CardList.cards.through
    extra = 1


class CardAdmin(admin.ModelAdmin):
    list_display = ('question','string_question_type','image_link','id','user')
    list_display_links = ('question',)
    list_filter = ('tags','created_by','user__username')
    search_fields = ('question','user__username')
    ordering = ('created',)
    filter_horizontal = ('tags',)
    fields = (('user','created_by'),
              'image_link',
              'question',
              'question_type',
              ('left_votes_count','right_votes_count'),
              ('left_votes_fake','right_votes_fake'),
              'branch_link',
              'featured',
              'tags',
              ('fake_active','fake_notification_count'))
    readonly_fields = ('image_link','image_url','branch_link')
    actions = ['set_random_user','set_random_votes','add_to_featured','add_to_daily','add_to_community']
    inlines = [CardListInline]

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

    def add_to_featured(self,request,queryset):
        featured = CardList.objects.filter(name='Featured')
        if not featured:
            self.message_user(request,'No list named Featured')
            return

        featured = featured[0]
        for i in queryset:
            if featured not in i.lists.all():
                i.lists.add(featured)
                i.save()

        self.message_user(request,'Done adding %s card to Featured'% queryset.count())

    add_to_featured.short_description = 'Add selected cards to Featured'

    def add_to_daily(self,request,queryset):
        daily = CardList.objects.filter(name='Daily 12')
        if not daily:
            self.message_user(request,'No list named Daily 12')
            return

        daily = daily[0]
        for i in queryset:
            if daily not in i.lists.all():
                i.lists.add(daily)
                i.save()

        self.message_user(request,'Done adding %s card to Daily 12'% queryset.count())

    add_to_daily.short_description = 'Add selected cards to Daily 12'

    def add_to_community(self,request,queryset):
        community = CardList.objects.filter(name='Community')
        if not community:
            self.message_user(request,'No list named Community')
            return

        community = community[0]
        for i in queryset:
            if community not in i.lists.all():
                i.lists.add(community)
                i.save()

        self.message_user(request,'Done adding %s card to Community'% queryset.count())

    add_to_community.short_description = 'Add selected cards to Community'







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


class ChooseAdmin(admin.ModelAdmin):
    list_display = ('daily_notification','card_lists_count','ready')

    def card_lists_count(self,obj):
        return obj.lists.count()

    def daily_notification(self,obj):
        return obj.message



admin.site.register(Tag)
admin.site.register(Card,CardAdmin)
admin.site.register(CardList,CardListAdmin)
admin.site.register(ShareText)
admin.site.register(Choose,ChooseAdmin)
admin.site.empty_value_display = 'Nothing here'