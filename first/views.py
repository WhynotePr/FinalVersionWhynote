from django.shortcuts import render, get_object_or_404, redirect
from first.forms import UserForm, UserProfileInfoForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required

import os
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *

from django.views.generic.list import ListView
from django.utils.safestring import mark_safe
from django.template.defaultfilters import slugify
from datetime import timedelta, datetime
from django.utils import timezone
import calendar

#from django.core.files.storage import FileSystemStorage

from .models import *
from taggit.models import Tag
from .utils import Calendar
from .forms import *


def index(request):
    return redirect('first:home')

@login_required
def special(request):
    return HttpResponse("You are logged in!")

@login_required
def user_logout(request):
    logout(request)
    userlogin = ""
    return HttpResponseRedirect(reverse('index'))


def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'profile_pic' in request.FILES:
                print('found it')
                profile.profile_pic = request.FILES['profile_pic']
            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
    return render(request,'registration.html',
                          {'user_form': user_form,
                           'profile_form': profile_form,
                           'registered': registered})
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                return redirect('first:home')
            else:
                return HttpResponse("Your account was inactive.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details given")
    else:
        return render(request, 'login.html', {})


#------------------------------------------------------------------------

def home(request):
    username = request.user.username
    lnl = list()
    lol = list()
    lisp = list()
    nobj = Note.objects.filter(username=username)
    for obj in nobj:
        if not (obj.tag in lol):
            if not(obj.tag == ""):
                lol.append(obj.tag)
    for i in lol:
        lisp.append([i,nobj.filter(tag=i)])
    for obj in Note.objects.all().order_by('-public_date'):
    	if obj.username == username:
    		lnl.append(obj)
    return render(request, 'home.html', {'latest_notes': lnl,'lisp':lisp})

@login_required
def post_new(request):
    username = request.user.username
    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.public_date = timezone.now()
            post.username = username
            post.tag = post.tag
            post.save()
            return redirect('first:home')
    else:
        form = NoteForm()
    return render(request, 'add_note.html', {'form': form})


@login_required
def detail(request, note_id):
    username = request.user.username
    post = get_object_or_404(Note, pk=note_id)
    note = post
    if username == note.username:
        if request.method == "POST":
            form = NoteForm(request.POST, instance=post)
            if form.is_valid():
                post = form.save(commit=False)
                post.public_date = timezone.now()
                post.username = username
                post.save()
                #return redirect('first:detail', note_id=post.pk)
                return redirect('first:home')
        else:
            form = NoteForm(instance=post)
        return render(request, 'add_note.html', {'form': form, 'val':1, 'id':note_id})
    return redirect('first:home')

# For calendar

def calendar_button(request):
    userlogin = request.user.username
    return render(request, 'calendar.html')


class CalendarView(ListView):
    model = Event
    template_name = 'calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Use today's date for the calendar
        d = get_date(self.request.GET.get('month', None))
        # Instantiate calendar class with today's year and date
        cal = Calendar(d.year, d.month, self.request.user.username)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context

def get_date(req_month):
    if req_month:
        year, month = (int(x) for x in req_month.split('-'))
        return datetime.date(year, month, day=1)
    return datetime.datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

def event(request, event_id=None, date=timezone.now()):
    if event_id:
        instance = get_object_or_404(Event, pk=event_id)
    else:
        instance = Event()
    form = EventForm(request.POST or None, instance=instance)
    username = request.user.username
    if 'create_event' in request.POST and form.is_valid():
        post = form.save(commit=False)
        post.public_date = timezone.now()
        post.username = username
        post.save()
        return HttpResponseRedirect(reverse('first:calendar'))
    if 'delete_event' in request.POST and event_id:
        event = Event.objects.get(pk=event_id)
        event.delete()
        return HttpResponseRedirect(reverse('first:calendar'))
    return render(request, 'event.html', {'form': form, 'event_id': event_id})

def add_note_button(request):
    return render(request, 'add_note.html')


@login_required
def delete_note(request, note_id):
    username = request.user.username
    note = Note.objects.get(pk=note_id)
    if note.username == username:
        note.delete()
    return redirect('first:home')

def book_list(request):
    userlogin = request.user.username
    books = []
    for obj in Book.objects.all():
        if obj.username == userlogin:
            books.append(obj)
    return render(request, 'book_list.html', {'books': books})


def upload_book(request):
    username = request.user.username
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.username = username
            #post.url = post.pdf.uploadfile.name
            post.save()
            return redirect('first:book_list')
    else:
        form = BookForm()
    return render(request, 'upload_book.html', {'form': form})

@login_required
def delete_book(request, pk):
    if request.method == 'POST':
        book = Book.objects.get(pk=pk)
        if book.username == request.user.username:
            os.remove(os.path.join(settings.MEDIA_ROOT, book.pdf.name))
            book.delete()
    return redirect('first:book_list')

def about_us(request):
    return render(request, 'about_us.html')


class NoteList(APIView):

    def get(self,request,username):
        notes = Note.objects.filter(username = username)
        serializer = NoteSerializer(notes,many=True)
        return Response(serializer.data)

    def post(self):
        pass

























