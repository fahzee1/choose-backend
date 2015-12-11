import uuid
import binascii
import os
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
from django.utils.encoding import python_2_unicode_compatible
#Below is usefull for turning a middleware class into a decorator for use on a per view bases (Authentication)
#from django.utils.decorators import decorator_from_middleware_with_args, decorator_from_middleware

"""
Add logging
"""

# Prior to Django 1.5, the AUTH_USER_MODEL setting does not exist.
# Note that we don't perform this code in the compat module due to
# bug report #1297
# See: https://github.com/tomchristie/django-rest-framework/issues/1297
AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


GENDER_CHOICES = (
    ('M','Male'),
    ('F','Female'),
    ('T','Transgender')
    )

class MyUserManager(BaseUserManager):
    def create_user(self, email, date_of_birth, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=MyUserManager.normalize_email(email),
            date_of_birth=date_of_birth,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, date_of_birth, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(email,
            password=password,
            date_of_birth=date_of_birth
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class UserProfile(AbstractBaseUser,PermissionsMixin):
    username = models.CharField(max_length=255,default="",blank=True,unique=True)
    first_name = models.CharField(max_length=255,default="",blank=True)
    last_name = models.CharField(max_length=255,default="",blank=True)
    gender = models.CharField(max_length=1,choices=GENDER_CHOICES,blank=True)
    location = models.CharField(max_length=255,default="",blank=True)

    score = models.CharField(max_length=10, blank=True, null=True,default="0")

    facebook_user = models.BooleanField(default=True , blank=True)
    facebook_id = models.CharField(max_length=255,default="",blank=True)

    device_token = models.CharField(default="",max_length=255, blank=True)
    send_notifications = models.BooleanField(default=True)
    fake_user = models.BooleanField(default=False)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    date_of_birth = models.DateField(null=True,blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)


    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['date_of_birth']


    
    def save(self, *args, **kwargs):
        if not self.first_name and not self.last_name and '_' in self.username:
            first, last = self.username.replace('_',' ').split(' ',1)
            self.first_name = first
            self.last_name = last

        if not self.password:
            self.password = str(uuid.uuid4())[:10]
        return super(UserProfile, self).save(*args, **kwargs)



    def _name(self):
        return self.username.replace('_',' ')
    name = property(_name)


    def get_token(self):
        """
        Refers to related Token model in rest_framework
        """
        return self.auth_token.key

    def to_dict(self,token=False):
        data = {}
        data['username'] = self.name
        data['first_name'] = self.first_name
        data['last_name'] = self.last_name
        data['email'] = self.email
        data['facebook_id'] = self.facebook_id
        data['location'] = self.location

        if self.gender:
            data['gender'] = self.gender

        if token:
            data['auth_token'] = self.get_token()


        return data

    @classmethod
    def queryset_to_dict(cls,qs):
        data = []
        for item in qs:
            data.append(item.to_dict())

        return data

    # for django admin
    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin



class UpperUserProfile(UserProfile):
    """
    This class doenst save to DB but works off of above model 
    since its just a proxy
    """

    class Meta:
        proxy = True

    def __unicode__(self):
        return "%s %s" %(self.first_name.upper(),self.last_name.upper())





@python_2_unicode_compatible
class Token(models.Model):
    """
    The default authorization token model.
    """
    key = models.CharField(max_length=40, primary_key=True,editable=False)
    user = models.OneToOneField(AUTH_USER_MODEL, related_name='auth_token')
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super(Token, self).save(*args, **kwargs)

    def generate_key(self):
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return "%s:%s" % (self.user,self.key)



@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
