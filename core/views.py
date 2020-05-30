import json
import threading

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from services import vk as vk_app

@csrf_exempt
def vk(request):
    rq = json.loads(request.body, encoding="utf-8")

    if rq['type'] != "confirmation":
        x = threading.Thread(target=vk_app.Vk, args=(request,))
        x.start()
        return HttpResponse("ok", status=200)
    else: return HttpResponse("3dac7805")
