from django.urls import path
from . import views

app_name = 'catalog'
urlpatterns = [
	path('', views.index, name = 'index'),
	path('<int:task_id>/', views.task, name = 'task'),
	path('search/', views.search, name = 'search'),
]


"""path('<int:article_id>/leave_comment/', views.leave_comment, name = 'leave_comment'),
			    path('contact/', views.contact, name = 'contact'),
			    path('leave_message/', views.leave_message, name = 'leave_message'),
				path('<name_of_theme>/', views.theme, name = 'theme'),"""