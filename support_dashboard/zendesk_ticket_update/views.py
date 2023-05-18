from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Overview, ZendeskUpdateLogs
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
import requests
from user_setting.models import AutomationCredentials, Group, TeamMember
from django.shortcuts import get_object_or_404
from slack_sdk import WebClient
import markdown


from .cred import (
    headers,
    all_custom_fields,
    load,
    base_url,
    additional_tag,
    custom_fields,
    payload,
)

from .slack_function import (
    send_message_to_recipient,
)


# Create your views here.
@login_required
def home(request):
    all_overview = Overview.objects.all()
    return render(request, "home.html", {"all_overview": all_overview})


def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        print("I got name: {} and pass: {}".format(username, password))

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            all_overview = Overview.objects.all()

            print("I got auth name: {} and auth pass: {}".format(username, password))

            auth.login(request, user)
            return redirect("home")
        else:
            messages.info(request, "Credential Invalid, Please try again!")
            return redirect("login")

    else:
        print("calling else block for login view")
        return render(request, "login.html")


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        password1 = request.POST["password1"]

        if password == password1:
            if User.objects.filter(email=email).exists():
                messages.info(request, "Email Already Used")
                return redirect("register")
            elif User.objects.filter(username=username).exists():
                messages.info(request, "Username Already Used")
                return redirect("register")
            else:
                user = User.objects.create_user(
                    username=username, email=email, password=password
                )
                user.save()
                return redirect("/")
        else:
            messages.info(request, "Password not same")
            return redirect("register")
    else:
        return render(request, "register.html")


def get_api_key_for_user_and_name(user, name):
    try:
        credentials = AutomationCredentials.objects.get(user=user, name=name)
        return credentials.api_key
    except AutomationCredentials.DoesNotExist:
        return None


def making_zendes_api_calls(request, ticket_id, custom_field, api_key_value):
    url = base_url.format(ticket_id)

    # update headers for api_key_value
    headers["Authorization"] = "Basic " + api_key_value
    tags = ""

    print("My header: {}".format(headers))

    try:
        print("Fetching ticket {}: Start".format(ticket_id))
        response = requests.request("GET", url, headers=headers)
        if response.status_code == 200:
            print("Fetching ticket {}: Done".format(ticket_id))
            data = json.loads(response.text)
            tags = data["ticket"]["tags"]
            tags.append(additional_tag)

            # Create log entry
            action = "Called GET request for {}".format(ticket_id)
            application = "update_zendesk"
            description = f"User {request.user.username} made a get request for {url}"
            ZendeskUpdateLogs.objects.create(
                user=request.user,
                action=action,
                status=response.status_code,
                description=description,
                application=application,
            )
        else:
            print(f"Failed to fetch ticket Error code: {response.status_code}")
            # Create log entry
            action = "Failed GET request for {}".format(ticket_id)
            application = "update_zendesk"
            description = f"User {request.user.username} made a get request for {url}"
            ZendeskUpdateLogs.objects.create(
                user=request.user,
                action=action,
                status=response.status_code,
                description=description,
                application=application,
            )
            return False

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return False

    load["ticket"]["tags"] = tags
    # optimze the call
    if custom_field in all_custom_fields and custom_field != "no update needed":
        load["ticket"]["custom_fields"] = custom_fields
        load["ticket"]["custom_fields"][0]["value"] = custom_field
        payload = json.dumps(load)
        # print("called if block")

    payload = json.dumps(load)
    print("Update ticket {}: Start".format(ticket_id))

    # API PUT CALL
    try:
        print("Update ticket {}: Start".format(ticket_id))
        response = requests.request("PUT", url, headers=headers, data=payload)
        if response.status_code == 200:
            print("Updating ticket {}: Done".format(ticket_id))
            # Create log entry
            action = "Called PUT request data for {}".format(ticket_id)
            application = "update_zendesk"
            description = f"User {request.user.username} made a put request for {url}"
            ZendeskUpdateLogs.objects.create(
                user=request.user,
                action=action,
                status=response.status_code,
                description=description,
                application=application,
            )
        else:
            print(
                "Updating Ticket: Failed \n Error code: {}".format(response.status_code)
            )
            # Create log entry
            action = "Falied PUT request data for {}".format(ticket_id)
            application = "update_zendesk"
            description = f"User {request.user.username} made a put request for {url}"
            ZendeskUpdateLogs.objects.create(
                user=request.user,
                action=action,
                status=response.status_code,
                description=description,
                application=application,
            )
            return False

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return False
    return True


@login_required
def update_zendesk(request):
    if request.method == "POST":
        ticket_id = request.POST.get("ticket_id")
        tag_name = request.POST.get("tag_name")
        api_key_name = request.POST.get("key_name")

        user = request.user
        api_key_value = get_api_key_for_user_and_name(user, api_key_name)
        # print("api_key_value is:{}".format(api_key_value))
        if api_key_value is not None:
            succeed = making_zendes_api_calls(
                request, ticket_id, tag_name, api_key_value
            )
            if succeed == False:
                return HttpResponse(
                    "Request failed, please recheck all the information and try again"
                )
            messages.success(
                request,
                "Ticket {} updated with tag {} and API key: {}".format(
                    ticket_id, tag_name, api_key_name
                ),
            )
        else:
            return HttpResponse("API key not found")

        return redirect("update_zendesk")
    else:
        all_api_key_names = AutomationCredentials.objects.filter(user=request.user)
        return render(
            request,
            "update_zendesk.html",
            {
                "all_custom_fields": all_custom_fields,
                "all_api_key_names": all_api_key_names,
            },
        )


def slack_message(request):
    if request.method == "POST":
        group_name = request.POST.get("group_name")
        api_key_name = request.POST.get("key_name")
        message = request.POST.get("message")

        # text into Markdown format
        message = markdown.markdown(message)
        print(group_name)
        print(api_key_name)
        print(message)

        group = get_object_or_404(Group, name=group_name, user=request.user)
        member_emails = group.members.values_list("email", flat=True)
        print(member_emails)

        user = request.user
        api_key_value = get_api_key_for_user_and_name(user, api_key_name)

        # calling slack functions
        # try:
        #     client = WebClient(token=api_key_value)
        # except:
        #     return HttpResponse("API key not found")
        # send_message_to_recipient(client, message, member_emails)

        return redirect("slack_message")

    else:
        all_groups = Group.objects.filter(user=request.user)
        all_api_key_names = AutomationCredentials.objects.filter(user=request.user)
        return render(
            request,
            "slack_message.html",
            {
                "all_groups": all_groups,
                "all_api_key_names": all_api_key_names,
            },
        )
