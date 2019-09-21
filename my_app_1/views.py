from django.http import HttpResponse
from django.shortcuts import render
import operator
from .mp_finder import Mp, send_email

def index(request):
    #context = {"context_variable": context_variable}
    return render(request, 'index.html')

def count(request):
    fulltext = request.GET['fulltext']
    x = Mp(fulltext)
    try:
        x.find_constituency()
        x.find_mp_parliament_address()
        x.find_extract_mp_details()
        x.find_bio_page()
        x.find_email_address()
        x.find_constituant_address()
    except:
        paven = "paven"

    mp_name = x.name
    mp_email = x.email
    mp_twitter = "joe.blogs69"
    constituency = x.constituency

    send_email()

    return render(request,'output.html', {'postcode':fulltext, 'mp_name':mp_name, 'constituency':constituency, 'mp_email':mp_email, })