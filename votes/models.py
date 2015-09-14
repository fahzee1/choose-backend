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


class TheVote(Base):
    user = models.ForeignKey('users.UserProfile',related_name='twin_vote')
    category = models.ForeignKey(Category,related_name='category')
    image = models.ImageField(upload_to='images/%Y/%m/%d')
    left_label = models.CharField(max_length=255, blank=False, help_text='Most likely name of user')
    right_label = models.CharField(max_length=255, blank=False,help_text='Most likey name of celebrity')
    total_votes_yes = models.BigIntegerField(default=0)
    total_votes_no = models.BigIntegerField(default=0)
    facebook_shared = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created']

    def __unicode__(self):
        return "%s vs %s" % (self.left_label,self.right_label)

    def to_dict(self):
        data = {}
        data['category'] = self.category.to_dict()
        data['user'] = self.user.to_dict()
        data['vote'] = {
                        'image':self.image.url,
                        'left_label':self.left_label,
                        'right_label':self.right_label,
                        'total_votes':self.total_votes_yes + self.total_votes_no,
                        'votes_yes':self.total_votes_yes,
                        'votes_no':self.total_votes_no,
                        'featured':self.featured,
                        'facebook_shared':self.facebook_shared,
                        'created':self.created
                        }

        return data

    @classmethod
    def queryset_to_dict(cls,qs):
        data = []
        for item in qs:
            data.append(item.to_dict())

        return data

    def get_percentage(self):
        total = self.total_votes_yes + self.total_votes_no
        yes = float(self.total_votes_yes) / float(total) * 100
        no = float(self.total_votes_no) / float(total) * 100

        data = {
            'yes':yes,
            'no':no,
            'total':total
        }

        return data


