from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse
from .models import Category, Tasks

from .forms import CategoriesForm, TasksForm, TasksViewDate


# Create your views here.
def home_view(request):

    tasks = Tasks.objects.all()
    categories = Category.objects.all()

    context = {
        'tasks':tasks,
        "categories": categories,
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

def task_listing(request):
    tasks = Tasks.objects.all()

    task_form = TasksForm()


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
        category_form = CategoriesForm(data=request.POST)
        if category_form.is_valid():
            new_cat = None
            new_cat = category_form.save(commit=False)
            new_cat.author = request.user
            new_cat.save()
            messages.add_message(
                request, messages.SUCCESS,
                'Category submitted'
            )

            category_form = CategoriesForm()

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
        task_form = TasksForm(data=request.POST)
        if task_form.is_valid():
            new_task = None
            new_task = task_form.save(commit=False)
            new_task.author = request.user
            new_task.save()
            messages.add_message(
                request, messages.SUCCESS,
                'task submitted'
            )

            task_form = TasksForm()

    return render(
        request,
        "tasks/add_task.html",
        {
        "task_form": task_form,
        },
    )

def post_detail(request, slug):
   """ Display an individual: model:`tasks.Category`

   **Context**

   ``post``
      an instance of :model:`tasks.Category`.
   ``comments``
      all approved categories related to a post
   ``category_count``
      a count of approved categories related to the category
   ``category_form``
      an instance of :form:`tasks.CategoryForm`

   **Template:**
   :template: `tasks/post_detail.html`
   """

   queryset = Category.objects.all()
   post = get_object_or_404(queryset, slug=slug)

   comments = post.categories.all().order_by("-created_on")
   comment_count = post.categories.all().count()

   if request.method == "POST":
      category_form = CategoryForm(data=request.POST)
      if category_form.is_valid():
         category = category_form.save(commit=False)
         category.author = request.user
         category.post = post
         category.save()
         messages.add_message(
            request, messages.SUCCESS,
            'Category submitted and awaiting approval'
         )

   category_form = CommentForm()

   return render(
      request,
      "tasks/post_detail.html",
      {"post": post,
       "categories": categories,
       "category_count": category_count,
       "category_form": category_form,
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

        categories = Category.objects.all()

        category = get_object_or_404(Category, pk=category_id)
        category_form = CategoriesForm(data=request.POST, instance=category)
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

        tasks = Tasks.objects.all()

        task = get_object_or_404(Tasks, pk=task_id)
        task_form = TasksForm(data=request.POST, instance=task)
        print("TP1:", task_form)

        if task_form.is_valid() and task.author == request.user:
            new_task = task_form.save(commit=False)
            #category.post = category
            new_task.approved = False
            new_task.save()
            messages.add_message(request, messages.SUCCESS, 'Task Updated!')
        else:
            messages.add_message(request, messages.ERROR, 'Error updating task!')

    tasks = Tasks.objects.all()
    categories = Category.objects.all()

    context = {
        'tasks':tasks,
        "categories": categories,
    }
    return HttpResponseRedirect(reverse('home'),context)

def category_delete(request, category_id):
    """
    Delete an individual category

    **context**

    ``post``
        an instance of :model:`tasks.Category`
    ``category``
        a single category
    """
    categories = Category.objects.all()
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
    tasks = Tasks.objects.all()
    # post = get_object_or_404(queryset, slug=slug)
    task = get_object_or_404(Tasks, pk=task_id)

    if task.author == request.user:
        task.delete()
        messages.add_message(request, messages.SUCCESS, 'Task deleted!')
    else:
        messages.add_message(request, messages.ERROR, 'You can only delete your own tasks!')

    categories = Category.objects.all()
    tasks = Tasks.objects.all()


    context = {
        'tasks':tasks,
        "categories": categories,
    }

    return HttpResponseRedirect(reverse('home'),context)

def task_date_view_initial(request):
    print("TP task_view_initial")

    tasks = Tasks.objects.all()
    view_date_form = TasksViewDate()
    return render(
        request,
        "tasks/view-date.html",
        {
        'tasks':tasks,
        'view_date_form': view_date_form,
        },
    )

def task_date_view(request,date):
    #print(date)
    print("TP here")
   # print(request.POST)
    date = request.POST.get('date_to_view')

    print(date)
    tasks = Tasks.objects.filter(date__range=[date,date])
    print(date)

    return render(
        request,
        "tasks/index.html",
        {
        'tasks':tasks,
        },
    )