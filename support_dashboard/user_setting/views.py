from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import AutomationCredentials


@login_required
def user_settings(request):
    # Get the credentials for the current user
    creds = AutomationCredentials.objects.filter(user=request.user)
    # Pass the credentials to the template
    return render(request, "user_settings.html", {"credentials": creds})


@login_required
def add_credentials(request):
    if request.method == "POST":
        # get data from form
        name = request.POST["name"]
        description = request.POST["description"]
        username = request.POST["username"]
        api_key = request.POST["api_key"]

        # create new credential object
        credential = AutomationCredentials(
            user=request.user,
            name=name,
            description=description,
            username=username,
            api_key=api_key,
        )
        print("wow we have our API cred: {}".format(credential))
        # save credential to database
        credential.save()

        # redirect to success page
        return redirect("user_settings")

    else:
        # if request method is not POST, render the form
        return render(request, "user_settings.html")
