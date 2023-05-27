import requests
import json


def get_pipeline_tables():
    url = "https://shades-pledge-lawyers-surf.trycloudflare.com/tables"

    payload = json.dumps(
        {"pipeline_no": 1, "cluster_name": "us", "account_name": "breacking code"}
    )
    headers = {"Content-Type": "application/json"}

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.text


# data = get_pipeline_tables()

# data = json.loads(data)
# type(data)
# data["src_objects"]
