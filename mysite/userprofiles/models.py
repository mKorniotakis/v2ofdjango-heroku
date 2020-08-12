# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save

from myapp.models import AuthUser
from django.utils.translation import ugettext_lazy as _

from mysite import settings

GENDER =(('male','Male'),('female','Female'))


class UserProfile(models.Model):  
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    phone = models.PositiveIntegerField(null=True, blank=True)
    gender = models.CharField(max_length=40, blank=True, verbose_name=_(u'Gender'), choices=GENDER) 
    avatar = models.ImageField(upload_to='userprofiles/avatars', null=True, blank=True, verbose_name=_(u'Avatar'))
    completion_level = models.PositiveSmallIntegerField(default=0, verbose_name=_(u'Profile completion percentage'))
    email_is_verified = models.BooleanField(default=False, verbose_name=_(u'Email is verified'))
    personal_info_is_completed = models.BooleanField(default=False, verbose_name=_(u'Personal info completed'))

    class Meta:
        verbose_name=_(u'User profile')
        verbose_name_plural = _(u'User profiles')
        
    def __unicode__(self):
        return u"User profile: %s" % self.user.username
    
    def get_completion_level(self):
        completion_level = 0
        if self.email_is_verified:
            completion_level += 50
        if self.personal_info_is_completed:
            completion_level += 50
        return completion_level
        
    def update_completion_level(self):
        self.completion_level = self.get_completion_level()
        self.save()
        return

    # # Auto-create the profile upon user account creation.
    # # It's important to start with a fresh database so the user and profile ID's match.
    # def create_user_profile(sender, instance, created, **kwargs):
    #     if settings.DEBUG:
    #         print('create_user_profile fired')
    #     if created:
    #         UserProfile.objects.create(user=instance)
    #
    # post_save.connect(create_user_profile, sender=User)
