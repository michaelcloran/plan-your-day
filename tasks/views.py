from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from .models import Category, Tasks
from django.conf import settings
from django.shortcuts import redirect

# Create your views here.
def home_view(request):
    tasks = Tasks.objects.all()

    context = {
        'tasks':tasks
    }
    if not request.user.is_authenticated:
        return redirect(f"{'account_login'}")
    return render(
        request,
        'tasks/index.html',
        context
    )