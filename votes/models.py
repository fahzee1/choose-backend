import math
import uuid
from django.db import models
from django.conf import settings
from datetime import datetime
from django.utils import timezone
from random import randrange
from parse_rest.connection import register
from parse_rest.installation import Push
from django.core.cache import cache

FAKE_IT = getattr(settings,'FAKE_IT',False)

class Base(models.Model):
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

class Tag(Base):
    name = models.CharField(max_length=255, blank=True)

    def __unicode__(self):
        return self.name

    def to_dict(self):
        data = {}
        data['name'] = self.name
        data['id'] = self.pk
        return data

    @classmethod
    def list_categories(cls):
        data = {}
        categories = cls.objects.all()
        for i in categories:
            data[i.pk] = i.name
        return data




"""
>>> from django.db.models import F
>>> product = Product.objects.get(name='Venezuelan Beaver Cheese')
>>> product.number_sold = F('number_sold') + 1
>>> product.save()
"""

class Card(Base):
    user = models.ForeignKey('users.UserProfile',related_name='card')
    tags = models.ManyToManyField(Tag,related_name='tag',blank=True,null=True)
    image = models.ImageField(upload_to='images/%Y/%m/%d')
    image_url = models.TextField(max_length=255, blank=True, default='',help_text='Static Image url take from above image field')
    question = models.CharField(max_length=255, blank=False, help_text='Title of card')
    question_type = models.IntegerField(default=0,help_text='100 (A/B) or 101 (YES/NO)')
    left_votes_count = models.BigIntegerField(default=0)
    right_votes_count = models.BigIntegerField(default=0)
    left_votes_fake = models.BigIntegerField(default=0)
    right_votes_fake = models.BigIntegerField(default=0)
    facebook_shared = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    branch_link = models.CharField(max_length=255,blank=True)

    class Meta:
        ordering = ['-created']

    def __unicode__(self):
        return "%s (%s)" % (self.question,self.user)

    def to_dict(self):
        #self.created.strftime("%Y-%m-%d %H:%M"),
        data = {
                'user':self.user.to_dict(),
                'id':self.id,
                'question':self.question,
                'question_type':self.question_type,
                'left_count':self.left_votes(),
                'right_count':self.right_votes(),
                'total_votes':self.total_votes(),
                'featured':self.featured,
                'facebook_shared':self.facebook_shared,
                'created':self.created.strftime("%Y-%m-%d %H:%M:%S"),
                'percentage':self.get_percentage()
                }

        # Since its slow to request image urls, cron job should be filling image_url
        if self.image_url:
            data['image'] = self.image_url
        else:
            url = self.image.url
            data['image'] = url
            self.image_url = url
            self.save()

        return data


    def get_percentage(self):
        total = self.total_votes()
        if (total > 0):
            left = float(self.left_votes()) / float(total) * 100
            right = float(self.right_votes()) / float(total) * 100
        else:
            left = 0.0
            right = 0.0

        # get left side of decimal point for both numbers
        leftDecimal = left % 1
        rightDecimal = right % 1

        # if greater then .5 round it up
        if leftDecimal >= .5:
            left = math.ceil(left)

        if rightDecimal >= .5:
            right = math.ceil(right)

        # int() rounds it down if not even
        data = {
            'left':int(left),
            'right':int(right)
        }

        return data

    def left_votes(self):
        return self.left_votes_count + self.left_votes_fake

    def right_votes(self):
        return self.right_votes_count + self.right_votes_fake

    def total_votes(self):
        return self.left_votes_count + self.right_votes_count + self.left_votes_fake + self.right_votes_fake

    def fake_votes(self,save=True,notify=True):
        if FAKE_IT:
            left1 = randrange(0,40)
            left2 = randrange(100,300)
            right1 = randrange(0,30)
            right2 = randrange(100,200)
            left_random = randrange(left1,left2)
            right_random = randrange(right1,right2)
            self.left_votes_fake = self.left_votes_fake + left_random
            self.right_votes_fake = self.right_votes_fake + right_random
            if save:
                self.save()
            if notify:
                total_new_votes = left_random + right_random
                message = "%s new votes on '%s'!" % (total_new_votes,self.question)
                data = {'card_id':str(self.id)}
                self.send_notification(message,data)
                # clear cache? so users see new data
                cache.clear()


    def send_notification(self,message,data={}):
        # sends push to creator of this card
        register(settings.APPLICATION_ID, settings.REST_API_KEY,master_key=settings.MASTER_KEY)
        data['alert'] = message
        data['badge'] = "Increment"
        formatted_name = self.user.username.replace(' ','-')
        Push.alert(data,channels=[formatted_name])

    @classmethod
    def queryset_to_dict(cls,qs):
        data = []
        for item in qs:
            data.append(item.to_dict())

        return data



