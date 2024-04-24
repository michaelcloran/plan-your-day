from . import views
from django.urls import path
from tasks.views import home_view

urlpatterns = [
    #path('', views.TaskList.as_view(), name='home'),
    path('', home_view, name='home')

]