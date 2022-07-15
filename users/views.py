from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from blogs.forms import CustomUserCreationForm


def register(request):
    """Register a new user."""
    if request.method == 'POST':
        # Process completed form.
        form = CustomUserCreationForm(data=request.POST)

        if form.is_valid():
            user = form.save()
            password = form.cleaned_data.get("password1")
            authenticate(username=user.username, password=password)
            login(request, user)
            return redirect('blogs:index')
        
    else:
        # Display blank registration form
        form = CustomUserCreationForm()

    # Display a blank or invalid form.
    context = {'form': form}
    return render(request, 'registration/register.html', context)
    