from django.urls import path
from tasks.views import home_view, categories_listing




urlpatterns = [
    #path('', views.TaskList.as_view(), name='home'),
    path('', home_view, name='home'),
    path('categories/', categories_listing, name='categories'),

]