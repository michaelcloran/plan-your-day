from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import UserManager


def randomString():
    """This function is used to set a random string
    to the slug
    """
    um = UserManager()
    return (um.make_random_password(length=25))


# Create your models here.
class Category(models.Model):
    """This is the model for the Category

    Args:
        models (models.Model): The model to be
        used in the database

    Returns:
        category_name: return the category_name
    """
    category_name = models.CharField(max_length=25)
    slug = models.SlugField(max_length=200, unique=True,  default=randomString)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="category_post")

    class Meta:
        ordering = ["category_name", "author"]

    def __str__(self):
        return f"{self.category_name}"


class Tasks(models.Model):
    """This si the task model for setting
    up the database

    Args:
        models (models.Model): the model to be used
        in the database

    Returns:
        task_name: returns the task_name of the Task
    """
    slug = models.SlugField(max_length=200, unique=True, default=randomString)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="task_post"
    )
    task_name = models.CharField(max_length=50)
    task_description = models.TextField()
    is_urgent = models.BooleanField(default=False)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE,
                                    related_name="category")
    finished_task = models.BooleanField(default=False)

    class Meta:
        ordering = ["start_time", "author"]

    def __str__(self):
        return f"{self.task_name}"
