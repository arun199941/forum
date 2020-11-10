from django.shortcuts import *
from community.models import  Community



def search(request):
    query = request.GET['q']
    if  Community.objects.filter(name__contains=query):
        comm_details = Community.objects.filter(name__contains=query)
        params ={
            "comms": comm_details,
            "query": query
        }
        return render(request, 'results.html',params)
    else:
        return render(request, 'results.html',{'query': query})


