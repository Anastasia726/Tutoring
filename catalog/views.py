from django.shortcuts import render

from django.http import Http404, HttpResponseRedirect
from django.contrib import auth
from django.utils import timezone

from django.urls import reverse

from django.contrib.auth.models import User
from .models import Task_theme, Task, Solution, Comment, Search, Message
from django.db.models import Q




# --- Поиск схожих статей по содержимому ---

"""morph = pymorphy2.MorphAnalyzer()

def Delete_punctuacion(text):
    tt = str.maketrans(dict.fromkeys(string.punctuation))
    return (text.translate(tt))

def To_primary_form(text):
    return ' '.join([morph.normal_forms(w)[0] for w in text.split()]) 

def Get_similar(article, stroka, user):
	user_already_read = []
	for v in View.objects.filter(user_name_id = user.id):
		user_already_read.append(v.article_id - 1)
	some_texts = []
	for x in article:
		some_texts.append(To_primary_form(Delete_punctuacion(x.article_text)))
	df = pd.DataFrame({'texts': some_texts})
	find_nearest_to = ' '.join([morph.normal_forms(w)[0] for w in Delete_punctuacion(stroka).split()])
	# формирование весов tf-idf
	tfidf = TfidfVectorizer()
	mx_tf = tfidf.fit_transform(some_texts)
	new_entry = tfidf.transform([find_nearest_to]) 
	# расчет косинусного расстояния
	cosine_similarities = linear_kernel(new_entry, mx_tf).flatten()
	# запишем все попарные результаты сравнений
	df['cos_similarities'] = cosine_similarities
	# отсортируем по убыванию (т.к. cos(0)=1)
	df = df.sort_values(by=['cos_similarities'], ascending=[0])
	# удалим элементы с расстояниями близкими к 1 и 0
	df = df.drop(df[df.cos_similarities > 0.99].index).drop(df[df.cos_similarities < 0.01].index)
	similar = df.index.tolist()
	closest = []
	# сначала те, которые пользователь не читал
	for a in similar:
		if a not in user_already_read:
			closest.append(a)
	for a in similar:
		if a in user_already_read:
			closest.append(a)
	return closest
"""


# --- Поиск статей по запросу ---

"""def Searching(articles, string):
	some_texts = []
	for x in articles:
		some_texts.append(To_primary_form(Delete_punctuacion(x.article_title + ' ' + x.article_text)))
	df = pd.DataFrame({'texts': some_texts})
	print(df)
	find_nearest_to = ' '.join([morph.normal_forms(w)[0] for w in Delete_punctuacion(string).split()])
	# формирование весов tf-idf
	tfidf = TfidfVectorizer()
	mx_tf = tfidf.fit_transform(some_texts)
	new_entry = tfidf.transform([find_nearest_to]) 
	# расчет косинусного расстояния
	cosine_similarities = linear_kernel(new_entry, mx_tf).flatten()
	# запишем все попарные результаты сравнений
	df['cos_similarities'] = cosine_similarities
	# отсортируем по убыванию (т.к. cos(0)=1)
	df = df.sort_values(by=['cos_similarities'], ascending=[0])
	# удалим элементы с расстояниями юлизкими к 0
	df = df.drop(df[df.cos_similarities < 0.00000001].index)
	print(df)
	result = df.index.tolist()
	return result
"""

# --- История поиска пользователя  ---

"""def Get_user_search_info(user):
	if user.is_authenticated:
		search_list = Search.objects.filter(user_name = user).order_by('-search_date')
		search_text_list = []
		for s in search_list:
			for i in range(s.search_number):
				search_text_list.append(s.search_text)
		res = ' '.join(search_text_list)
	else:
		res = []
	return res"""


#Task_theme, Task, Solution, Comment, Search, Message


