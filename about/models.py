from django.db import models

# Create your models here.
class About(models.Model):
    """ Outputs the about text"""
    title = models.CharField(default='testing',max_length=200)
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField(default='Testing')

    def __str__(self):
        return self.title

class ContactFormRequest(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    updated_on = models.DateTimeField(auto_now=True)
    message = models.TextField()
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"Contact request from {self.name}"