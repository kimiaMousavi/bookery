from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm


def logout_view(request):
    logout(request)


def register(request):
    """Register a new user."""

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        print(form)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return render(request, 'search/index.html')

    else:
        form = UserCreationForm()
    context = {'form': form}
    return render(request, 'registration/register.html', context)
