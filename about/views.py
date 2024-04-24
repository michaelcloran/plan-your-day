from django.shortcuts import render
from .models import About
from django.contrib import messages
from .forms import ContactRequestForm

# Create your views here.
def about_me(request):
    """
    Renders the most recent information on the website author
    and allows the collaboration requests
    Displays an individual instance of :model:`about.About`.
    **Context**
    ``about``
        The most recent instance of :model:`about.About`.
    ``collaborate_form``
        an instance of :form:`about.CollaborateForm`.
    **Template**
    :template:`about/about.html`
    """
    if request.method == "POST":
        contact_form = ContactRequestForm(data=request.POST)
        if contact_form.is_valid():
            contact_form.save()
            messages.add_message(
                request,
                messages.SUCCESS,
                'Contact request received! I endeavor to respond within 2 working days.'
            )

    about = About.objects.all() # .order_by('-updated_on').first()
    contact_form = ContactRequestForm()

    return render(
        request,
        "about/about.html",
        {"about": about,
         "contact_form": contact_form
         },
    )
