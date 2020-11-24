from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Todo
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm

# Create your views here.
@login_required(login_url='login')
def index(request):
  user = request.user
  todos  = Todo.objects.all().filter(user = user)
  context = {
    'todos' : todos
  }  
  return render(request, "index.html", context)

@login_required(login_url='login')
def details(request, id):
  todo = Todo.objects.get(id=id)
  context = {
    'todo' : todo
  }  
  return render(request, "details.html", context)

@login_required(login_url='login')
def add(request):
  if request.method == 'POST':
    title = request.POST['title']
    text = request.POST['text']
    user = request.user
    todo = Todo(title=title, text=text, user=user)
    todo.save()
    return redirect('/todos')
  else:
    return render(request, "add.html")

@login_required(login_url='login')
def delete_todo(request):
  if request.method == 'POST':
      Id = request.POST['Id']
      print(Id)
      content = Todo.objects.all().filter(id=Id)
      content.delete()
      return redirect('/todos')
  else:
      count = Todo.objects.all().count()
      context = {
          'count': count
      }
      return render(request, "delete.html", context)

def registerPage(request):
  if request.user.is_authenticated:
    return redirect('home')
  else:
    form = CreateUserForm()
    if request.method == 'POST':
      form = CreateUserForm(request.POST)
      if form.is_valid():
        form.save()
        user = form.cleaned_data.get('username')
        messages.success(request, 'Account was created for ' + user)

        return redirect('login')
      

    context = {'form':form}
    return render(request, "register.html", context)

def loginPage(request):
  if request.user.is_authenticated:
    return redirect('home')
  else:
    if request.method == 'POST':
      username = request.POST.get('username')
      password =request.POST.get('password')

      user = authenticate(request, username=username, password=password)

      if user is not None:
        login(request, user)
        return redirect('index')
      else:
        messages.info(request, 'Username OR password is incorrect')

    context = {}
    return render(request, "login.html", context)

def logoutUser(request):
  logout(request)
  return redirect('login')