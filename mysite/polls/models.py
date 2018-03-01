import datetime
from django.db import models
from django.utils import timezone

# Create your models here.

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        # returns the question in string format instead of Django field representation
        return self.question_text

    def was_published_recently(self):
        # returns boolean value corresponding to whether or not the item was recently published
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        # returns the question in string format instead of Django field representation
        return self.choice_text

"""
class Tl_user(models.Model):
    user_id = models.ForeignKey(User, on_delete=PROTECT)
    provider_id = models.ForeignKey(Provider)
    a_token = models.CharField()
    r_token = models.CharField
    r_lasttime = models.DateTimeField()
    r_sec = models.IntegerField()
    other = models.CharField()

class User(models.Model):
    user_id = models.UUIDField(primary_key=user_id)
    f_name = models.CharField()
    l_name = models.CharField()
    primary_email = models.CharField()
    gender_id = models.ForeignKey(Gender)

class Gender(models.Model):
    gender_id = models.IntegerField()
    gender_nm = models.CharField()

class Provider(models.Model):
    provider_id = models.CharField(primary_key=provider_id)
    display_nm = models.CharField()
    logo_url = models.CharField()
    scopes = models.CharField()
    provider_UUID = models.UUIDField()
"""