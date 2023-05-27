from django.http import HttpResponse
from django.shortcuts import render, redirect
from .data_functions.get_pipeline_data import get_pipeline_tables


def issue_analyzer(request):
    return render(request, "issue_analyzer/main.html")


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

            # data = get_pipeline_tables()
            # print("dekho vo aa gya:{}".format(data))

            # Perform any necessary processing with the form data
            # ...

            # Prepare the HTML content to be displayed in the response
            html_content = "<h2>Results</h2>"
            html_content += f"<p>Pipeline Number: {pipeline_number}</p>"
            html_content += f"<p>Cluster: {cluster}</p>"
            html_content += f"<p>Account Name: {account_name}</p>"

            # Return the rendered HTML content as the response
            return HttpResponse("get the view fcuntion boy")
        elif action == "get_internal_data":
            selected_sources = request.POST.getlist("selected_sources[]")
            selected_destinations = request.POST.getlist("selected_destinations[]")
            print(selected_sources)
            print(selected_destinations)

    # Return an empty or default response for GET requests
    return HttpResponse("get the view fcuntion boy")
