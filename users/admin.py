import traceback
from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from users.models import UserProfile, Token
from random import randrange


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = UserProfile
        fields = ('username',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField(label=('Password'),help_text= ("Raw passwords are not stored, change password using <a href=\"password/\">this form</a>."))

    class Meta:
        model = UserProfile
        fields = ('username',)

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]

class UserProfileAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_filter = ('username',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('facebook_image','username','first_name','last_name','gender','location')}),
        ('Social',{'fields':('score','facebook_user','facebook_id')}),
        ('Permissions', {'fields': ('is_admin','is_superuser')}),
        ('Important dates', {'fields': ('last_login',)}),
    )

    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username','email', 'password1', 'password2')}
        ),
    )
    search_fields = ('email','username')
    ordering = ('email',)
    readonly_fields = ('facebook_image',)
    actions = ['format_username']

    def format_username(self,request,queryset):
        for i in queryset:
            name = i.username
            if name == 'cjogbuehi':
                continue

            if len(name.split(' ')) == 2:
                first, last = name.split(' ')
                first = first.capitalize()
                last = last.capitalize()
                name = first + ' ' + last
            elif len(name.split(' ')) == 1:
                name = name.capitalize()

            else:
                name = 'Rename user %s' % randrange(0,5000)

            i.username = name
            try:
                i.save()
            except:
                traceback.print_exc()

        self.message_user(request,'Succesfully formated %s usernames' % queryset.count())
    format_username.short_description = 'Capitalize usernames'

# Register your models here.
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Token)