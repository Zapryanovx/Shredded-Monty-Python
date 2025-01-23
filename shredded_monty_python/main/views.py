from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required   
from .forms import RegisterForm, LoginForm

def homepage_view(request):
    return render(request, 'homepage.html')

def contact_view(request):
    return render(request, 'contact.html')

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('homepage')
    else:
        form = RegisterForm()
    
    return render(request, 'register.html', {
            'form': form
    })

def login_view(request):
    if request.method == 'POST':    
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('homepage')
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {
        'form': form
    })

@login_required
def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('homepage')  
