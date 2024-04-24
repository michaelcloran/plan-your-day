from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from django.shortcuts import redirect, render, get_object_or_404, reverse
from .models import Category, Tasks
from django.conf import settings
from .forms import CategoriesForm
from django.contrib import messages


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

def categories_listing(request):
   categories = Category.objects.all()
    #    post = get_object_or_404(categories)

    #    if request.method == "POST":
    #       category_form = CategoriesForm(data=request.POST)
    #       if category_form.is_valid():
    #          cat = category_form.save(commit=False)
    #          cat.author = request.user
    #          cat.post = post
    #          cat.save()
    #          messages.add_message(
    #             request, messages.SUCCESS,
    #             'Category submitted'
    #          )

    #    category_form = CategoriesForm()

   return render(
      request,
      "tasks/categories.html",
      {
       "categories": categories,

       },
   )
