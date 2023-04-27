from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Overview
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
import requests
from user_setting.models import AutomationCredentials


from .cred import (
    headers,
    all_custom_fields,
    load,
    base_url,
    additional_tag,
    custom_fields,
    payload,
)


# Create your views here.
@login_required(login_url="/login/")
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


@login_required
def update_zendesk(request):
    all_api_key_names = AutomationCredentials.objects.filter(user=request.user)
    return render(
        request,
        "update_zendesk.html",
        {
            "all_custom_fields": all_custom_fields,
            "all_api_key_names": all_api_key_names,
        },
    )


def get_api_key_for_user_and_name(user, name):
    try:
        credentials = AutomationCredentials.objects.get(user=user, name=name)
        return credentials.api_key
    except AutomationCredentials.DoesNotExist:
        return None


def making_zendes_api_calls(ticket_id, custom_field, api_key_value):
    url = base_url.format(ticket_id)

    # update headers for api_key_value

    try:
        print("Fetching ticket {}: Start".format(ticket_id))
        response = requests.request("GET", url, headers=headers)
        if response.status_code == 200:
            print("Fetching ticket {}: Done".format(ticket_id))
            data = json.loads(response.text)
            tags = data["ticket"]["tags"]
            tags.append(additional_tag)
        else:
            print(f"Failed to fetch ticket Error code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

    load["ticket"]["tags"] = tags
    # optimze the call
    if custom_field in all_custom_fields:
        load["ticket"]["custom_fields"] = custom_fields
        load["ticket"]["custom_fields"][0]["value"] = custom_field
        payload = json.dumps(load)

    else:
        payload = json.dumps(load)
        print("Update ticket {}: Start".format(ticket_id))

    return payload


def call_zendesk_api(request):
    if request.method == "POST":
        ticket_id = request.POST.get("ticket_id")
        tag_name = request.POST.get("tag_name")
        api_key_name = request.POST.get("api_key_name")

        # Call API with ticket_id and tag_name
        print(
            "get the values: {} and {} and api_token_name: {}".format(
                ticket_id, tag_name, api_key_name
            )
        )
        user = request.user
        api_key_value = get_api_key_for_user_and_name(user, api_key_name)
        print("api_key_value is:{}".format(api_key_value))
        if api_key_value is not None:
            # payload = making_zendes_api_calls(ticket_id, tag_name, api_key_value)
            # print("payload is {}".format(payload))

            messages.success(
                request,
                "Ticket {} updated with tag {} and API key".format(ticket_id, tag_name),
            )
        else:
            return HttpResponse("API key not found")

        # return a success response
        # return JsonResponse({"status": "success"})
        return redirect("update_zendesk")

    else:
        # Render form
        print("Sorry hogya")

        # return a form response
        return render(request, "update_form.html", {})
