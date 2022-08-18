from django.contrib import admin
from .models import Department
from .models import UserProfile
from .models import Invite
from .models import Task


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email']
    search_fields = ['name', ]


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'department', ]


class InviteAdmin(admin.ModelAdmin):
    list_display = ['inviter', 'invited', ]
    search_fields = ['inviter', 'invited', ]
    # list_filter = ['inviter', 'invited,']


# class TaskAdmin(admin.ModelAdmin):
#     list_display = ['task_name', 'project']
#     list_filter = ['project', ]
#     search_fields = ['project']

# Register your models here.


admin.site.register(Department, DepartmentAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Invite, InviteAdmin)
# admin.site.register(Task, TaskAdmin)



