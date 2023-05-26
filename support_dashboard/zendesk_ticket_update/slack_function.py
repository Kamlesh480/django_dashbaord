from slack_sdk.errors import SlackApiError


def get_recipient_ids(client, recipient_emails):
    recipient_ids = []
    for recipient_email in recipient_emails:
        try:
            response = client.users_lookupByEmail(email=recipient_email)
            recipient_ids.append(response["user"]["id"])
            print(f"The user ID for {recipient_email} is {response['user']['id']}")
        except SlackApiError as e:
            print("Error:", e)

    return recipient_ids


def send_message_to_recipient(client, message, recipient_emails):
    recipient_ids = get_recipient_ids(client, recipient_emails)

    for recipient_id in recipient_ids:
        try:
            # call the conversations.open method using the WebClient to open a DM channel with the recipient
            response = client.conversations_open(users=recipient_id)
            dm_channel_id = response["channel"]["id"]

            # call the chat.postMessage method using the WebClient to send the message to the DM channel
            response = client.chat_postMessage(channel=dm_channel_id, **message)
            print(f"Message sent to user {recipient_id}: {response['ts']}")
        except SlackApiError as e:
            print(f"Error sending message to user {recipient_id}: {e}")
