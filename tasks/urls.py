from django.urls import path
from . import views

urlpatterns = [


     path('', views.home_view, name='home'),
     path('tasks/', views.task_listing, name='tasks'),

     path('view-date/', views.tasks_date_view, name='tasks_date_view'),




     path('statistics/', views.task_statistics, name='view_task_statistics'),



     path('view-date/edit_task/<int:task_id>', views.task_edit, name='tasks_edit'),
     path('view-date/delete_task/<int:task_id>',
          views.task_delete, name='task_delete'),

     path('<str:view_date>/edit_task/<int:task_id>', views.task_edit_with_date, name='tasks_edit_width_date'),
     path('<str:view_date>/delete_task/<int:task_id>',
          views.task_delete_with_date, name='task_delete_with_date'),
     path('view-date/<str:view_date>/delete_task/<int:task_id>',
          views.task_delete_with_date, name='task_delete_with_date'),

     path('add_task/<str:foo>/',views.add_task, name='add_task' ),



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

     path('<str:view_date>/', views.home_view2, name='home2'),



]