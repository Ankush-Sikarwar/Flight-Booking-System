from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from home import views
from accounts.models import User
from accounts.EmailBackEnd import EmailBackEnd
from django.views.generic import UpdateView
from django.urls import reverse_lazy
from accounts.forms import EditProfileFrom


def profile(request):
    return render(request, "profile.html")


class UserEditView(UpdateView):
    form_class = EditProfileFrom
    template_name = "edit_profile.html"
    success_url = reverse_lazy("profile")

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy("profile")


def handelSingup(request):
    if request.method == "POST":
        # Get the post parameters
        username = request.POST["username"]
        fname = request.POST["fname"]
        lname = request.POST["lname"]
        email = request.POST["email"]
        phone_number = request.POST["phone_number"]
        pass1 = request.POST["pass1"]
        pass2 = request.POST["pass2"]

        # check for errorneous input
        if pass1 != pass2:
            messages.error(request, "Password do not match.")
            return redirect("handelSingup")

        # Create User
        try:
            myuser = User.objects.create_user(
                username=username,
                password=pass1,
                email=email,
                first_name=fname,
                last_name=lname,
                phone_number=phone_number,
            )
            # myuser.is_active = False
            myuser.save()

            # after registration login user
            login(request, myuser)
            # print("here")
            messages.success(request, "Account Created Successfully!")
            return redirect(views.homeView)

        except Exception as e:
            print(e)
            messages.error(request, "Failed to SignUp!")
            return redirect(views.homeView)
    else:
        return HttpResponse("404 - Not Found")


def handleLogin(request):
    if request.method != "POST":
        return HttpResponse("Submission outside this window is not allowed 😎")
    else:
        # Get the post parameters
        loginusername = request.POST["loginusername"]
        loginpassword = request.POST["loginpassword"]
        # user = EmailBackEnd.authenticate(
        #     request, username=loginusername, password=loginpassword
        # )
        user = EmailBackEnd.authenticate(
            request, username=loginusername, password=loginpassword
        )
        if user is not None:
            login(request, user)
            messages.success(request, "Successfuly logged in 🥰")
            return redirect(views.homeView)
        else:
            messages.error(request, "Invalid credentialsl, Please try again 😎")
            return redirect(views.homeView)


def handleLogout(request):
    if request.method == "POST":
        value = request.POST["value"]
        logout(request)
        response = redirect(views.homeView)
        print(response)
        for cookie in request.COOKIES:
            response.delete_cookie(cookie)

        messages.success(request, "Successfuly logged out 🥰")
        return response

    else:
        return HttpResponse("Sorry No Users Logged in 😎")
