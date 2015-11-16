from django.db import models

# Create your models here.

class Base(models.Model):
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

class Category(Base):
    name = models.CharField(max_length=255, blank=False)

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
    category = models.ForeignKey(Category,related_name='category',blank=True,null=True)
    image = models.ImageField(upload_to='images/%Y/%m/%d')
    question = models.CharField(max_length=255, blank=False, help_text='Title of card')
    question_type = models.IntegerField(default=0)
    left_votes_count = models.BigIntegerField(default=0)
    right_votes_count = models.BigIntegerField(default=0)
    facebook_shared = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created']

    def __unicode__(self):
        return "%s (%s)" % (self.question,self.user)

    def to_dict(self):
        data = {}
        #data['category'] = self.category.to_dict()
        data['user'] = self.user.to_dict()
        data['card'] = {
                        'id':self.pk,
                        'image':self.image.url,
                        'left_count':self.left_votes_count,
                        'right_count':self.right_votes_count,
                        'total_votes':self.total_votes(),
                        'featured':self.featured,
                        'facebook_shared':self.facebook_shared,
                        'created':self.created,
                        'percentage':self.get_percentage()
                        }

        return data

    @classmethod
    def queryset_to_dict(cls,qs):
        data = []
        for item in qs:
            data.append(item.to_dict())

        return data

    def get_percentage(self):
        total = self.total_votes()
        if (total > 0):
            left = float(self.left_votes_count) / float(total) * 100
            right = float(self.right_votes_count) / float(total) * 100
        else:
            left = 0.0
            right = 0.0

        data = {
            'left':left,
            'right':right
        }

        return data

    def total_votes(self):
        return self.left_votes_count + self.right_votes_count


