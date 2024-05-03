import datetime
from datetime import datetime, timedelta
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse
from .models import Category, Tasks

from .forms import CategoriesForm, TasksForm, TasksViewDate, TaskStatistics


# Create your views here.
def home_view(request):
    if not request.user.is_authenticated:
        return redirect(f"{'account_login'}")
    print(f"TP home view : {request.POST}, : {request}")

    todays_date = datetime.now()

    tasks = Tasks.objects.filter(date__range=[todays_date, todays_date],author=request.user)

    categories = Category.objects.filter(author=request.user)

    context = {
        'tasks':tasks,
        "categories": categories,
    }

    return render(
        request,
        'tasks/index.html',
        context,
    )

def home_view2(request, view_date):

    tasks = Tasks.objects.filter(date__range=[view_date, view_date],author=request.user)

    categories = Category.objects.filter(author=request.user)

    context = {
        'tasks':tasks,
        "categories": categories,
    }

    return render(
        request,
        'tasks/index.html',
        context,
    )

def categories_listing(request):
    categories = Category.objects.filter(author=request.user)

    return render(
        request,
        "tasks/categories.html",
        {
        "categories": categories,
        },
    )

def category_listing(request):
    categories = Category.objects.filter(author=request.user)

    category_form = CategoriesForm(request=request)

    return render(
        request,
        "tasks/add_category.html",
        {
        "category_form": category_form,
        },
    )

def task_listing(request):
    tasks = Tasks.objects.filter(author=request.user)

    task_form = TasksForm(request=request)


    return render(
        request,
        "tasks/add_task.html",
        {

        "tasks": tasks,
        "task_form": task_form,
        },
    )

def add_category(request, foo):
    category_form = None
    if request.method == "POST":
        category_form = CategoriesForm(data=request.POST, request=request)
        if category_form.is_valid():
            new_cat = None
            new_cat = category_form.save(commit=False)
            new_cat.author = request.user
            new_cat.save()
            messages.add_message(
                request, messages.SUCCESS,
                'Category submitted'
            )

            category_form = CategoriesForm(request=request)

    return render(
        request,
        "tasks/add_category.html",
        {
        "category_form": category_form,
        },
    )

def add_task(request, foo):
    task_form = None
    if request.method == "POST":
        task_form = TasksForm(data=request.POST,request=request)
        if task_form.is_valid():
            new_task = None
            new_task = task_form.save(commit=False)
            new_task.author = request.user
            new_task.save()
            messages.add_message(
                request, messages.SUCCESS,
                'task submitted'
            )

            task_form = TasksForm(request=request)

    return render(
        request,
        "tasks/add_task.html",
        {
        "task_form": task_form,
        },
    )

def category_edit(request, category_id):
    """
    Display and individual category for edit

    **Context**


   ``category``
      a single category related to the POST
   ``category_form``
      an instance of :form:`tasks.CategoryForm`
    """
    if request.method == "POST":

        categories = Category.objects.filter(author=request.user)

        category = get_object_or_404(Category, pk=category_id)
        category_form = CategoriesForm(data=request.POST, instance=category,request=request)
        print("TP1:", category_form)

        if category_form.is_valid() and category.author == request.user:
            category = category_form.save(commit=False)
            #category.post = category
            category.approved = False
            category.save()
            messages.add_message(request, messages.SUCCESS, 'Category Updated!')
        else:
            messages.add_message(request, messages.ERROR, 'Error updating category!')

    categories = Category.objects.all()
    # return render(
    #     request,
    #     "tasks/categories.html",
    #     {'categories':categories,},
    # )
    return HttpResponseRedirect(reverse('categories'))

def task_edit(request, task_id):
    """
    Display and individual category for edit

    **Context**


   ``category``
      a single category related to the POST
   ``category_form``
      an instance of :form:`tasks.CategoryForm`
    """
    if request.method == "POST":

        tasks = Tasks.objects.filter(author=request.user)

        task = get_object_or_404(Tasks, pk=task_id)
        task_form = TasksForm(data=request.POST, instance=task, request=request)
        print("TP1:", task_form)

        if task_form.is_valid() and task.author == request.user:
            new_task = task_form.save(commit=False)
            #category.post = category
            new_task.approved = False
            new_task.save()
            messages.add_message(request, messages.SUCCESS, 'Task Updated!')
        else:
            messages.add_message(request, messages.ERROR, 'Error updating task!')

    date_from = request.POST.get('date')
    tasks = Tasks.objects.filter(date__range=[date_from, date_from],author=request.user)
    categories = Category.objects.filter(author=request.user)

    return redirect(reverse('home2' ,args=[date_from]))

def task_edit_with_date(request, view_date, task_id):
    if request.method == "POST":

        tasks = Tasks.objects.filter(author=request.user)

        task = get_object_or_404(Tasks, pk=task_id)
        task_form = TasksForm(data=request.POST, instance=task, request=request)
        print("TP1:", task_form)

        if task_form.is_valid() and task.author == request.user:
            new_task = task_form.save(commit=False)
            #category.post = category
            new_task.approved = False
            new_task.save()
            messages.add_message(request, messages.SUCCESS, 'Task Updated!')
        else:
            messages.add_message(request, messages.ERROR, 'Error updating task!')

    date_from = view_date # request.POST.get('date')
    tasks = Tasks.objects.filter(date__range=[date_from, date_from],author=request.user)
    categories = Category.objects.filter(author=request.user)

    context = {
        'tasks':tasks,
        "categories": categories,
    }
    # return render(
    #     request,
    #     'tasks/index.html',
    #     context,
    # )
    #return HttpResponseRedirect(reverse('home'))
    return redirect(reverse('home2' ,args=[date_from]))
    #return redirect(reverse('home'), context=context)

