from django.db import models
from django.contrib.auth.models import User
import os


# Create your models here.

class Status(models.Model):
    name = models.CharField(max_length=80, unique=True)


    class Meta:
        verbose_name_plural = 'status'

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=80, unique=True)
    email = models.EmailField()

    class Meta:
        verbose_name_plural = 'Departments'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Task(models.Model):
    """
    User tasks
    """
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    task_name = models.CharField(max_length=80)
    description = models.TextField(blank=False)
    status = models.ForeignKey(Status, on_delete=models.CASCADE, default=1)
    add_date = models.DateTimeField(auto_now_add=True)
    upd_date = models.DateTimeField(auto_now_add=False, auto_now=True)
    dead_line = models.DateField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    resp_person = models.ForeignKey(User, on_delete=models.CASCADE, default=None, related_name='resp_person_article_set')


    class Meta:
        ordering = ['id', 'task_name']

    def __str__(self):
        return self.task_name


class UploadFiles(models.Model):
    """
    Uploaded files to task
    """
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True, blank=True)
    file = models.FileField(upload_to="files/%Y/%m/%d", blank=True, null=True, verbose_name='file')
    file_name = models.CharField(max_length=100, null=True, blank=False)
    add_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.task


class Comments(models.Model):
    """
    Task comments
    """
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    comment = models.TextField(blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    add_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-add_date',)

    def __str__(self):
        return self.comment


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    friends = models.ManyToManyField('self', blank=True)
    img = models.ImageField(upload_to='core/avatar', blank=True, default='core/avatar/blank_profile.png')

    def __str__(self):
        return str(self.user)

    def invite(self, invite_profile):
        invite = Invite(inviter=self, invited=invite_profile)
        invites = invite_profile.received_invites.filter(inviter_id=self.pk)
        if not len(invites) > 0:    # don't accept duplicated invites
            invite.save()

    def remove_friend(self, profile_id):
        friend = UserProfile.objects.filter(id=profile_id)[0]
        self.friends.remove(friend)


class Invite(models.Model):
    inviter = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='made_invites')
    invited = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='received_invites')

    def accept(self):
        self.invited.friends.add(self.inviter)
        self.inviter.friends.add(self.invited)
        self.delete()

    def __str__(self):
        return str(self.inviter)



