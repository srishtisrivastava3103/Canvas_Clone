from django.db import models
from django.urls import reverse
from datetime import date
# Create your models here.

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    @property
    def get_html_url(self):
        url = reverse('event_edit', args=(self.id,))
        return f'<a href="{url}"> {self.title} </a>'
class Task(models.Model):
    title= models.CharField(max_length=200)
    date= models.DateField(default=date.today)
    time=models.TimeField()
    description=models.TextField(blank=False)
    complete=models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

