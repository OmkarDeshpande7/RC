from django.contrib import admin
from django.contrib.auth.models import User
from app1.models import UserProfile,MCQ,Question_list,Chart
admin.site.register(UserProfile,)
admin.site.register(MCQ)
admin.site.register(Question_list)
admin.site.register(Chart)

# Register your models here.
