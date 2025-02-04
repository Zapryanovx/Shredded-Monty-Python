from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import RegisterForm, LoginForm


def homepage_view(request):
    """Render the homepage."""
    return render(request, 'homepage.html')


def contact_view(request):
    """Render the contact page. """
    return render(request, 'contact.html')


def register_view(request):
    """
    Handle user registration.

    If the request method is POST, validate the form and create a new user.
    If the form is valid, log in the user and redirect to the homepage.
    If the request method is GET, display the registration form.

    """
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('homepage')
    else:
        form = RegisterForm()
    
    return render(request, 'register.html', {'form': form})


def login_view(request):
    """
    Handle user login.

    If the request method is POST, validate the form and authenticate the user.
    If authentication is successful, log in the user and redirect to the homepage.
    If the request method is GET, display the login form.
    
    """
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
    
    return render(request, 'login.html', {'form': form})
