from django import template
from register.models import *

register = template.Library()

@register.simple_tag()
def task_set(user_id=None):
    a = User.objects.get(user_id=user_id)
    b = a.task_set
    return a
