from django.contrib import admin
from .models import Category, Tasks

# Register your models here.
#admin.site.register(Category)
#admin.site.register(Tasks)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    allows listing of categorys by name and author
    """
    list_display = ('category_name', 'author',)


@admin.register(Tasks)
class TaskAdmin(admin.ModelAdmin):
    """
    Allows listing of tasks by name and author
    """

    list_display = ('task_name', 'author',)