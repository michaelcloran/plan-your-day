from django import forms
from .models import ContactFormRequest

class ContactRequestForm(forms.ModelForm):
    """
    Allows a form to be displayed for collaboration
    with name email and message fields
    """
    class Meta:
        model = ContactFormRequest
        fields = ('name', 'email', 'message')