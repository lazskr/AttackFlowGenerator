"""Views for user-related functionality."""
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm  # add this
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from .forms import NewUserForm

# Create your views here.


def register_request(request):
    """View for user registration."""
    if request.method == "POST":
        form = NewUserForm(request.POST)
        email = request.POST["email"]
        if form.is_valid() and not User.objects.filter(email=email).exists():
            user = form.save()
            login(request, user)
            return redirect("/")
        else:
            messages.error(request, "Unsuccessful registration; see reasons below: ")
            if User.objects.filter(email=email).exists():
                messages.error(request, "• Email already exists")
            for _, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"• {error}")
    else:
        form = NewUserForm()
    return render(request, "users/registration.html", context={"register_form": form})


def login_request(request):
    """View for user login."""
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # messages.info(request, f"You are now logged in as {username}.")
                next_url = request.GET.get("next")
                if next_url:
                    return redirect(next_url)
                else:
                    return redirect("/")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request, "users/login.html", context={"login_form": form})


def logout_request(request):
    """View for logging out."""
    logout(request)
    # messages.info(request, "You have successfully logged out.")
    return redirect("/")
