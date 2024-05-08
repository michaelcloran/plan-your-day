import datetime
from datetime import datetime
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse
from .models import Category, Tasks

from .forms import CategoriesForm, TasksForm, TasksViewDate, TaskStatistics


# Create your views here.
def home_view(request):
    """This function is used as the landing view
    of the website and displays a list of tasks
    based on logged in user and todays date.

    If the user is not logged in then a redirect
    is done to account_login

    Args:
        request (request.user.is_authenticated):
        checks to see if user ias logged in

    Returns:
        render: renders the index.html page
        if the user is authenticated
    """
    if not request.user.is_authenticated:
        return redirect(f"{'account_login'}")

    todays_date = datetime.now()

    tasks = Tasks.objects.filter(date__range=[todays_date, todays_date],
                                 author=request.user)

    categories = Category.objects.filter(author=request.user)

    context = {
        'tasks': tasks,
        "categories": categories,
    }

    return render(
        request,
        'tasks/index.html',
        context,
    )


def home_view2(request, view_date):
    """This function is used to display
    a list of tasks at a particular date

    Args:
        request (request.user): is used to
        get logged in user and to pass
        tasks based on it.
        view_date (string): This is the
        view_date wanted to display by.
        It will display tasks based on
        logged in user and view_date

    Returns:
        render: returns the context
        and page to render with the
        context infos.
    """

    tasks = Tasks.objects.filter(date__range=[view_date, view_date],
                                 author=request.user)

    categories = Category.objects.filter(author=request.user)

    context = {
        'tasks': tasks,
        "categories": categories,
    }

    return render(
        request,
        'tasks/index.html',
        context,
    )


def categories_listing(request):
    """This view method is used to view
    the categories and to pass the categories
    to the categories.html template

    Args:
        request (request.user):used to get only
        the categories fo the logged in user

    Returns:
        render: returns the categories to be viewed
        by the categories.html file
    """
    categories = Category.objects.filter(author=request.user)

    context = {
        "categories": categories,
    }
    return render(
        request,
        "tasks/categories.html",
        context,
    )


def category_listing(request):
    """passes the category_form to the
    add_category.html file

    Args:
        request (request.user):THe categories form
        requires that request.user be passed

    Returns:
        render: returns the category_form
        to the add_category.html template
    """

    category_form = CategoriesForm(request=request)

    return render(
        request,
        "tasks/add_category.html",
        {
            "category_form": category_form,
        },
    )


def task_listing(request):
    """passes the TasksForm and tasks
    to the add_task.html template

    Args:
        request (request.user): used to authenticate
        and display the form with only categories
        for the logged in  user

    Returns:
        render: returns tasks and the task_form
        to the add_task.html template
    """
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
    """This function if the request method is
    a POST if the form is valid saves the form
    and creates a new category

    Args:
        request (data, request): the data and request
        information is required for this form
        foo (string): This was used to single out
        a url to add the category

    Returns:
        render: category_form to add_category.html
        template
    """
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

    #         category_form = CategoriesForm(request=request)

    # return render(
    #     request,
    #     "tasks/add_category.html",
    #     {
    #         "category_form": category_form,
    #     },
    # )
    return HttpResponseRedirect(reverse('categories'))


def add_task(request, foo):
    """This function adds a task to the tasks list

    Args:
        request (data, request.user): the request.user
        is used to get the categories and to display only
        valid ones for the logged in user
        foo (string): This value was used to single out
        this url in the urls list

    Returns:
        render: task_form to add_task.html
    """
    task_form = None
    if request.method == "POST":
        task_form = TasksForm(data=request.POST, request=request)
        if task_form.is_valid():
            new_task = None
            new_task = task_form.save(commit=False)
            new_task.author = request.user
            new_task.save()
            messages.add_message(
                request, messages.SUCCESS,
                'task submitted'
            )

            # task_form = TasksForm(request=request)

    # return render(
    #     request,
    #     "tasks/add_task.html",
    #     {
    #         "task_form": task_form,
    #     },
    # )
    date_from = request.POST.get('date')

    return redirect(reverse('home2', args=[date_from]))


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

        category = get_object_or_404(Category, pk=category_id)
        category_form = CategoriesForm(data=request.POST, instance=category,
                                       request=request)

        if category_form.is_valid() and category.author == request.user:
            category = category_form.save(commit=False)
            category.approved = False
            category.save()
            messages.add_message(request, messages.SUCCESS,
                                 'Category Updated!')
        else:
            messages.add_message(request, messages.ERROR,
                                 'Error updating category!')

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

        task = get_object_or_404(Tasks, pk=task_id)
        task_form = TasksForm(data=request.POST, instance=task,
                              request=request)

        if task_form.is_valid() and task.author == request.user:
            new_task = task_form.save(commit=False)
            new_task.approved = False
            new_task.save()
            messages.add_message(request, messages.SUCCESS, 'Task Updated!')
        else:
            messages.add_message(request, messages.ERROR,
                                 'Error updating task!')

    date_from = request.POST.get('date')

    return redirect(reverse('home2', args=[date_from]))


