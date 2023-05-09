import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


client = WebClient(token=os.environ["SLACK_USER_TOKEN"])


# # message to send
message = {
    "blocks": [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "Hello Guys,\nBy working together we can create a more effective and engaging training experience.\nPlease share your feedback to help us bridge gap, if there is any :\n*Trainer Feedback Form*-\nhttps://forms.gle/JvxRgUPpG4tp6Wa89\nNote: You will receive an email for the same.\nIts an anonymous form hence your ID will not be shared, feel free to share your thoughts honestly.",
            },
        }
    ]
}
recipient_emails = [
    "anu.yadav@hevodata.com",
    # "arun.sunderraj@hevodata.com",
    "chirag.agarwal@hevodata.com",
    # "dimple.mk@hevodata.com",
    # "dipak.patil@hevodata.com",
    # "geetha.n@hevodata.com",
    # "kamlesh.chhipa@hevodata.com",
    # "karthic.c@hevodata.com",
    # "madhusudhan.gaddam@hevodata.com",
    # "monica.patel@hevodata.com",
    # "mridul.juyal@hevodata.com",
    # "muskan.kesharwani@hevodata.com",
    # "nathaniel.rampur@hevodata.com",
    # "nishant.tandon@hevodata.com",
    # "nitin.birajdar@hevodata.com",
    # "prashant@hevodata.com",
    # "rohit.guntuku@hevodata.com",
    # "sai.rao@hevodata.com",
    # "sarthak.bhardwaj@hevodata.com",
    # "sasikumar.reddy@hevodata.com",
    # "satyam.agrawal@hevodata.com",
    # "sindhura.devarapalli@hevodata.com",
    # "skand.agrawal@hevodata.com",
    # "sneha.r@hevodata.com",
    # "subham.bansal@hevodata.com",
    # "sudhanshu.sharan@hevodata.com",
    # "veeresh.biradar@hevodata.com",
    # "vinita.mittal@hevodata.com",
    # "vishnu.bhargav@hevodata.com"
    "akanksha.singh@hevodata.com",
    "anmol.baunthiyal@hevodata.com",
    "madanlal.bidiyasar@hevodata.com",
    "parthiv.patel@hevodata.com",
    "pushkar.dayal@hevodata.com",
    "rahul.kumar@hevodata.com",
    "raja.pandey@hevodata.com",
    "shivanshu.dabral@hevodata.com",
    "siddhartha.chauhan@hevodata.com",
]
# recipient_emails=["skand.agrawal@hevodata.com"]
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
