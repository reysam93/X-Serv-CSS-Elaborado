from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseNotFound
from models import Page


def addPage(name, content):
    try:
        newPage = Page.objects.get(name=name)
        newPage.page = content
    except Page.DoesNotExist:
        newPage = Page(name = name, page = content)
    newPage.save()


@csrf_exempt
def processCmsRequests(request, resource):
    if request.method == 'GET':
        try:
            page = '<link rel="stylesheet" href="/css/main.css" +\
                type="text/css" /> <html>'
            page += '<body>' + Page.objects.get(name = resource).page
            page += '</body></html>'
            return HttpResponse(page)
        except Page.DoesNotExist:
            return HttpResponseNotFound("Page not found")
    elif request.method == 'PUT':
        addPage(resource, request.body)
        return HttpResponse("Added to the list")
    else:
        return HttpResponse(status=403)


@csrf_exempt
def processCSS(request, resource):
    if request.method == 'GET':
        try:
            css = Page.objects.get(name = resource)
            return HttpResponse(css.page, content_type="text/css")
        except Page.DoesNotExist:
            return HttpResponseNotFound("Page not found")
    elif request.method == 'PUT':
        addPage(resource, request.body)
        return HttpResponse("Added to the list")
    else:
        return HttpResponse(status=403)