def category_delete(request, category_id):
    """
    Delete an individual category

    **context**

    ``post``
        an instance of :model:`tasks.Category`
    ``category``
        a single category
    """
    categories = Category.objects.filter(author=request.user)
    # post = get_object_or_404(queryset, slug=slug)
    category = get_object_or_404(Category, pk=category_id)

    if category.author == request.user:
        category.delete()
        messages.add_message(request, messages.SUCCESS, 'Category deleted!')
    else:
        messages.add_message(request, messages.ERROR, 'You can only delete your own categories!')

    categories = Category.objects.all()
    # return render(
    #     request,
    #     "tasks/categories.html",
    #     {'categories':categories,},
    # )
    return HttpResponseRedirect(reverse('categories'))

def task_delete(request, task_id):
    """
    Delete an individual task

    **context**


    ``task``
        a single task
    """
    tasks = Tasks.objects.filter(author=request.user)
    # post = get_object_or_404(queryset, slug=slug)
    task = get_object_or_404(Tasks, pk=task_id)

    if task.author == request.user:
        task.delete()
        messages.add_message(request, messages.SUCCESS, 'Task deleted!')
    else:
        messages.add_message(request, messages.ERROR, 'You can only delete your own tasks!')

    categories = Category.objects.filter(author=request.user)
    tasks = Tasks.objects.filter(author=request.user)

    #date_from = request.POST.get('date')
    context = {
        'tasks':tasks,
        "categories": categories,
    }

    # return render(
    #     request,
    #     'tasks/index.html',
    #     context,
    # )
    #return redirect(reverse('home2' ,args=[date_from]))
    return HttpResponseRedirect(reverse('home'))

def task_delete_with_date(request, view_date, task_id):
    tasks = Tasks.objects.filter(author=request.user)
    # post = get_object_or_404(queryset, slug=slug)
    task = get_object_or_404(Tasks, pk=task_id)

    if task.author == request.user:
        task.delete()
        messages.add_message(request, messages.SUCCESS, 'Task deleted!')
    else:
        messages.add_message(request, messages.ERROR, 'You can only delete your own tasks!')

    categories = Category.objects.filter(author=request.user) #??
    tasks = Tasks.objects.filter(author=request.user) #??


    # context = {
    #     'tasks':tasks,
    #     "categories": categories,
    # }

    date_from = view_date

    # return render(
    #     request,
    #     'tasks/index.html',
    #     context,
    # )
    return redirect(reverse('home2' ,args=[date_from]))

def tasks_date_view(request):
    print("TP here")

    tasks = Tasks.objects.filter(author=request.user)
    categories = Category.objects.filter(author=request.user)
    view_date_form = TasksViewDate()

    context = ""

    if request.method == "POST":
        date = request.POST.get('date_to_view')

        print(date)
        tasks = Tasks.objects.filter(date__range=[date,date], author=request.user)
        print(date)
        categories = Category.objects.filter(author=request.user)

        context = {
        'tasks':tasks,
        'categories': categories,
        }
    else:
        context = {
        'tasks':tasks,
        'categories': categories,
        'view_date_form': view_date_form,
        }

    if request.method == "POST":
        return render (
            request,
            'tasks/index.html',
            context,
        )
    else:
        return render (
            request,
            "tasks/view-date.html",
            context,
        )

def task_statistics(request):
    tasks = Tasks.objects.filter(author=request.user)

    result = ""
    context = ""

    if request.method == "POST":
        date_from = request.POST.get('date_from')
        date_to = request.POST.get('date_to')

        category = request.POST.get('category_sel')

        tasks = Tasks.objects.filter(date__range=[date_from, date_to], category_id=category, author=request.user)

        task_statistics_form = TaskStatistics(data=request.POST,request=request)


        # already checkded for author = request.user
        if task_statistics_form.is_valid():

            task_seconds = 0

            for task in tasks:
                time1 = task.start_time
                time2 = task.end_time

                timeformat = "%H:%M:%S"
                delta = datetime.strptime(str(time2), timeformat) - datetime.strptime(str(time1), timeformat)

                task_seconds += delta.total_seconds()


            total_seconds = task_seconds
            total_hours = total_seconds // 3600
            total_min = (total_seconds % 3600) // 60
            total_seconds = (total_seconds % 3600) % 60
            result = f"Hours:{total_hours} minutes:{total_min} seconds:{total_seconds}"
        else:
            messages.add_message(request, messages.ERROR, 'Ops! something went wrong!!')

        context = {
        'result': result,
        'task_statistics_form':task_statistics_form,
        'tasks':tasks,
        'category': category,
        }

    else:
        task_statistics_form = TaskStatistics(request=request)

        context = {
        'result': result,
        'task_statistics_form':task_statistics_form,
        'tasks':tasks,

        }


    return render (
        request,
        'tasks/statistics.html',
        context,
    )
