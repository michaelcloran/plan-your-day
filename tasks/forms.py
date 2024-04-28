from django import forms
from .models import Category,Tasks



class CategoriesForm(forms.ModelForm):
    """
    Allows a category
    """
    class Meta:
        model = Category
        fields = ('category_name',)


class DateInput(forms.DateInput):
    input_type = 'date'
class TasksForm(forms.ModelForm):
    """
    A tasks form

    Args:
        forms (_type_): _description_
    """
    class Meta:
        model = Tasks
        fields = ('category_id', 'task_name', 'task_description', 'is_urgent', 'date', 'start_time', 'end_time')

        widgets = {
            'date': DateInput()
        }