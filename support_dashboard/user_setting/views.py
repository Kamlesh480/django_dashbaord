from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import AutomationCredentials


@login_required
def user_settings(request):
    if request.method == "POST":
        # get data from form
        name = request.POST["name"]
        description = request.POST["description"]
        api_key = request.POST["api_key"]

        # create new credential object
        credential = AutomationCredentials(
            user=request.user,
            name=name,
            description=description,
            api_key=api_key,
        )
        print("wow we have our API cred: {}".format(credential))
        # save credential to database
        credential.save()

        # redirect to success page
        return redirect("user_settings")

    else:
        credentials_list = AutomationCredentials.objects.filter(user=request.user)

        # if request method is not POST, render the form
        return render(
            request, "user_settings.html", {"credentials_list": credentials_list}
        )


def get_api_key_for_user_and_name(user, name):
    try:
        credentials = AutomationCredentials.objects.get(user=user, name=name)
        return credentials.api_key
    except AutomationCredentials.DoesNotExist:
        return None


@login_required
def settings_fun_calls(request):
    if request.method == "POST":
        action = request.POST.get("update_zendesk")
        param1 = request.POST.get("param1")
        # call the appropriate function based on the value of `action`
        if action == "update_zendesk":
            user = request.user
            api_key_name = action
            api_key_value = get_api_key_for_user_and_name(user, api_key_name)
            result = api_key_value if api_key_value is not None else "API key not found"
            return HttpResponse(result)
        elif action == "function2":
            # result = function2()
            pass
        else:
            result = "Unknown action"
        return HttpResponse(result)
    else:
        # handle GET requests
        # render the form
        return render(request, "ui.html")