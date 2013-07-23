from django.shortcuts import resolve_url
from twilio import twiml
from .hold import HoldMusic
from twilio_accelerate_workshop.wrappers import twilio
from django.conf import settings

@twilio
def add_to_queue(request):

    r = twiml.Response()

    r.say('Welcome to Acme Industries. To change your hold music dial numbers 1 through 6.')

    if request.POST and request.POST.get('From', None) and request.POST['From'] in settings.PRIORITY_PHONE_NUMBERS:
        queue = 'PriorityQueue'
    else:
        queue = 'Default'

    r.enqueue(queue, waitUrl=resolve_url('queue_wait')+'?queue='+queue)

    return r

@twilio
def queue_wait(request, digits=None, music_type=HoldMusic.CLASSICAL, hold_music=HoldMusic):

    hold_music = hold_music()

    # Set Music URL
    if request.POST and request.POST.get('Digits', None) and digits is None:
        digits = request.POST['Digits']
        music_type = hold_music.get_music_type(digits)

    # Create Digits URL
    if digits is None:
        redirect_url = resolve_url('queue_wait')
    else:
        redirect_url = resolve_url('queue_wait_music_explicit', music_type=digits)

    r = twiml.Response()

    with r.gather(numDigits='1', action=resolve_url('queue_wait')) as g:
        for music in music_type:
            g.play(music)

    r.redirect(redirect_url)

    return r

@twilio
def remove_from_queue(request):

    r = twiml.Response()

    r.say('You are being connected to our first available representative.')

    return r

@twilio
def agent_remove_from_queue(request):

    r = twiml.Response()
    with r.dial() as d:
        d.queue('PriorityQueue', url=resolve_url('remove_from_queue'))
        d.queue('DefaultQueue', url=resolve_url('remove_from_queue'))

    return r