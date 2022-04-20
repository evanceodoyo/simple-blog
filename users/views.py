from django.shortcuts import render, redirect
from django.contrib.auth import login
from blogs.forms import CustomUserCreationForm


def register(request):
    """Register a new user."""
    if request.method != 'POST':
        # Display blank registration form
        form = CustomUserCreationForm()

    else:
        # Process completed form.
        form = CustomUserCreationForm(data=request.POST)

        if form.is_valid():
            new_user = form.save()
            # Login the user and redirect to the home page.
            login(request, new_user)
            return redirect('blogs:index')

    # Display a blank or invalid form.
    context = {'form': form}
    return render(request, 'registration/register.html', context)
    