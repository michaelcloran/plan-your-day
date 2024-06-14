from django.contrib import admin
from .models import Category, Tasks

# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    allows listing of categories by name and author
    """
    list_display = ('category_name', 'author',)


@admin.register(Tasks)
class TaskAdmin(admin.ModelAdmin):
    """
    Allows listing of tasks by name and author
    """

    list_display = ('task_name', 'author', 'date')
