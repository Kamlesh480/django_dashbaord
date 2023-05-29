from django.http import HttpResponse
from django.shortcuts import render, redirect
from .data_functions.get_pipeline_data import get_pipeline_tables, get_report_data
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt

url = "https://chair-crude-shuttle-vendors.trycloudflare.com"


def issue_analyzer(request):
    return render(request, "issue_analyzer/main.html")


def get_pipeline_detail2(request):
    return render(request, "ui.html")


@csrf_exempt
def get_pipeline_detail(request):
    if request.method == "POST":
        action = request.POST.get("action")

        if action == "get_tables":
            pipeline_number = request.POST.get("pipelineNumber")
            cluster = request.POST.get("cluster")
            account_name = request.POST.get("accountName")

            print(pipeline_number)
            print(cluster)
            print(account_name)
            print(action)

            data = get_pipeline_tables(url, pipeline_number, cluster, account_name)
            data = json.loads(data)

            srcObjects = data["src_objects"]
            destObjects = data["dest_objects"]

            response_data = {
                "src_objects": srcObjects,
                "dest_objects": destObjects,
            }

            return JsonResponse(response_data)

            # return HttpResponse("get the view fcuntion boy")
        elif action == "get_internal_data":
            selected_sources = request.POST.getlist("selected_sources[]")
            selected_destinations = request.POST.getlist("selected_destinations[]")
            pipelineNumber = request.POST.getlist("pipelineNumber")
            cluster = request.POST.getlist("cluster")
            accountName = request.POST.getlist("accountName")

            print(url)
            print(pipelineNumber[0])
            print(cluster[0])
            print(accountName[0])
            print(selected_sources)
            print(selected_destinations)

            data = get_report_data(
                url,
                pipelineNumber[0],
                cluster[0],
                accountName[0],
                selected_sources,
                selected_destinations,
            )
            data = json.loads(data)
            # print(data)

            connector_task = data["connector_task"]
            handyman_connector_poll = data["handyman_connector_poll"]
            handyman_copy_job = data["handyman_copy_job"]
            sideline = data["sideline"]
            sink = data["sink"]
            integration = data["integration"]
            grafana = data["grafana"]

            response_data = {
                "connector_task": connector_task,
                "handyman_connector_poll": handyman_connector_poll,
                "handyman_copy_job": handyman_copy_job,
                "sideline": sideline,
                "sink": sink,
                "integration": integration,
                "grafana": grafana,
            }

            return JsonResponse(response_data)

        elif action == "reply_sideline_file":
            print("in sideline view")
            schema_name = request.POST.get("rowData[schema_name]")
            stage = request.POST.get("rowData[stage]")
            code = request.POST.get("rowData[code]")
            pipelineNumber = request.POST.get("pipelineNumber")
            print(schema_name)
            print(stage)
            print(code)
            print(pipelineNumber)
            return HttpResponse("Replyed the events")

    # Return an empty or default response for GET requests
    return HttpResponse("get the view fcuntion boy")
