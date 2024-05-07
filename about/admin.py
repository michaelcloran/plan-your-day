from django.contrib import admin
from .models import About, ContactFormRequest
from django_summernote.admin import SummernoteModelAdmin


# Register your models here.
@admin.register(About)
class AboutAdmin(SummernoteModelAdmin):
    """
    allows editing of the about user
    """
    summernote_fields = ('content',)


# Note: admin.ModelAdmin is the standard way of registering
#       our model with the admin panel. We do it differently
#       above because we are supplying Summernote fields.
#       If you want to customise the admin panel view in your
#       own projects, then inherit from admin.ModelAdmin like
#       we do below.

@admin.register(ContactFormRequest)
class ContactFormRequestAdmin(admin.ModelAdmin):
    """
    Allows the contact form in admin to be displayed
    with message and a read tick
    """

    list_display = ('message', 'read',)
