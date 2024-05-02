from django.urls import path
from . import views

urlpatterns = [
     path('', views.home_view, name='home'),

     #path('statistics/', views.task_statistics, name="task_statistics"),
     #path('view-statistics/', views.task_statistics_initial, name='view-statistics-form'),
     path('statistics/', views.task_statistics, name='view_task_statistics'),

     path('task_view_date/', views.task_date_view, name='task_date_view'),
     path('view-date/', views.task_date_view_initial, name='view-date'),

     path('task_view_date/edit_task/<int:task_id>', views.task_edit, name='tasks_edit'),
     path('task_view_date/delete_task/<int:task_id>',
          views.task_delete, name='task_delete'),

     path('add_task/<str:foo>/',views.add_task, name='add_task' ),
     path('tasks/', views.task_listing, name='tasks'),
     path('edit_task/<int:task_id>', views.task_edit, name='tasks_edit'),
     path('delete_task/<int:task_id>',
          views.task_delete, name='task_delete'),

     path('categories/', views.categories_listing, name='categories'),
     path('category/', views.category_listing, name='category'),
     path('add_category/<str:foo>/',views.add_category, name='add_category' ),

     path('categories/edit_category/<int:category_id>',
          views.category_edit, name='category_edit'),

     path('categories/delete_category/<int:category_id>',
          views.category_delete, name='category_delete'),



]