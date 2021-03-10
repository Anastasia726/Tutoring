from django.contrib import admin

from .models import Task_theme, Task, Solution, Comment, Search, Message

admin.site.register(Task_theme)
admin.site.register(Task)
admin.site.register(Solution)
admin.site.register(Comment)
admin.site.register(Search)
admin.site.register(Message)