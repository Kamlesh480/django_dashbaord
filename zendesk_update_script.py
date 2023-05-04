import requests
import json
from credentials import (
    headers,
    all_custom_fields,
    load,
    base_url,
    additional_tag,
    custom_fields,
    payload,
)


while True:
    try:
        ticket_id = int(input("Enter an ticket ID: "))
        break
    except ValueError:
        print("Oops! That was not a valid integer. Please try again...")


while True:
    print(
        "Enter a number between 1 and {} to select a custom field:".format(
            len(all_custom_fields)
        )
    )
    for index, field in enumerate(all_custom_fields):
        print("{}. {}".format(index, field))

    selection = input()

    if not selection.isdigit():
        print("Oops! That was not a valid number. Please try again...")
    elif int(selection) < 0 or int(selection) >= len(all_custom_fields):
        print("Oops! Number not in range. Please try again...")
    elif selection == "" or selection == str(0):
        custom_field = None
        print("You have selected: Other")
        break
    else:
        custom_field = all_custom_fields[int(selection)]
        print("You have selected: {}".format(custom_field))
        break


url = base_url.format(ticket_id)
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
print("Update ticket {}: Start".format(ticket_id))


# API PUT CALL
try:
    print("Update ticket {}: Start".format(ticket_id))
    response = requests.request("PUT", url, headers=headers, data=payload)
    if response.status_code == 200:
        print("Updating ticket {}: Done".format(ticket_id))
    else:
        print("Updating Ticket: Failed \n Error code: {}".format(response.status_code))
except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
