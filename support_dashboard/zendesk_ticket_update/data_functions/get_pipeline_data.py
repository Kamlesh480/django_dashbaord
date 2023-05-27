import requests
import json


def get_pipeline_tables(url, pipeline_no, cluster_name, account_name):
    url = f"{url}/tables"

    payload = json.dumps(
        {
            "pipeline_no": pipeline_no,
            "cluster_name": cluster_name,
            "account_name": account_name,
        }
    )
    headers = {"Content-Type": "application/json"}

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.text


def get_report_data(
    url, pipeline_no, cluster_name, account_name, src_objects, dest_objects
):
    url = f"{url}/data"

    payload = json.dumps(
        {
            "pipeline_no": pipeline_no,
            "cluster_name": cluster_name,
            "account_name": account_name,
            "selection": {"src_objects": src_objects, "dest_objects": dest_objects},
        }
    )
    headers = {"Content-Type": "application/json"}

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.text


# data = get_pipeline_tables()

# data = json.loads(data)
# type(data)
# data["src_objects"]
