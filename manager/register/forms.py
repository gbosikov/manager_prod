from register.models import Department as Dep
from register.models import UserProfile
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import *
from django.contrib.auth.models import User


class DateInput(forms.DateInput):
    """
    Create custom widget in your forms.py file
    """
    input_type = 'date'


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(label='E-mail', required=True)
    department = forms.ModelChoiceField(queryset=Dep.objects.all())

    class Meta:
        model = User
        fields = {
            'username',
            'first_name',
            'last_name',
            'email',
            'department',
            'password1',
            'password2',
        }

        labels = {
            'first_name': 'Name',
            'last_name': 'Last Name',
            'department': 'Department',
        }

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.username = self.cleaned_data['username']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        department = self.cleaned_data['department']

        if commit:
            user.save()
            user_profile = UserProfile.objects.create(user=user, department=Dep.objects.get(name=department))
            user_profile.save()

        return user

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].widget.attrs['placeholder'] = 'First name'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Last name'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['placeholder'] = 'E-mail'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Retype Password'
        self.fields['department'].widget.attrs['class'] = 'form-control'


class DepartmentRegistrationForm(forms.Form):
    # social_name = forms.CharField(max_length=80)
    name = forms.CharField(max_length=80)
    email = forms.EmailField()
    # city = forms.CharField(max_length=50)
    # found_date = forms.DateField()

    class Meta:
        model = Dep

    def save(self, commit=True):
        department = Dep()
        # company.social_name = self.cleaned_data['social_name']
        department.name = self.cleaned_data['name']
        department.email = self.cleaned_data['email']
        # company.city = self.cleaned_data['city']
        # company.found_date = self.cleaned_data['found_date']

        if commit:
            department.save()

    def __init__(self, *args, **kwargs):
        super(DepartmentRegistrationForm, self).__init__(*args, **kwargs)
        # self.fields['social_name'].widget.attrs['class'] = 'form-control'
        # self.fields['social_name'].widget.attrs['placeholder'] = 'Social Name'
        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['name'].widget.attrs['placeholder'] = 'Name'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        # self.fields['city'].widget.attrs['class'] = 'form-control'
        # self.fields['city'].widget.attrs['placeholder'] = 'City'
        # self.fields['found_date'].widget.attrs['class'] = 'form-control'
        # self.fields['found_date'].widget.attrs['placeholder'] = 'Found date'


class ProfilePictureForm(forms.Form):
    img = forms.ImageField()

    class Meta:
        model = UserProfile
        fields = ['img']

    def save(self, request, commit=True):
        user = request.user.userprofile_set.first()
        user.img = self.cleaned_data['img']

        if commit:
            user.save()

        return user

    def __init__(self, *args, **kwargs):
        super(ProfilePictureForm, self).__init__(*args, **kwargs)
        self.fields['img'].widget.attrs['class'] = 'custom-file-input'
        self.fields['img'].widget.attrs['id'] = 'validatedCustomFile'


class FileFieldForm(forms.ModelForm):
    file = forms.FileField(
        label='file',
        widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)

    class Meta:
        model = UploadFiles
        fields = ('file',)


class TaskRegistrationForm(forms.ModelForm):
    resp_person = forms.ModelChoiceField(queryset=User.objects.filter(is_superuser=0))
    status = forms.ModelChoiceField(queryset=Status.objects.all(), required=False)
    dead_line = forms.DateField(widget=DateInput, required=False)
    files = forms.FileInput()

    class Meta:
        model = Task
        fields = ['department',
                  'resp_person',
                  'task_name',
                  'status',
                  'dead_line',
                  'description',

                  ]

    def __init__(self, *args, **kwargs):
        super(TaskRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['department'].widget.attrs['class'] = 'form-control'
        self.fields['department'].widget.attrs['placeholder'] = 'Department'
        self.fields['resp_person'].widget.attrs['class'] = 'form-control'
        self.fields['resp_person'].widget.attrs['placeholder'] = 'resp_person'
        self.fields['task_name'].widget.attrs['class'] = 'form-control'
        self.fields['task_name'].widget.attrs['placeholder'] = 'Task name'
        self.fields['status'].widget.attrs['class'] = 'form-control'
        self.fields['status'].widget.attrs['placeholder'] = 'Status'
        self.fields['dead_line'].widget.attrs['class'] = 'form-control'
        self.fields['dead_line'].widget.attrs['placeholder'] = 'dead line'
        self.fields['description'].widget.attrs['class'] = 'form-control'
        self.fields['description'].widget.attrs['placeholder'] = 'Description'



class AddCommentForm(forms.ModelForm):
    comment = forms.Textarea(attrs={"rows": 5, "cols": 20})

    class Meta:
        model = Comments
        fields = ['comment'
                  ]

    def __init__(self, *args, **kwargs):
        super(AddCommentForm, self).__init__(*args, **kwargs)
        self.fields['comment'].widget.attrs['class'] = 'form-control'
        self.fields['comment'].widget.attrs['placeholder'] = 'Leave your comment'
        self.fields['comment'].widget.attrs['rows'] = 4
        self.fields['comment'].widget.attrs['columns'] = 10





