import requests

webhook_url = "https://asia-webhook.hevodata.com/t/ru4sf57ehu"
params = {
    "event": "agents",
    "properties": [
        {"agent_name": "vishu", "agent_id": "bond007"},
        {"agent_name": "subha", "agent_id": "kkk00033"},
    ],
}
http_request = requests.post(url=webhook_url, json=params)
