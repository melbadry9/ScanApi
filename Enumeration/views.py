import multiprocessing

from django.template import loader
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from Enumeration.core.db import SubDomainData, delete_domain
from Enumeration.core.task import passive_domain, active_domain


# Create your views here.
def index(request):
    return render(request, 'Enumeration/active.html')

def db_domain(request, domain):
    subdomains = None
    if request.method == "GET":
        re_domain = SubDomainData(domain)
        re_pro = request.GET.get("pro")
        if re_pro:
            subdomains = re_domain.read_domains_scheme(re_pro)
        else:
            subdomains = re_domain.read_domains()

    return JsonResponse({
        "domain": domain,
        "sub_domains": subdomains
    })

def passive_enum_domain(request, domain):
    if request.method == "GET":
        process_passive = multiprocessing.Process(target=passive_domain, args=(domain,))
        process_passive.start()

    return JsonResponse({
        "domain": domain,
        "process_id": process_passive.pid,
        "passive": True,
        "active": False,
        })

def active_enum_domain(request, domain):
    if request.method == "GET":
        process_passive = multiprocessing.Process(target=active_domain, args=(domain,))
        process_passive.start()

    return JsonResponse({
        "domain": domain,
        "process_id": process_passive.pid,
        "passive": False,
        "active": True,
        })

def delete_db_domain(request, domain):
    if request.method == "GET":
        response = delete_domain(domain)
    
    return JsonResponse({
        "response": response
        })