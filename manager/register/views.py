from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import login
from django.shortcuts import redirect
from django.urls import reverse
from .forms import *
from django.contrib.auth.models import User


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        context = {'form': form}
        if form.is_valid():
            user = form.save()
            created = True
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            context = {'created': created}
            return HttpResponseRedirect(reverse('core:index'), context)
        else:
            return render(request, 'register/reg_form.html', context)
    else:
        form = RegistrationForm()
        context = {
            'form': form,
        }
        return render(request, 'register/reg_form.html', context)


def usersView(request):
    users = UserProfile.objects.all()
    tasks = Task.objects.all()
    context = {
        'users': users,
        'tasks': tasks,
    }
    return render(request, 'register/users.html', context)


def user_view(request, profile_id):
    user = UserProfile.objects.get(id=profile_id)
    department = User.objects.get(id=profile_id)
    context = {
        'user_view': user,
        'department': department
    }
    return render(request, 'register/user.html', context)


def profile(request):
    if request.method == 'POST':
        img_form = ProfilePictureForm(request.POST, request.FILES)
        print('PRINT 1: ', img_form)
        context = {'img_form': img_form}
        if img_form.is_valid():
            img_form.save(request)
            updated = True
            context = {'img_form': img_form, 'updated': updated}
            return render(request, 'register/profile.html', context)
        else:
            return render(request, 'register/profile.html', context)
    else:
        img_form = ProfilePictureForm()
        context = {'img_form': img_form}
        return render(request, 'register/profile.html', context)


def newDepartment(request):
    if request.method == 'POST':
        form = DepartmentRegistrationForm(request.POST)
        context = {'form': form}
        if form.is_valid():
            form.save()
            created = True
            form = DepartmentRegistrationForm()
            context = {
                'created': created,
                'form': form,
                       }
            return render(request, 'register/new_department.html', context)
        else:
            return render(request, 'register/new_department.html', context)
    else:
        form = DepartmentRegistrationForm()
        context = {
            'form': form,
        }
        return render(request, 'register/new_department.html', context)


def invites(request):
    return render(request, 'register/invites.html')


def invite(request, profile_id):
    profile_to_invite = UserProfile.objects.get(id=profile_id)
    logged_profile = get_active_profile(request)
    if not profile_to_invite in logged_profile.friends.all():
        logged_profile.invite(profile_to_invite)
    return redirect('core:index')


def deleteInvite(request, invite_id):
    logged_user = get_active_profile(request)
    logged_user.received_invites.get(id=invite_id).delete()
    return render(request, 'register/invites.html')


def acceptInvite(request, invite_id):
    invite = Invite.objects.get(id=invite_id)
    invite.accept()
    return redirect('register:invites')


def remove_friend(request, profile_id):
    user = get_active_profile(request)
    user.remove_friend(profile_id)
    return redirect('register:friends')


def get_active_profile(request):
    user_id = request.user.userprofile_set.values_list()[0][0]
    return UserProfile.objects.get(id=user_id)


def friends(request):
    if request.user.is_authenticated:
        user = get_active_profile(request)
        friends = user.friends.all()
        context = {
            'friends': friends,
        }
    else:
        users_prof = UserProfile.objects.all()
        context= {
            'users_prof': users_prof,
        }
    return render(request, 'register/friends.html', context)


def newTask(request):
    if request.method == 'POST' and request.user.is_authenticated:
        form = TaskRegistrationForm(request.POST)
        context = {'form': form}
        if form.is_valid():
            form = form.save(commit=False)
            form.user = User.objects.get(pk=request.user.id)


            form.save()
            if request.FILES.getlist('file'):
                files = request.FILES.getlist('file')
                for i in files:
                    UploadFiles.objects.create(task=form,
                                               file=i,
                                               user=User.objects.get(pk=request.user.id),
                                               file_name=i)
            return HttpResponseRedirect(reverse('core:index'))
        else:
            return render(request, 'register/new_task.html', context)
    else:
        form = TaskRegistrationForm()
        file_form = FileFieldForm()
        context = {
            'form': form,
            'file_form': file_form
        }
    return render(request, 'register/new_task.html', context)


def show_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    owner = User.objects.get(pk=task.user_id)
    task_files = UploadFiles.objects.filter(task_id=task_id)
    department = Department.objects.get(pk=task.department_id)
    file_name = task_files.values('file_name')
    status = task.status
    task_comments = Comments.objects.filter(task_id=task_id)
    resp_person = task.resp_person

    context = {
        'task_id': task.pk,
        'title': task.task_name,
        'description': task.description,
        'owner': owner,
        'department': department,
        'task_files': task_files,
        'file_name': file_name,
        'status': status,
        'task_comments': task_comments,
        'resp_person': resp_person
    }

    if request.method == 'POST' and request.user.is_authenticated:
        comment_form = AddCommentForm(data=request.POST)


        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            comment_form.comment = request.POST['comment']

            new_comment.task_id = task.pk
            new_comment.post = task
            new_comment.user_id = request.user.id
            new_comment.save()
            context['new_comment'] = new_comment
            context['comment_form'] = comment_form
            context['comment_form'] = AddCommentForm()
        else:
            comment_form = AddCommentForm()
            context['comment_form'] = comment_form

        return render(request, 'register/task.html', context=context)

    return render(request, 'register/task.html', context=context)


def edit_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if request.method != 'POST' and request.user.is_authenticated:
        form = TaskRegistrationForm(instance=task)
    else:
        form = TaskRegistrationForm(instance=task, data=request.POST)
        if form.is_valid():
            form.save()
            if request.FILES.getlist('file'):
                files = request.FILES.getlist('file')
                for i in files:
                    UploadFiles.objects.create(task_id=task_id,
                                               file=i,
                                               user=User.objects.get(pk=request.user.id),
                                               file_name=i)

            return redirect('core:index')
    file_form = FileFieldForm()
    context = {
        'task': task,
        'form': form,
        'file_form': file_form
    }
    return render(request, 'register/edit_task.html', context)


def show_person_tasks(request, user_id):
    # owner_tasks = Task.objects.filter(user_id=profile_id)
    #
    # context = {
    #         'owner_tasks': owner_tasks
    #     }
    return HttpResponse("Hello")












