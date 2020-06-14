from django.shortcuts import render,redirect
from django.urls import reverse
from django.utils.safestring import mark_safe
from datetime import datetime, timedelta
from django.views import generic
from django.shortcuts import get_object_or_404
from datetime import date
from .forms import EventForm, TaskForm
from .models import Event, Task
from django.shortcuts import render
from .utils import Calendar
from django.http import HttpResponse, HttpResponseRedirect
import calendar
# Create your views here.
def HomeView(request):

    tasks=Task.objects.all()
    form=TaskForm(request.POST)
    context = {'tasks': tasks,'form':form}
    if request.method=="POST":
        if form.is_valid():
            form.save()
            return render(request, 'canvas/home.html', context)


    return render(request, 'canvas/home.html', context)


def event(request, event_id=None):
    instance = Event()
    if event_id:
        instance = get_object_or_404(Event, pk=event_id)
    else:
        instance = Event()

    form = EventForm(request.POST or None, instance=instance)
    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('calendar'))
    return render(request, 'canvas/event.html', {'form': form})


class CalendarView(generic.ListView):
    model = Event
    template_name = 'canvas/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # use today's date for the calendar
        d = self.get_date(self.request.GET.get('day', None))
        d = self.get_date(self.request.GET.get('month', None))

        # Instantiate our calendar class with today's year and date
        cal = Calendar(d.year, d.month)
        print("==================")
        print(d.year)
        print(d.month)
        print("===============")

        # Call the formatmonth method, which returns our calendar as a table
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = self.prev_month(d)
        context['next_month'] = self.next_month(d)
        return context

    def prev_month(self, d):
        first = d.replace(day=1)
        prev_month = first - timedelta(days=1)
        month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
        return month

    def next_month(self, d):
        days_in_month = calendar.monthrange(d.year, d.month)[1]
        last = d.replace(day=days_in_month)
        next_month = last + timedelta(days=1)
        month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
        return month

    def get_date(self, req_day):
        if req_day:
            year, month = (int(x) for x in req_day.split('-'))
            return date(year, month, 1)
        return datetime.today()
def updateTask(request,pk):
    task=Task.objects.get(id=pk)
    alltasks=Task.objects.all()
    form= TaskForm(instance=task)
    if request.method =="POST":
        form=TaskForm(request.POST,instance=task)
        if form.is_valid():
            form.save()
            return redirect('/')

    return render(request, 'canvas/update_task.html',{'alltasks': alltasks, 'task': task,'form':form})

