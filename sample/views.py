from django.shortcuts import redirect,render, HttpResponseRedirect
from app1 import views
def login_redirect(request):
    return HttpResponseRedirect( '/app1/register')
    #return views.register(request)