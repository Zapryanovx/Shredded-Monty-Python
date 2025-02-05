from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from .forms import UserSettingsForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash


@login_required
def view_profile(request):
    """Render the profile view page."""
    return render(request, 'profile/view.html')


@login_required
def progress(request):
    """Render the progress page."""
    return render(request, 'profile/progress.html')


@login_required
def calendar(request):
    """Render the calendar page."""
    return render(request, 'profile/calendar.html')


@login_required
def settings_view(request):
    """
    Handles updating user settings, including profile updates and password changes.
    """
    user = request.user
    profile = user.profile  

    settings_form = UserSettingsForm(request.POST or None, request.FILES or None, initial={
        'username': user.username,
        'email': user.email,
    })
    password_form = PasswordChangeForm(request.POST or None)

    # Handle profile updates
    if request.method == 'POST':
        if 'save_profile' in request.POST and settings_form.is_valid():
            user.username = settings_form.cleaned_data['username']
            user.email = settings_form.cleaned_data['email']
            if 'profile_picture' in request.FILES:
                profile.profile_picture = request.FILES['profile_picture']
            user.save()
            profile.save()
            return redirect('settings')

        # Handle password changes
        if 'change_password' in request.POST and password_form.is_valid():
            current_password = password_form.cleaned_data['current_password']
            new_password = password_form.cleaned_data['new_password']
            confirm_password = password_form.cleaned_data['confirm_password']

            if not user.check_password(current_password):
                password_form.add_error('current_password', 'The current password is incorrect.')
            elif new_password != confirm_password:
                password_form.add_error('confirm_password', 'New password and confirmation do not match.')
            else:
                # Set the new password and update the session hash
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request, user)  # Prevent logout
                return redirect('settings')

    return render(request, 'settings.html', {
        'settings_form': settings_form,
        'password_form': password_form,
        'profile': profile,
    })


def send_emails_view(request):
    """
    Handles sending emails to selected recipients with the option to attach a single file.
    """
    if request.method == 'POST':
        recipient = request.POST.get('recipient')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        attachment = request.FILES.get('attachment')

        email = EmailMessage(
            subject=subject,
            body=message,
            from_email='shreddedmontypython@gmail.com',
            to=[recipient] if recipient != 'all' else [user.email for user in User.objects.all()]
        )

        if attachment:
            email.attach(attachment.name, attachment.read(), attachment.content_type)

        email.send()
        return redirect('send_emails')

    users = User.objects.all()
    return render(request, 'send_emails.html', {'users': users})


@login_required
def logout_view(request):
    """Log the user out and redirect to the homepage."""
    if request.user.is_authenticated:
        logout(request)
    return redirect('homepage')
