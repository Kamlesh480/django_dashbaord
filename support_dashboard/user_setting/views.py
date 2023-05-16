from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import AutomationCredentials
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from .models import UsersLogs, TeamMember, Group
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.http import JsonResponse


# from .cred import all_members


@login_required
def settings(request):
    if request.method == "POST":
        if "add_key" in request.POST:
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

            # save credential to database
            credential.save()

            # Create log entry
            action = "Added new API key"
            description = (
                f"User {request.user.username} added a new key with key name: {name}"
            )
            UsersLogs.objects.create(
                user=request.user, action=action, description=description
            )

        elif "delete_key" in request.POST:
            # get credential ID from form
            name = request.POST["name"]
            credential_id = request.POST["credential_id"]

            # delete credential from database
            AutomationCredentials.objects.filter(id=credential_id).delete()

            # Create log entry
            action = "API key Deleted"
            description = (
                f"User {request.user.username} Deleted a api key with key-name:{name}"
            )
            UsersLogs.objects.create(
                user=request.user, action=action, description=description
            )

        # redirect to success page
        request.session["previous_url"] = request.META.get("HTTP_REFERER")
        return HttpResponseRedirect(request.session["previous_url"])

    else:
        credentials_list = AutomationCredentials.objects.filter(user=request.user)
        all_groups = Group.objects.filter(user=request.user)
        all_members = TeamMember.objects.all()

        # if request method is not POST, render the form
        return render(
            request,
            "user_settings.html",
            {
                "credentials_list": credentials_list,
                "all_members": all_members,
                "all_groups": all_groups,
            },
        )


# use the csrf_exempt decorator on your view function to allow cross-site requests
@csrf_exempt
def old_create_group(request, selected_members, group_name):
    selected = TeamMember.objects.filter(id__in=selected_members)
    print(selected)

    user = request.user
    print("User:{}".format(user))

    new_group = Group(name=group_name, user=user)
    new_group.save()

    new_group.members.set(selected_members)


def create_group(request, selected_members, group_name):
    selected = TeamMember.objects.filter(id__in=selected_members)
    print(selected)

    user = request.user
    print("User: {}".format(user))

    # Check if a group with the same name already exists
    existing_group = Group.objects.filter(name=group_name).exists()
    if existing_group:
        messages.info(
            request, "Group already exists with the name '{}'".format(group_name)
        )
    else:
        new_group = Group(name=group_name, user=user)
        new_group.save()

        new_group.members.set(selected_members)
        messages.success(
            request,
            "Group '{}' created successfully".format(group_name),
        )


@login_required
@csrf_protect
def settings_fun_calls(request):
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "create_group":
            selected_members = request.POST.getlist("selected_members")
            group_name = request.POST.get("group_name")
            print(selected_members)
            print(group_name)
            # create_group(request, selected_members, group_name)

            result = selected_members

            return redirect("settings")

            # return HttpResponse(result)
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