class CardList(models.Model):
    """
    Should hold lists like 'featured, daily 12, etc'
    """
    name = models.CharField(max_length=255, blank=False, help_text='Name of Card list')
    cards = models.ManyToManyField(Card)
    approved = models.BooleanField(default=False,help_text='Only approved items will be shown in the menu of the client')
    active = models.BooleanField(default=False)
    last_display = models.DateTimeField(auto_now_add=True)
    data_changed = models.BooleanField(default=False)
    uuid = models.UUIDField(default=uuid.uuid4)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.data_changed:
            self.new_uuid(save=False)
            self.data_changed = False
            cache.clear()

        return super(CardList, self).save(*args, **kwargs)

    def to_dict(self):
        data = {
            'id':self.id,
            'name':self.name,
            'approved':self.approved,
            'last_display':self.last_display,
            'uuid':self.uuid
        }

        return data

    def new_uuid(self,save=False):
        new_uuid = uuid.uuid4().hex
        if new_uuid != self.uuid:
            self.uuid = new_uuid
            if save:
                self.save()

    @classmethod
    def queryset_to_dict(cls,qs):
        data = []
        for item in qs:
            data.append(item.to_dict())

        return data

    def now(self):
        return timezone.localtime(timezone.now())


    def hours_since_last(self):
        now = self.now()
        difference = now - self.last_display 
        seconds = float(difference.seconds)
        minutes = float(seconds/60)
        return float(minutes/60)

    @classmethod
    def send_push_notification(cls,message,data={}):
        register(settings.APPLICATION_ID, settings.REST_API_KEY,master_key=settings.MASTER_KEY)
        data['alert'] = message
        data['badge'] = "Increment"

        Push.alert(data,channels=['Choose'])



class Choose(Base):
    message = models.CharField(default='Your cards are ready for the day!',max_length=255,blank=False)
    lists = models.ManyToManyField(CardList,related_name='choose')
    ready = models.BooleanField(default=True)
    last_update = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "%s" % self.message

    def now(self):
        return timezone.localtime(timezone.now())

    def update_date(self):
        self.last_update = self.now()
        self.save()

    def send_notification(self,message=None,data={}):
        from parse_rest.connection import register
        from parse_rest.installation import Push

        register(settings.APPLICATION_ID, settings.REST_API_KEY,master_key=settings.MASTER_KEY)

        if not message:
            message = "%s %s new lists for you to checkout" % (self.message,self.lists.count())

        data['alert'] = message
        data['badge'] = "Increment"

        Push.alert(data,channels=['Choose'])




SHARECHOICES = (
    ('alert','UIAlert'),
    ('popup','UIPopup'),
    ('banner','Banner')
    )

class ShareText(Base):
    """
    Clients fetch this model to show inapp notification/messaging
    """
    message = models.CharField(max_length=255,blank=False)
    display = models.CharField(max_length=6,choices=SHARECHOICES,blank=False,default='popup') 
    shared = models.BooleanField(default=False)

    def __unicode__(self):
        return "%s" % self.message

    def save(self, *args, **kwargs):
        Card.send_push_notification(self.message,{'id':1171,'name':'king jolly'})
        return super(ShareText, self).save(*args, **kwargs)



    @classmethod
    def get_lastest_share_text(cls):
        obj = cls.objects.last()
        if obj:
            data = {
                'id':obj.id,
                'message':obj.message,
                'display':obj.display,
            }
            return data







