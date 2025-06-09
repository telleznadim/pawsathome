from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, 'Account created successfully. You can now log in.')
            return redirect('login')  # Make sure you have a url named 'login'
    else:
        form = UserCreationForm()

    return render(request, 'accounts/register.html', {'form': form})


# Create your views here.
