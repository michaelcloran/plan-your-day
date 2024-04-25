from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from .models import Category, Tasks

from .forms import CategoriesForm


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

    return render(
        request,
        "tasks/categories.html",
        {
        "categories": categories,
        },
    )

def category_listing(request):
    categories = Category.objects.all()

    category_form = CategoriesForm()

    return render(
        request,
        "tasks/add_category.html",
        {
        "category_form": category_form,
        },
    )


def add_category(request, foo):

    if request.method == "POST":
        print("IN POST")
        category_form = CategoriesForm(data=request.POST)
        if category_form.is_valid():
            new_cat = None
            new_cat = category_form.save(commit=False)
            new_cat.author = request.user
            new_cat.save()
            messages.add_message(
                request, messages.SUCCESS,
                'Category submitted and awaiting approval'
            )

    category_form = CategoriesForm()

    return render(
        request,
        "tasks/add_category.html",
        {
        "category_form": category_form,
        },
    )
