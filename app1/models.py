from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.core.validators import validate_email
import datetime
from django.db.models import Max
from django.contrib import messages
from django.contrib import admin 

class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	score = models.IntegerField(default = 0)
	timer = models.TimeField(default = '00:00')
	email_1 = models.EmailField(max_length = 100, validators = [validate_email], default = "player_1@gmail.com", editable = True)
	email_2 = models.EmailField(max_length = 100 , validators = [validate_email], default = "player_2@gmail.com", editable = True)
	name_1 = models.CharField(max_length = 100, default = "player_1", editable = True)
	name_2 = models.CharField(max_length = 100 ,default = "player_2", editable = True)
	number_1 = models.IntegerField(default = 0 , editable = True)
	number_2 = models.IntegerField(default = 0 , editable = True)
	level =  models.IntegerField(default = 0)
	no_question =  models.IntegerField(default = 0)
	attempt_question = models.IntegerField(default = 0)
	add_time = models.IntegerField(default = 0)

	def __str__(self):
		return self.user.username

class UserProfileAdmin(admin.ModelAdmin):
	list_display = ('user','score','timer','email_1','email_2','no_question')
	actions = ['maximum']

	def maximum(self,request,queryset):
		max_marks = UserProfile.objects.all().aggregate(Max('score'))
		self.message_user(request,'{} Maximum score'.format(max_marks['score__max']),level=messages.INFO)

def create_profile(sender, **kwargs):
	if kwargs['created']:
		user_profile = UserProfile.objects.create(user=kwargs['instance'])

post_save.connect(create_profile, sender=User) 

class Question_list(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	question_list = models.IntegerField(default = 0)
	attempt_count = models.IntegerField(default = 1)
	ans1 = models.IntegerField( null = True, editable = True)
	ans2 = models.IntegerField(null = True, editable  =True)


def create_list(sender, **kwargs):
	if kwargs['created']:
		ques = Question_list.objects.create(user=kwargs['instance'])

post_save.connect(create_list, sender=User) 

class MCQ(models.Model):
	question = models.CharField(max_length=150, default=' ')
	answer = models.IntegerField(default=0)
	level =  models.IntegerField(default = 0)

	def __str__(self):
		return self.question

class Chart(models.Model):
	score_30 = models.IntegerField(default = 0)
	score_20 = models.IntegerField(default = 0)
	score_10 = models.IntegerField(default = 0)
	score_10p = models.IntegerField(default = 0)
	score_20p = models.IntegerField(default = 0)
	score_30p = models.IntegerField(default = 0)


