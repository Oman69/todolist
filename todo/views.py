from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login,logout, authenticate
from .models import ToDo
from .forms import ToDoForm



def home (request):
    return render(request, 'todo/home.html')


def signup_user(request):
    if request.method == 'GET':
        return render(request, 'todo/signup_user.html', {'form': UserCreationForm()})
    else:
        #Create new user
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                # Save new user
                user.save()
                # Login new user
                login(request, user)
                # Redirect to todos page
                return redirect('current_todo')
            except IntegrityError:
                return render(request, 'todo/signup_user.html', {'form': UserCreationForm(), 'error': 'Это имя уже используется!!!'})

        else:
            print('Password is not correct!')
            return render(request, 'todo/signup_user.html', {'form': UserCreationForm(), 'error': 'Пароли не совпадают!!!'})



def current_todo(request):
    todos = ToDo.objects.filter(user=request.user, deadline__isnull=True)
    return render(request, 'todo/current.html', {'todos': todos})


def view_todo(request, todo_pk):
    todos = get_object_or_404(ToDo, pk=todo_pk, user=request.user)
    if request.method == 'GET':
        form = ToDoForm(instance=todos)
        return render(request, 'todo/view.html', {'todos': todos, 'form': form})
    else:
        try:
            form = ToDoForm(request.POST, instance=todos)
            form.save()
            return redirect('current_todo')
        except ValueError:
            return render(request, 'todo/view.html', {'todos': todos, 'form': form, 'error': 'Bad data!'})



def delete_todo(request, todo_pk):
    todos = get_object_or_404(ToDo, pk=todo_pk, user=request.user)
    if request.method == 'GET':
        todos.delete()
        return redirect('current_todo')
    else:
        pass


def create_todo(request):
    if request.method == 'GET':
        return render(request, 'todo/create.html', {'form': ToDoForm()})
    else:
        try:
            form = ToDoForm(request.POST)
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return redirect('current_todo')
        except ValueError:
            return render(request, 'todo/create.html', {'form': ToDoForm(), 'error': 'Слишком длинный заголовок!'})


def login_user(request):
    if request.method == 'GET':
        return render(request, 'todo/login.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'todo/login.html', {'form': AuthenticationForm(), 'error': 'Пользователь с таким именем не найден'})
        else:
            login(request, user)
            return redirect('current_todo')


def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')