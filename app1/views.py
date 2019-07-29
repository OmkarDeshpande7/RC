from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect, render_to_response
# built in django registration form
from django.views.generic import DetailView, TemplateView
from app1.models import MCQ, UserProfile, Question_list, Chart
import random
import datetime
from django.contrib.auth import authenticate,login , logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

def home(request): #for logging in
    if request.method == "GET":
        return render(request, 'reg_form.html')
    else:
        return render(request, 'reg_form.html')

#@login_required()
def timer(request):
    if request.user.id:
        if request.method == 'POST':
            currentuser = request.user.id
            data = UserProfile.objects.get(user_id = currentuser)
            data.timer = datetime.datetime.now()
            data.save()
            return display(request)
        else:
            return score_chart(request)
    else:
        return register(request)

@csrf_exempt
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email_1 = request.POST['email_1']
        email_2 = request.POST['email_2']
        name_1 = request.POST['name_1']
        name_2 = request.POST['name_2']
        number_1 = request.POST['num_1']
        number_2 = request.POST['num_2']
        #ad_pass = request.POST['ad_pass']
        # for validation of the user

        def validate():
            if username and password and email_1 and name_1 and number_1:
                pass
            else:
                return 1

            if User.objects.filter(username=username).exists():
                return 2

        if validate() == 1:
            return render(request,'reg_form.html', {"error": "Some Fields are Empty !!!"})
        if validate() == 2:
            return render(request,'reg_form.html', {"error": "User Already Exists"})


        user = User.objects.create(username=username, password=password)
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                datas = UserProfile.objects.filter(user_id=request.user.id)
                for data in datas:
                    data.level = request.POST['level']
                    data.email_1 = request.POST['email_1']
                    if request.POST['email_2']:
                        data.email_2 = request.POST['email_2']
                    data.name_1 = request.POST['name_1']
                    if request.POST['name_2']:
                        data.name_2 = request.POST['name_2']
                    data.number_1 = request.POST['num_1']
                    if request.POST['num_2']:
                        data.number_2 = request.POST['num_2']
                    data.save()
                    return rules(request)
        else:
            return render_to_response('reg_form.html', {"error": "Invalid data input"})
    else:
        return render(request, 'reg_form.html')



#for accessing rules page
@login_required()
def rules(request):
    if request.method == 'POST':
        return render(request, 'rules.html')
    else:
        return score_chart(request)

#for displaying questions on the page
@login_required()
def display(request):
    if request.method == 'POST':
        currentuser = request.user.id
        data = UserProfile.objects.get(user_id = currentuser)
        if (data.no_question < 97):
            m = random.randint(1,99)
            check = Question_list.objects.filter(user_id = currentuser)
            check = check.filter(question_list = m)
            pmark = +4
            nmark = 0
            if check:
                return display(request)
            else:
                show = MCQ.objects.get(id = m)
                if int(show.level) == int(data.level):
                    data.no_question += 1
                    data.save()
                    login_time = data.timer
                    login_time_sec = ((login_time.hour)*60*60)+((login_time.minute)*60)+(login_time.second)
                    time_kill = login_time_sec + 1680 + data.add_time
                    now = datetime.datetime.now()
                    now_sec = ((now.hour)*60*60)+((now.minute)*60)+(now.second)
                    time = time_kill - now_sec
                    if time<=0:
                        return score_chart (request)
                    else:
                        ques = Question_list.objects.create(user_id = currentuser, question_list = m,)
                        show = MCQ.objects.get(id = m)

                    context = {'v' : show, 'u' : data, 't' : time , 'w' : ques,'pmark':pmark , 'nmark':nmark}
                    return render (request, 'display.html', context)
                else:
                    return display(request)
        else:
            return score_chart(request)
    else:
        return context(request)

#for checking the answer
def anscheck(request):
    if request.user.id :
        if request.method == 'POST':
            currentuser = request.user.id
            data = UserProfile.objects.get(user_id = currentuser)
            check = Question_list.objects.filter(user_id = currentuser).last()
            show = MCQ.objects.get(id = check.question_list)
            if check.attempt_count == 1:
                isActive = True
                pmark=4
                nmark=0
                
                check.attempt_count-=1
                check.save()
                n = 0
                if request.POST.get('try1'):
                    n = request.POST.get('try1')
                check.ans1 = n
                check.save()
                if show.answer == int(n):
                    data.attempt_question += 1
                    data.score += 4
                    data.save()
                    return display(request)
                else:
                    data.score -= 0
                    data.save()
                    #args = {'v' : show , 'u' : data ,'w' : check}
                    #return render (request, 'app1/display.html', args)
                    return context(request)

            if check.attempt_count == 0:
                isActive = False
                check.attempt_count-=1
                check.save()
                n = 0
                if request.POST.get('try2'):
                    n = request.POST.get('try2')
                check.ans2 = n
                check.save()
                if show.answer == int(n):
                    data.attempt_question += 1
                    data.score += 2
                    data.save()
                    return display(request)
                else:
                    data.score -= 1
                    data.save()
                    return display(request)
        else:
            return score_chart(request)
    else:
        return render(request, 'reg_form.html')

def context(request):
	ques = Question_list.objects.filter(user_id = request.user.id).last()
	m = ques.question_list
	show = MCQ.objects.get(id = m)
	data = UserProfile.objects.get(user_id = request.user.id)
	pmark=2
	nmark=-1
	login_time = data.timer
	login_time_sec = ((login_time.hour)*60*60)+((login_time.minute)*60)+(login_time.second)
	time_kill = login_time_sec + 1680 + data.add_time
	now = datetime.datetime.now()
	now_sec = ((now.hour)*60*60)+((now.minute)*60)+(now.second)
	time = time_kill - now_sec

	value = {'v' : show, 'u' : data, 't' : time , 'w': ques,'pmark':pmark,'nmark':nmark}
	return render (request, 'display.html', value)

def validate_username(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': User.objects.filter(username=username).exists()
    }
    if data['is_taken']:
        data['error_message'] = 'A user with this username already exists.'
    return JsonResponse(data)

def score_chart(request):
    #check = UserProfile.objects.get(user_id = request.user.id)
    if request.user.id:
    #if request.method == "POST":

        data = Chart.objects.get(id = 1)
        check = UserProfile.objects.get(user_id = request.user.id)
        if check.score >-30 and check.score < -20 :
            data.score_30 += 1
        if check.score >-20 and check.score < -10 :
            data.score_20 += 1
        if check.score >-10 and check.score < 0 :
            data.score_10 += 1
        if check.score > 0 and check.score < 10 :
            data.score_10p += 1
        if check.score > 10 and check.score < 20 :
            data.score_20p += 1
        if check.score > 20 and check.score < 30 :
            data.score_30p += 1
        data.save()
        content = {'v' : data,'u':check}
        logout(request)
        return render (request, 'Result.html', content)
    else:
        return render (request , 'reg_form.html')

def url(request):
    return register(request)


@csrf_exempt
def logged(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        ad_pass = request.POST['ad_pass']
        if not ad_pass == "NORSians":
            return render_to_response('login.html', {"error": "Admin password required or incorrect !"})

        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                data = UserProfile.objects.get(user_id=request.user.id)
                data.add_time = request.POST.get('add_time')
                data.save()
                return context(request)
            return render(request, 'login.html')
        else:
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')
