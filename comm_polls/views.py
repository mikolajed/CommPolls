from django.shortcuts import render

def index(request):
    return render(request, "comm_polls/index.html")
