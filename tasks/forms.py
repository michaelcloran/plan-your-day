from datetime import date
from django import forms
from .models import Category,Tasks



class CategoriesForm(forms.ModelForm):
    """
    Allows a category
    """

    def __init__(self, *args, **kwargs):
        """ Grants access to the request object so that only members of the current user
        are given as options"""
        # digout https://stackoverflow.com/questions/8841502/how-to-use-the-request-in-a-modelform-in-django/8841565#8841565

        self.request = kwargs.pop('request')
        super(CategoriesForm, self).__init__(*args, **kwargs)
        self.fields['category_name'].queryset = Category.objects.filter(author=self.request.user)

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

    def __init__(self, *args, **kwargs):
        """ Grants access to the request object so that only members of the current user
        are given as options"""
        # digout https://stackoverflow.com/questions/8841502/how-to-use-the-request-in-a-modelform-in-django/8841565#8841565

        self.request = kwargs.pop('request')
        super(TasksForm, self).__init__(*args, **kwargs)
        self.fields['category_id'].queryset = Category.objects.filter(author=self.request.user)

    class Meta:
        model = Tasks
        fields = ('category_id', 'task_name', 'task_description', 'is_urgent', 'date', 'start_time', 'end_time')

        widgets = {
            'date': DateInput(),

        }

class TasksViewDate(forms.Form):
    today = date.today()
    date_to_view = forms.DateField(initial=today, required=True, widget=forms.DateInput(attrs={'type':'date'}))


class TaskStatistics(forms.Form):

    def __init__(self, *args, **kwargs):
        """ Grants access to the request object so that only members of the current user
        are given as options"""
        # digout https://stackoverflow.com/questions/8841502/how-to-use-the-request-in-a-modelform-in-django/8841565#8841565

        self.request = kwargs.pop('request')
        super(TaskStatistics, self).__init__(*args, **kwargs)
        self.fields['category_sel'].queryset = Category.objects.filter(author=self.request.user)

    def setUser(self):
        tUser = self.user

        return Category.objects.filter(user=tUser)

    today = date.today()
    date_from = forms.DateField(initial=today, required=True, widget=forms.DateInput(attrs={'type':'date'}))
    date_to = forms.DateField(initial=today, required=True, widget=forms.DateInput(attrs={'type':'date'}))

    category_sel = forms.ModelChoiceField(queryset=None)

