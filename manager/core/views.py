from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.urls import reverse
from django.http import HttpResponseRedirect
from register.models import Department
from register.models import UserProfile
from register.models import Task

# Create your views here.


def index(request):
    tasks = Task.objects.all()
    context = {
        'tasks': tasks,
    }
    return render(request, 'core/index.html', context=context)


def dashboard(request):
    users = User.objects.all()
    active_users = User.objects.all().filter(is_active=True)
    departments = Department.objects.all()
    tasks = Task.objects.all()
    context = {
        'users': users,
        'active_users': active_users,
        'departments': departments,
        'tasks': tasks,
    }
    return render(request, 'core/dashboard.html', context)


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            authenticated_user = authenticate(username=request.POST['username'], password=request.POST['password'])
            login(request, authenticated_user)
            return redirect('core:index')
        else:
            return render(request, 'register/login.html', {'login_form': form})
    else:
        form = AuthenticationForm()
    return render(request, 'register/login.html', {'login_form': form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('core:login'))


def context(request): # send context to base.html
    # if not request.session.session_key:
    #     request.session.create()
    users = User.objects.all()
    users_prof = UserProfile.objects.all()
    if request.user.is_authenticated:
        try:
            users_prof = UserProfile.objects.exclude(
                id=request.user.userprofile_set.values_list()[0][0])  # exclude himself from invite list
            user_id = request.user.userprofile_set.values_list()[0][0]
            logged_user = UserProfile.objects.get(id=user_id)
            friends = logged_user.friends.all()
            context = {
                'users': users,
                'users_prof': users_prof,
                'logged_user': logged_user,
                'friends': friends,
            }
            return context

        except:
            users_prof = UserProfile.objects.all()
            context = {
                'users': users,
                'users_prof': users_prof,
            }
            return context
    else:
        context = {
            'users': users,
            'users_prof': users_prof,
        }
        return context








