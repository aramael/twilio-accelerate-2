"""
Django views for twilio_accelerate_workshop project.

"""

from django.http import HttpResponseNotFound, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from twilio import twiml


def home(request):
    """    Display the Landing Page    """

    context = {}

    return render(request, '', context)

@csrf_exempt
def twilio_fallback(request, fallback_type):

    if fallback_type not in ('voice', 'sms'):
        return HttpResponseNotFound('Sorry Unable to Fallback')

    print request.POST

    r = twiml.Response()
    if fallback_type == 'voice':
        r.say("Our Application is Unavailable at this time, a representative will call you back shortly.")
    else:
        r.sms("Our Application is Unavailable at this time, a representative will call you back shortly.")

    return HttpResponse(str(r))