def task_edit_with_date(request, view_date, task_id):
    """This function allows an edit of a task with the
    view_date in the url

    Args:
        request (data, request): The task form requires
        the data and instance and request = request.user
        in order to validate the categories listing for
        the logged in user
        view_date (string): This value is used to pass
        the view_date to the home2 view for listing
        task_id (int): used to uniquely identify the
        task to be edited

    Returns:
        redirect: to home2 given date_from
    """
    if request.method == "POST":

        task = get_object_or_404(Tasks, pk=task_id)
        task_form = TasksForm(data=request.POST, instance=task,
                              request=request)

        if task_form.is_valid() and task.author == request.user:
            new_task = task_form.save(commit=False)
            new_task.approved = False
            new_task.save()
            messages.add_message(request, messages.SUCCESS, 'Task Updated!')
        else:
            messages.add_message(request, messages.ERROR,
                                 'Error updating task!')

    date_from = view_date

    return redirect(reverse('home2', args=[date_from]))


def category_delete(request, category_id):
    """
    Delete an individual category

    **context**

    ``post``
        an instance of :model:`tasks.Category`
    ``category``
        a single category
    """

    category = get_object_or_404(Category, pk=category_id)

    if category.author == request.user:
        category.delete()
        messages.add_message(request, messages.SUCCESS, 'Category deleted!')
    else:
        messages.add_message(request, messages.ERROR,
                             'You can only delete your own categories!')

    return HttpResponseRedirect(reverse('categories'))


def task_delete(request, task_id):
    """
    Delete an individual task

    **context**


    ``task``
        a single task
    """
    task = get_object_or_404(Tasks, pk=task_id)

    if task.author == request.user:
        task.delete()
        messages.add_message(request, messages.SUCCESS, 'Task deleted!')
    else:
        messages.add_message(request, messages.ERROR,
                             'You can only delete your own tasks!')

    return HttpResponseRedirect(reverse('home'))


def task_delete_with_date(request, view_date, task_id):
    """This function is used to delete a task with
    a date in the url

    Args:
        request (user): if the task.author == request.user
        then the task with task_id is deleted
        view_date (string): the view date is passed to
        the function in order to pass the view_date
        to the renderer home2
        task_id (int): The id of the task to be
        deleted

    Returns:
        redirect: to home2 given date_from
    """

    task = get_object_or_404(Tasks, pk=task_id)

    if task.author == request.user:
        task.delete()
        messages.add_message(request, messages.SUCCESS, 'Task deleted!')
    else:
        messages.add_message(request, messages.ERROR,
                             'You can only delete your own tasks!')

    date_from = view_date

    return redirect(reverse('home2', args=[date_from]))


def tasks_date_view(request):
    """This function is used to render
    the TasksViewDate  form and to on
    submitting to view the tasks by the
    date set

    Args:
        request (_type_): _description_

    Returns:
        render: returns the context to index
        if a POST else to view-date.html
    """

    tasks = Tasks.objects.filter(author=request.user)
    categories = Category.objects.filter(author=request.user)
    view_date_form = TasksViewDate()

    context = ""

    if request.method == "POST":
        date = request.POST.get('date_to_view')

        tasks = Tasks.objects.filter(date__range=[date, date],
                                     author=request.user)

        categories = Category.objects.filter(author=request.user)

        context = {
            'tasks': tasks,
            'categories': categories,
        }
    else:
        context = {
            'tasks': tasks,
            'categories': categories,
            'view_date_form': view_date_form,
        }

    if request.method == "POST":
        return render(
            request,
            'tasks/index.html',
            context,
        )
    else:
        return render(
            request,
            "tasks/view-date.html",
            context,
        )


def task_statistics(request):
    """To allow a logged in user of the system
    an avenue to display statistics based on
    category where for each task a category is
    used as a marked for a task. When the user
    chooses the from date and to_date and the
    category then the results are displayed
    in hours minutes and seconds used for that
    category within the time frame

    Args:
        request (user): THe user logged in

    Returns:
        render: with context and tasks_stats_form

    """
    tasks = Tasks.objects.filter(author=request.user)

    result = []
    context = ""

    if request.method == "POST":
        date_from = request.POST.get('date_from')
        date_to = request.POST.get('date_to')

        category = request.POST.get('category_sel')

        tasks = Tasks.objects.filter(date__range=[date_from, date_to],
                                     category_id=category, author=request.user)

        task_statistics_form = TaskStatistics(data=request.POST,
                                              request=request)

        # already checked for author = request.user
        if task_statistics_form.is_valid():

            task_seconds = 0

            for task in tasks:
                time1 = task.start_time
                time2 = task.end_time

                timeformat = "%H:%M:%S"
                delta = datetime.strptime(str(time2), timeformat) \
                    - datetime.strptime(str(time1), timeformat)

                task_seconds += delta.total_seconds()

                task_sec = delta.total_seconds()
                tot_hours = task_sec // 3600
                tot_min = (task_sec % 3600) // 60
                tot_seconds = (task_sec % 3600) % 60
                result.append(f"Total time on {task.task_name}")
                result.append(f"Hours:{tot_hours} minutes:{tot_min}"\
                              f" seconds:{tot_seconds}")

            total_seconds = task_seconds
            total_hours = total_seconds // 3600
            total_min = (total_seconds % 3600) // 60
            total_seconds = (total_seconds % 3600) % 60
            result.append("Total")
            result.append(f"Hours:{total_hours} minutes:{total_min}"\
                          f" seconds:{total_seconds}")
        else:
            messages.add_message(request, messages.ERROR,
                                 'Ops! something went wrong!!')

        context = {
            'result': result,
            'task_statistics_form': task_statistics_form,
            'tasks': tasks,
            'category': category,
        }

    else:
        task_statistics_form = TaskStatistics(request=request)

        context = {
            'result': result,
            'task_statistics_form': task_statistics_form,
            'tasks': tasks,
        }

    return render(
        request,
        'tasks/statistics.html',
        context,
    )
