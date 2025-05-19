from django.views import View
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from newsApp.models import NewsPost


def signup_view(request):
    form = UserCreationForm(request.POST)
    if form.is_valid():
        form.save()
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect("index")
    return render(request, "registration/signup.html", {"form": form})


class ProfileView(View):
    def get(self, req):
        return render(
            req,
            "accounts/profile.html",
            context={
                "user": req.user,
                "articles": NewsPost.objects.filter(reporter_id=req.user),
            },
        )


class LogoutView(View):
    def get(self, req):
        return render(req, "registration/logout.html", context={"user": req.user})
