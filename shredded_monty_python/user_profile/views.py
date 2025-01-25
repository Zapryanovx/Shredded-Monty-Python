from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

@login_required
def view_profile(request):
    return render(request, 'profile/view.html')

@login_required
def progress(request):
    return render(request, 'profile/progress.html')

@login_required
def calendar(request):
    return render(request, 'profile/calendar.html')

@login_required
def settings(request):
    return render(request, 'profile/settings.html')

@login_required
def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('homepage')  