def index(request):
	theme_list = Task_theme.objects.all()
	offer_tasks_list = Task.objects.order_by('-pub_date')
	return render(request, 'index.html', {'offer_tasks_list': offer_tasks_list, 'theme_list': theme_list, 'username': auth.get_user(request), })
	"""if request.user.is_authenticated:
					offer_tasks_list = Tasks.objects.order_by('-pub_date')
					return render(request, 'index.html', {'offer_tasks_list': offer_tasks_list, 'theme_list': theme_list, 'username': auth.get_user(request).username})
				else:
					return render(request, 'login.html', {})
			"""

def search(request):
	theme_list = Task_theme.objects.all()
	if request.method == 'POST':
		search_field = request.POST['text'];
		search_articles_list = []
		for i in Searching(Task.objects.all(), search_field):
			search_articles_list.append(Task.objects.get(id = i + 1))
	else:
		search_field = ''
		search_articles_list = Article.objects.order_by('-pub_date')[:9]
	return render(request, 'search.html', {'username': auth.get_user(request), 'theme_list': theme_list, 
													'search_articles_list': search_articles_list[:9], 'search_field': search_field})


"""def theme(request, name_of_theme):
	t = Theme.objects.get(theme_name = name_of_theme)
	theme_list = Theme.objects.all()
	ads_left = Ads_left_short()
	ads_right = Ads_right_short()
	if request.user.is_authenticated:
		previous_searchs = Search.objects.filter(user_name = request.user).order_by('-search_date')[:5]
		all_searchs1 = Search.objects.filter(user_name = request.user).order_by('-search_number')
		all_searchs2 = Search.objects.filter(~Q(user_name = request.user)).order_by('-search_number')
		article_theme_list = Article.objects.filter(theme = t.id).order_by('-views')
	else:
		previous_searchs = []
		all_searchs1 = []
		all_searchs2 = Search.objects.order_by('-search_number')
		article_theme_list = Article.objects.filter(theme = t.id).order_by('-views')
	return render(request, 'Articles/theme.html', {'username': auth.get_user(request).username, 'theme': name_of_theme,
												   'theme_list': theme_list, 'article_theme_list': article_theme_list, 
												   'previous_searchs': previous_searchs, 
												   'all_searchs1': all_searchs1, 'all_searchs2': all_searchs2, 
												   'ads_left':ads_left, 'ads_right':ads_right})"""


def task(request, task_id):
	try:
		a = Task.objects.get( id = task_id )
	except:
		raise Http404("Задание не найдено!")

	theme_list = Task_theme.objects.all()

	return render(request, 'task.html', {'username': auth.get_user(request), 'theme_list': theme_list, 
													'task':a, })


"""def leave_comment(request, article_id):
	try:
		a = Article.objects.get( id = article_id )
	except:
		raise Http404("Статья не найдена!")
	a.comment_set.create(author_name = request.user, comment_text = request.POST['text'], comment_pub_date = timezone.now())
	a.num_of_comments = Comment.objects.filter(article_id = article_id).count()
	return HttpResponseRedirect(reverse('Articles:detail', args = (a.id,)))"""





"""def contact(request):
	theme_list = Theme.objects.all()
	ads_left = Ads_left_short()
	ads_right = Ads_right_short()
	if request.user.is_authenticated:
		previous_searchs = Search.objects.filter(user_name = request.user).order_by('-search_date')[:5]
		all_searchs1 = Search.objects.filter(user_name = request.user).order_by('-search_number')
		all_searchs2 = Search.objects.filter(~Q(user_name = request.user)).order_by('-search_number')
	else:
		previous_searchs = []
		all_searchs1 = []
		all_searchs2 = Search.objects.order_by('-search_number')
	return render(request, 'Articles/contact.html', {'username': auth.get_user(request).username,
												   'theme_list': theme_list, 'previous_searchs': previous_searchs, 
												   'all_searchs1': all_searchs1, 'all_searchs2': all_searchs2,
												   'ads_left': ads_left, 'ads_right': ads_right})"""



"""def leave_message(request):
	m = Message(user_name = request.POST['username'], email = request.POST['email'], message_text = request.POST['text'], send_date = timezone.now())
	m.save()
	return HttpResponseRedirect(reverse('Articles:contact', args = ()))"""