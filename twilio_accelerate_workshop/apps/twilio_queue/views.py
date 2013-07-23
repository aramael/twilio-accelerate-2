from django.shortcuts import resolve_url
from twilio import twiml
from django.conf import settings
from .hold import HoldMusic
from twilio_accelerate_workshop.wrappers import twilio
from twilio_accelerate_workshop.shortcuts import redirect_url as url_with_get


@twilio
def add_to_queue(request):

    r = twiml.Response()

    r.say('Welcome to Acme Industries. To change your hold music dial numbers 1 through 6.')

    if request.POST and request.POST.get('From', None) and request.POST['From'] in settings.PRIORITY_PHONE_NUMBERS:
        queue = 'PriorityQueue'
    else:
        queue = 'DefaultQueue'

    wait_url = url_with_get(resolve_url(queue_wait), queue=queue)

    r.enqueue(queue, waitUrl=wait_url)

    return r

@twilio
def queue_wait(request, digits=None, default_music="GUITARS", hold_music=HoldMusic):

    # Instantiate Hold Music Object
    hold_music = hold_music(default_music=default_music)

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

    queue_position = request.POST.get('QueuePosition', None)
    queue_wait_time = request.POST.get('AvgQueueTime', None)

    if queue_position and queue_wait_time:

        queue_wait_time = int(queue_wait_time) / 60

        r.say('We appreciate your feedback you are number ' + queue_position + ' in queue. You '
              'are probably going to wait ' + str(queue_wait_time) + ' minutes')

    # Load Up Play Music
    played = request.GET.get('played', [])

    if isinstance(played, basestring):
        played = played.split(',')

    with r.gather(numDigits='1', action=resolve_url('queue_wait')) as g:
        for music in hold_music.get_music(max_time=40, played=played):
            played.append(music['id'])
            g.play(music['uri'])

    # Add Played to Queue List
    redirect_url = url_with_get(redirect_url, played=played)

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