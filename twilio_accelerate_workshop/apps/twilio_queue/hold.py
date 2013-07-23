class HoldMusicTwiml(object):
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
        {
            'id': '400',
            'uri': 'http://sms.aramael.com/static/subway.mp3',
            'time': 34,
        },
        {
            'id': '401',
            'uri': 'http://sms.aramael.com/static/winters-tale.mp3',
            'time': 30,
        },
        {
            'id': '402',
            'uri': 'http://sms.aramael.com/static/get-up.mp3',
            'time': 31,
        },
        {
            'id': '403',
            'uri': 'http://com.twilio.music.guitars.s3.amazonaws.com/Pitx_-_A_Thought.mp3',
            'time': 62,
        },
        {
            'id': '404',
            'uri': 'http://com.twilio.music.guitars.s3.amazonaws.com/Pitx_-_Long_Winter.mp3',
            'time': 103
        }
    )
    ROCK = (
        {
            'id': '500',
            'uri': 'http://com.twilio.music.rock.s3.amazonaws.com/jlbrock44_-_Apologize_Guitar_Deep_Fried.mp3',
        },
        {
            'id': '501',
            'uri': 'http://com.twilio.music.rock.s3.amazonaws.com/jlbrock44_-_Apologize_Guitar_DropC.mp3',
        },
        {
            'id': '502',
            'uri': 'http://com.twilio.music.rock.s3.amazonaws.com/nickleus_-_original_guitar_song_200907251723.mp3',
        },
    )
    SOFT_ROCK = (
        'http://com.twilio.music.soft-rock.s3.amazonaws.com/_ghost_-_promo_2_sample_pack.mp3',
        'http://com.twilio.music.soft-rock.s3.amazonaws.com/tazzista_-_Cecil_Helen_instrumental_loop_pack_105_C.mp3',
        'http://com.twilio.music.soft-rock.s3.amazonaws.com/Per_-_Joachim_-_Instrumental.mp3',
        'http://com.twilio.music.soft-rock.s3.amazonaws.com/jacksontorreal_-_The_First_Sunny_Sky.mp3',
        'http://com.twilio.music.soft-rock.s3.amazonaws.com/Fireproof_Babies_-_Melancholy_4_a_Sun-lit_day.mp3',
    )

    DEFAULT = "GUITARS"

    MUSIC_TYPES = {
        "1": "CLASSICAL",
        "2": "AMBIENT",
        "3": "ELECTRONICA",
        "4": "GUITARS",
        "5": "ROCK",
        "6": "SOFT_ROCK",
    }

    music_choice = None

    def __init__(self, default_music):

        self.DEFAULT = default_music
        self.time_elapsed = 0

    def get_music_type(self, digits):

        self.music_choice = digits

        return self.MUSIC_TYPES.get(digits, self.DEFAULT)

    def get_music(self, max_time=None, played=None):

        if played is None:
            played = []

        music_choice = self.music_choice or self.DEFAULT

        music_type = getattr(self, str(music_choice), None)

        if music_type is None:
            music_type = getattr(self, self.DEFAULT)

        for music in music_type:
            if music['id'] not in played:
                self.time_elapsed += music.get('time', 0)

                if max_time < self.time_elapsed:
                    return

                yield music
        return