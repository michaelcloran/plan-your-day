from datetime import date
from django import forms
from django.core.exceptions import ValidationError
from .models import Category, Tasks


class CategoriesForm(forms.ModelForm):
    """
    Allows a category
    """

    def __init__(self, *args, **kwargs):
        """ Grants access to the request object so that only members of the
        current user
        are given as options"""
        # digout https://stackoverflow.com/questions/8841502/
        # how-to-use-the-request-in-a-modelform-in-django/8841565#8841565

        self.request = kwargs.pop('request')
        super(CategoriesForm, self).__init__(*args, **kwargs)
        self.fields['category_name'].queryset = Category.objects.filter(
            author=self.request.user)

    class Meta:
        model = Category
        fields = ('category_name',)


class DateInput(forms.DateInput):
    input_type = 'date'


class TasksForm(forms.ModelForm):
    """
    A tasks form

    Args:
        forms (forms.ModelForm): Allows the user an
        ability to add a task
    """

    def __init__(self, *args, **kwargs):
        """ Grants access to the request object so that only members of the
        current user
        are given as options"""
        # digout https://stackoverflow.com/questions/8841502/
        # how-to-use-the-request-in-a-modelform-in-django/8841565#8841565

        self.request = kwargs.pop('request')
        super(TasksForm, self).__init__(*args, **kwargs)
        self.fields['category_id'].queryset \
            = Category.objects.filter(author=self.request.user)

    class Meta:
        model = Tasks
        fields = ('category_id', 'task_name', 'task_description', 'is_urgent',
                  'date', 'start_time', 'end_time')

        widgets = {
            'date': DateInput(),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),

        }

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if start_time > end_time:
            raise ValidationError("The start time must be less than the end time!!")

        return self.cleaned_data


class TasksViewDate(forms.Form):
    """This form is used to set the date
    to view tasks by

    Args:
        forms (date): to set the date
    """
    today = date.today()
    date_to_view = forms.DateField(initial=today,
                                   required=True,
                                   widget=forms.DateInput(
                                    attrs={'type': 'date'}))


class TaskStatistics(forms.Form):
    """This form is used to display the statistics
    form to allow a logged in user access to stats

    Args:
        forms (date): the date from and date to fields
        are date typees and the category is the logged
        in users categories listing
    """

    def __init__(self, *args, **kwargs):
        """ Grants access to the request object so that only members of the
        current user
        are given as options"""
        # digout https://stackoverflow.com/questions/8841502/
        # how-to-use-the-request-in-a-modelform-in-django/8841565#8841565

        self.request = kwargs.pop('request')
        super(TaskStatistics, self).__init__(*args, **kwargs)
        self.fields['category_sel'].queryset = Category.objects.filter(
            author=self.request.user)

    def setUser(self):
        tUser = self.user

        return Category.objects.filter(user=tUser)

    today = date.today()
    date_from = forms.DateField(initial=today, required=True,
                                widget=forms.DateInput(attrs={'type': 'date'}))
    date_to = forms.DateField(initial=today, required=True,
                              widget=forms.DateInput(attrs={'type': 'date'}))

    category_sel = forms.ModelChoiceField(queryset=None)
