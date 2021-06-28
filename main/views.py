from django.shortcuts import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from .models import Shortener
from django.forms.models import model_to_dict
import json


def create(request):
    if request.method == 'POST':
        try:
            full_url = json.loads(request.body)['url']
            shortener = Shortener.objects.create(full_url=full_url)
        except Exception as e:
            return HttpResponse('Error creating shortener - {0}'.format(e), status=400)
        dict_obj = model_to_dict(shortener)
        return JsonResponse(dict_obj, status=201)
    else:
        return HttpResponse('Method {0} not allowed'.format(request.method), status=400)


def redirect_to_full_url(request, short_url):
    if request.method == 'GET':
        try:
            shortener = Shortener.objects.get(short_url=short_url)
            shortener.counter += 1
            shortener.save()
            return HttpResponseRedirect(shortener.full_url)
        except Exception as e:
            return HttpResponse('Not found - {0}'.format(e), status=404)
    else:
        return HttpResponse('Method {0} not allowed'.format(request.method), status=400)


