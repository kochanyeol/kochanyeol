from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Todo, Comment

class TodoAdmin(SummernoteModelAdmin):
    summernote_fields = ['description']
    fieldsets = [
        ('기본 정보', {'fields': ['user', 'title', 'description', 'start_date', 'end_date']}),
        ('완료 정보', {'fields': ['is_completed', 'completed_image']}),
    ]

admin.site.register(Todo, TodoAdmin)
admin.site.register(Comment)
