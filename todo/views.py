from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import ToDoForm
from .models import ToDo
from django.utils import timezone
from django.contrib.auth.decorators import login_required

def signupuser(request):
    if request.method == 'GET':
        #--RETURN FORM FOR USER SIGN UP
        return render(request, 'todo/signupuser.html', { 'createUserForm': UserCreationForm() })
    else:
        if request.POST['password1'] == request.POST['password2']:
            #--CREATE THE USER
            try:
                userObj = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                userObj.save()
                login(request, userObj)
                return redirect('todos')

            except IntegrityError:
                return render(request, 'todo/signupuser.html', { 'createUserForm': UserCreationForm(), 'requestResult': 'ERROR', 'requestResultCode': 'USER_ALREADY_EXIST', 'requestResultMessage': 'O utilizador já existe.' })
        else:
            return render(request, 'todo/signupuser.html', { 'createUserForm': UserCreationForm(), 'requestResult': 'ERROR', 'requestResultCode': 'PASSWORDS_DONT_MATCH', 'requestResultMessage': 'As passwords não são iguais.' })

def loginuser(request):
    if request.method == 'GET':
        #--RETURN FORM FOR USER LOG IN
        return render(request, 'todo/loginuser.html', { 'authUserForm': AuthenticationForm() })
    else:
        #--AUTHENTICATE THE USER
        userObj = authenticate(request, username=request.POST['username'], password=request.POST['password'])

        if userObj is None:
            return render(request, 'todo/loginuser.html', { 'authUserForm': AuthenticationForm(), 'requestResult': 'ERROR', 'requestResultCode': 'USER_PASSWORD_MISMATCH', 'requestResultMessage': 'O utilizador ou a password estão incorrectos.' })
        else:
            login(request, userObj)
            return redirect('todos')

@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('todos')

def home(request):
    return render(request, 'todo/home.html')

@login_required
def todos(request):
    todoObj = ToDo.objects.filter(user=request.user, dt_completed__isnull=True).order_by('dt_created')
    return render(request, 'todo/listtodos.html', { 'todos': todoObj })

@login_required
def completedtodos(request):
    todoObj = ToDo.objects.filter(user=request.user, dt_completed__isnull=False).order_by('dt_completed')
    return render(request, 'todo/listcompletedtodos.html', { 'todos': todoObj })

@login_required
def createtodo(request):
    if request.method == 'GET':
        #--RETURN FORM FOR TODO CREATION FORM
        return render(request, 'todo/createtodo.html', { 'createTodoForm': ToDoForm() })
    else:
        try:
            formObj = ToDoForm(request.POST)
            todoObj = formObj.save(commit=False)
            todoObj.user = request.user
            todoObj.save()
            return redirect('todos')
        except ValueError:
            return render(request, 'todo/createtodo.html', { 'createTodoForm': ToDoForm(), 'requestResult': 'ERROR', 'requestResultCode': 'INVALID_DATA', 'requestResultMessage': 'A informação enviada é inválida.' })

@login_required
def viewtodo(request, todo_pk):
    todoObj = get_object_or_404(ToDo, pk=todo_pk, user=request.user)

    if request.method == 'GET':
        formObj = ToDoForm(instance=todoObj)
        return render(request, 'todo/viewtodo.html', { 'todo': todoObj, 'todoForm': formObj })
    else:
        try:
            formObj = ToDoForm(request.POST, instance=todoObj)
            formObj.save()
            return redirect('todos')
        except ValueError:
            return render(request, 'todo/viewtodo.html', { 'todo': todoObj, 'todoForm': formObj, 'requestResult': 'ERROR', 'requestResultCode': 'INVALID_DATA', 'requestResultMessage': 'A informação enviada é inválida.' })

@login_required
def completetodo(request, todo_pk):
    todoObj = get_object_or_404(ToDo, pk=todo_pk, user=request.user)

    if request.method == 'POST':
        todoObj.dt_completed = timezone.now()
        todoObj.save()
        return redirect('todos')

@login_required
def deletetodo(request, todo_pk):
    todoObj = get_object_or_404(ToDo, pk=todo_pk, user=request.user)

    if request.method == 'POST':
        todoObj.delete()
        return redirect('todos')