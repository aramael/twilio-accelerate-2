from django.http import HttpResponse
from django.shortcuts import resolve_url
from django.views.decorators.csrf import csrf_exempt
from twilio import twiml


class HoldMusicComs(object):
    CLASSICAL = 'http://twimlets.com/holdmusic?Bucket=com.twilio.music.classical'
    AMBIENT = 'http://twimlets.com/holdmusic?Bucket=com.twilio.music.ambient'
    ELECTRONICA = 'http://twimlets.com/holdmusic?Bucket=com.twilio.music.electronica'
    GUITARS = 'http://twimlets.com/holdmusic?Bucket=com.twilio.music.guitars'
    ROCK = 'http://twimlets.com/holdmusic?Bucket=com.twilio.music.rock'
    SOFT_ROCK = 'http://twimlets.com/holdmusic?Bucket=com.twilio.music.soft-rock'


class HoldMusic(object):

    CLASSICAL = (
        'http://com.twilio.music.classical.s3.amazonaws.com/Mellotroniac_-_Flight_Of_Young_Hearts_Flute.mp3',
        'http://com.twilio.music.classical.s3.amazonaws.com/oldDog_-_endless_goodbye_%28instr.%29.mp3',
        'http://com.twilio.music.classical.s3.amazonaws.com/BusyStrings.mp3',
        'http://com.twilio.music.classical.s3.amazonaws.com/ClockworkWaltz.mp3',
        'http://com.twilio.music.classical.s3.amazonaws.com/ith_brahms-116-4.mp3',
        'http://com.twilio.music.classical.s3.amazonaws.com/ith_chopin-15-2.mp3',
        'http://com.twilio.music.classical.s3.amazonaws.com/MARKOVICHAMP-Borghestral.mp3',
    )
    AMBIENT = (
        'http://com.twilio.music.ambient.s3.amazonaws.com/gurdonark_-_Exurb.mp3',
        'http://com.twilio.music.ambient.s3.amazonaws.com/aerosolspray_-_Living_Taciturn.mp3',
        'http://com.twilio.music.ambient.s3.amazonaws.com/gurdonark_-_Plains.mp3',
    )
    ELECTRONICA = (
        'http://com.twilio.music.electronica.s3.amazonaws.com/spenceyb_-_O-T-S-H-T_%28Razma_World_IV_Remix%29.mp3',
        'http://com.twilio.music.electronica.s3.amazonaws.com/Kaer_Trouz_-_Seawall_Stepper.mp3',
        'http://com.twilio.music.electronica.s3.amazonaws.com/teru_-_110_Downtempo_Electronic_4.mp3',
    )
    GUITARS = (
        'http://com.twilio.music.guitars.s3.amazonaws.com/Pitx_-_A_Thought.mp3',
        'http://com.twilio.music.guitars.s3.amazonaws.com/Pitx_-_Long_Winter.mp3',
    )
    ROCK = (
        'http://com.twilio.music.rock.s3.amazonaws.com/jlbrock44_-_Apologize_Guitar_Deep_Fried.mp3',
        'http://com.twilio.music.rock.s3.amazonaws.com/jlbrock44_-_Apologize_Guitar_DropC.mp3',
        'http://com.twilio.music.rock.s3.amazonaws.com/nickleus_-_original_guitar_song_200907251723.mp3',
    )
    SOFT_ROCK = (
        'http://com.twilio.music.soft-rock.s3.amazonaws.com/_ghost_-_promo_2_sample_pack.mp3',
        'http://com.twilio.music.soft-rock.s3.amazonaws.com/tazzista_-_Cecil_Helen_instrumental_loop_pack_105_C.mp3',
        'http://com.twilio.music.soft-rock.s3.amazonaws.com/Per_-_Joachim_-_Instrumental.mp3',
        'http://com.twilio.music.soft-rock.s3.amazonaws.com/jacksontorreal_-_The_First_Sunny_Sky.mp3',
        'http://com.twilio.music.soft-rock.s3.amazonaws.com/Fireproof_Babies_-_Melancholy_4_a_Sun-lit_day.mp3',
    )

    MUSIC_TYPES = {
        "1": CLASSICAL,
        "2": AMBIENT,
        "3": ELECTRONICA,
        "4": GUITARS,
        "5": ROCK,
        "6": SOFT_ROCK,
    }

    @staticmethod
    def get_music_type(digits):
        return HoldMusic.MUSIC_TYPES.get(digits, HoldMusic.CLASSICAL)

@csrf_exempt
def add_to_queue(request):

    r = twiml.Response()

    r.say('Welcome to Acme. Industries. To change your hold music dial numbers 1 through 6.')
    r.enqueue('test_app_queue', waitUrl=resolve_url('queue_wait'))

    return HttpResponse(str(r))

@csrf_exempt
def queue_wait(request, digits=None):

    if request.POST and request.POST['Digits'] and digits is None:
        digits = request.POST['Digits']
        music_type = HoldMusic.get_music_type(digits)
    else:
        music_type = HoldMusic.CLASSICAL

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