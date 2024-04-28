from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse
from .models import Category, Tasks

from .forms import CategoriesForm, TasksForm


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

def task_listing(request):
    tasks = Tasks.objects.all()

    task_form = TasksForm()

    return render(
        request,
        "tasks/add_task.html",
        {
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

