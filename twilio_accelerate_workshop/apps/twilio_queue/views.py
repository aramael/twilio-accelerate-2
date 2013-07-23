from django.http import HttpResponse
from django.shortcuts import resolve_url
from django.views.decorators.csrf import csrf_exempt
from twilio import twiml
from .hold import HoldMusic

@csrf_exempt
def add_to_queue(request):

    r = twiml.Response()

    r.say('Welcome to Acme. Industries. To change your hold music dial numbers 1 through 6.')
    r.enqueue('test_app_queue', waitUrl=resolve_url('queue_wait'))

    return HttpResponse(str(r))

@csrf_exempt
def queue_wait(request, digits=None, music_type=HoldMusic.CLASSICAL, hold_music=HoldMusic):

    if request.POST and request.POST['Digits'] and digits is None:
        digits = request.POST['Digits']
        music_type = hold_music.get_music_type(digits)

    r = twiml.Response()

    with r.gather(numDigits='1') as g:
        for music in music_type:
            g.play(music)

    if digits is None:
        r.redirect(resolve_url('queue_wait'))
    else:
        r.redirect(resolve_url('queue_wait_music_explicit', music_type=digits))

    return HttpResponse(str(r))

@csrf_exempt
def remove_from_queue(request):

    r = twiml.Response()

    r.say('You are being connected to our first available representative.')

    return HttpResponse(str(r))

@csrf_exempt
def agent_remove_from_queue(request):

    r = twiml.Response()
    with r.dial() as d:
        d.queue('DefaultQueue', url=resolve_url('remove_from_queue'))

    return HttpResponse(str(r))