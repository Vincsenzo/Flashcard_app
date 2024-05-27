from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm


def login_user(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("flashcard:stack_list_view")
        
        else:
            fail_message = "Wrong username or password."
            messages.error(request, fail_message)
            return redirect("users:login")

    else:
        if request.user.is_authenticated:
            return render(request, 'users/profile.html')
        else:
            return render(request, 'users/login.html')
    

def logout_user(request):
    logout(request)
    # messages.success(request, 'You were logged out')
    return redirect("flashcard:stack_list_view")


def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration succesful!')
            return redirect("users:login")
    else:
        form = UserCreationForm()

    context = {'form':form}
    return render(request, 'users/register_user.html', context)
