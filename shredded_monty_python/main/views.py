from django.shortcuts import render

def homepage(request):
    return render(request, 'homepage.html')

def register(request):
    if request.method == "POST":
        pass
    return render(request, 'register.html')

def login(request):
    if request.method == "POST":
        pass
    return render(request, 'login.html')
