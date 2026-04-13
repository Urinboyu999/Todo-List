from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import datetime

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Todo
# Create your views here.

from datetime import datetime

@login_required(login_url='/login/')
def main(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        date_str = request.POST.get('notif_date')
        time_str = request.POST.get('notif_time')

        full_datetime = None
        if date_str:
            # Agar sana bor, lekin vaqt yo'q bo'lsa, 00:00 deb belgilaymiz
            final_time = time_str if time_str else "00:00"
            try:
                datetime_str = f"{date_str} {final_time}"
                full_datetime = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M')
            except ValueError:
                full_datetime = None

        if title:
            Todo.objects.create(
                user=request.user, 
                title=title, 
                description=description,
                time_notification=full_datetime
            )
            return redirect('main') # POSTdan keyin refreshda qayta jo'natmaslik uchun

    todos = Todo.objects.filter(user=request.user, is_completed=False).order_by('-created_at')
    completed_todos = Todo.objects.filter(user=request.user, is_completed=True).order_by('-updated_at')
    
    context = {
        'todos': todos,
        'completed_todos': completed_todos,
    }
    return render(request, 'main.html', context)

@login_required(login_url='/login/')
def complete_todo(request, pk):
    todo = get_object_or_404(Todo, pk=pk, user=request.user)
    todo.is_completed = True
    todo.save()
    return redirect('main')


@login_required(login_url='/login/')
def detail_todo(request, pk):
    todos = get_object_or_404(Todo, pk=pk, user=request.user)
    todos.delete()
    return redirect('main')


#  Login and Register

def login_view(request):
    if request.user.is_authenticated:
        return redirect('main')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', '/')
            return redirect(next_url)
        else:
            messages.error(request, "Login yoki parol xato")

    templates = loader.get_template('login.html')
    return HttpResponse(templates.render({}, request))

def register_view(request):
    if request.user.is_authenticated:
        return redirect('main')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password != password2:
            messages.error(request, 'Ikka parol mos kelmadi')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Bu username mavjud')
        else:
            user = User.objects.create_user(username=username, password=password)
            login(request, user)
            return redirect('main')
        
    templates = loader.get_template('register.html')
    return HttpResponse(templates.render({}, request))


def logout_view(request):
    logout(request)
    return redirect('/login/')