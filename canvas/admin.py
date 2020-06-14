from django.contrib import admin
from .models import Event,Task
from users.models import Profile
# Register your models here.
admin.site.register(Event)
admin.site.register(Task)
admin.site.register(Profile)
