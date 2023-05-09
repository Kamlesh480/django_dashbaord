import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# set up the Slack API client with your bot token


from credentials import recipient_emails, message, SLACK_USER_TOKEN, SLACK_BOT_TOKEN

client = WebClient(token=SLACK_USER_TOKEN)


recipient_ids = []
for recipient_email in recipient_emails:
    try:
        response = client.users_lookupByEmail(email=recipient_email)
        recipient_ids.append(response["user"]["id"])
        print(f"The user ID for {recipient_email} is {response['user']['id']}")
    except SlackApiError as e:
        print("Error:", e)


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
