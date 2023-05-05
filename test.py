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


def making_zendes_api_calls(ticket_id, custom_field, api_key_value):
    url = base_url.format(ticket_id)

    # update headers for api_key_value
    headers["Authorization"] = "Basic " + api_key_value
    tags = ""
    # load = load

    print("My header: {}".format(headers))

    try:
        print("Fetching ticket {}: Start".format(ticket_id))
        response = requests.request("GET", url, headers=headers)
        print(url)
        print(headers)

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
    if custom_field in all_custom_fields and custom_field != "no update needed":
        load["ticket"]["custom_fields"] = custom_fields
        load["ticket"]["custom_fields"][0]["value"] = custom_field
        # print("called if block")

    payload = json.dumps(load)
    print("Update ticket {}: Start".format(ticket_id))
    print("pyload----------------------")
    print(payload)
    print("----------------------pyload")

    # # API PUT CALL
    try:
        print("Update ticket {}: Start".format(ticket_id))
        response = requests.request("PUT", url, headers=headers, data=payload)
        if response.status_code == 200:
            print("Updating ticket {}: Done".format(ticket_id))

        else:
            print(
                "Updating Ticket: Failed \n Error code: {}".format(response.status_code)
            )

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
