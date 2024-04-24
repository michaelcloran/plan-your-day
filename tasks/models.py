from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=25, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="category_post")

    class Meta:
        ordering = ["category_name", "author"]


    def __str__(self):
        return f"{self.category_name} | written by {self.author}"

class Tasks(models.Model):
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="task_post"
    )
    task_name = models.CharField(max_length=50, unique=True)
    task_description = models.TextField()
    is_urgent = models.BooleanField(default=False)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE, related_name = "category")

    class Meta:
        ordering = ["-date", "author"]


    def __str__(self):
        return f"{self.task_name} | written by {self.author}"
