from django.shortcuts import redirect, render
from employee.models import Employee
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.core.cache import cache

MAX_LOGIN_ATTEMPTS = 5
LOCKOUT_SECONDS = 300

# Create your views here.
def login_user(request):
    if request.method == "POST":
        id = request.POST["id"]
        password = request.POST["password"]

        lockout_key = f"login_lockout_{id}"
        attempts_key = f"login_attempts_{id}"

        if cache.get(lockout_key):
            messages.error(request,"Too many failed login attempts. Please try again later.")
            return redirect("/")

        user = authenticate(request,username=id,password=password)
        if user is not None:
            cache.delete(attempts_key)
            login(request , user)
            return redirect("/ems/dashboard")
        else:
            attempts = cache.get(attempts_key, 0) + 1
            cache.set(attempts_key, attempts, LOCKOUT_SECONDS)
            if attempts >= MAX_LOGIN_ATTEMPTS:
                cache.set(lockout_key, True, LOCKOUT_SECONDS)
            messages.error(request,"Invalid Credentials")
            return redirect("/")

    return render(request,"employee/Login.html")


def logout_user(request):
    logout(request)
    return redirect("/")


def signup(request):
    if request.method == "POST":
        id = request.POST["id"]
        password = request.POST["password"]
        cnfpass = request.POST["cnfpass"]

        can_register = (
            password == cnfpass
            and Employee.objects.filter(eID=id).exists()
            and not User.objects.filter(username=id).exists()
        )

        if can_register:
            user = User.objects.create_user(username=id,password=password)
            user.save()
            messages.info(request,"Registered Successfully")
        else:
            messages.info(request,"Registration failed. Please check your details and try again.")

        return redirect("/signup")

    return render(request,"employee/signup.html")