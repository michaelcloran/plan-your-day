from django import forms
from .models import Category



class CategoriesForm(forms.ModelForm):
    """
    Allows a category
    """
    class Meta:
        model = Category
        fields = ('category_name',)