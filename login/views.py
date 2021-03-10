from django.shortcuts import render

from django.http import Http404, HttpResponseRedirect
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import auth
from django.template.context_processors import csrf

from django.contrib.auth.forms import UserCreationForm

from django.urls import reverse

from catalog.models import Task_theme, Task, Solution, Comment, Search, Message


def login(request):
	args = {}
	args.update(csrf(request))
	if request.POST:
		username = request.POST.get('username', '')
		password = request.POST.get('password', '')
		user = auth.authenticate(username=username, password=password)
		if user is not None:
			auth.login(request, user)

			theme_list = Task_theme.objects.all()
			offer_tasks_list = Task.objects.order_by('-pub_date')[:9]

			return render(request, 'index.html', {'offer_tasks_list': offer_tasks_list, 'theme_list': theme_list, 'username': auth.get_user(request)})
		else:
			args['login_error'] = "Пользователь не найден"
			return render(request, 'login.html', args)
	else:
		theme_list = Task_theme.objects.all()
		return render(request, 'login.html', {'username': auth.get_user(request), 'theme_list': theme_list})


def logout(request):
	auth.logout(request)
	return render(request, 'login.html', {})


def register(request):
	args = {}
	args.update(csrf(request))
	args['form'] = UserCreationForm()
	theme_list = Task_theme.objects.all()
	args['theme_list'] = theme_list
	if request.POST:
		newuser_form = UserCreationForm(request.POST)
		if newuser_form.is_valid():
			newuser_form.save()
			newuser = auth.authenticate(username=newuser_form.cleaned_data['username'], password=newuser_form.cleaned_data['password2'])
			auth.login(request, newuser)
			theme_list = Task_theme.objects.all()
			offer_tasks_list = Task.objects.order_by('-pub_date')[:9]
			return render(request, 'index.html', {'offer_tasks_list': offer_tasks_list, 'theme_list': theme_list, 'username': auth.get_user(request).username})
		else:
			args['form'] = newuser_form
	return render(request, 'register.html', args)