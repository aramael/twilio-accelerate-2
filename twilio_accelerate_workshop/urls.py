from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()


queue_urlpatterns = patterns('twilio_accelerate_workshop.apps.twilio_queue.views',
    url(r'^add/$', 'add_to_queue', name='add_to_queue'),
    url(r'^wait/$', 'queue_wait', name='queue_wait'),
    url(r'^wait/(?P<music_type>\d+)$', 'queue_wait', name='queue_wait_music_explicit'),
    url(r'^dequeue/$', 'remove_from_queue', name='remove_from_queue'),
    url(r'^agent/$', 'agent_remove_from_queue', name='agent_remove_from_queue'),
)

urlpatterns = patterns('twilio_accelerate_workshop',
    url(r'^$', 'views.home', name='home'),
    url(r'^twilio/(?P<fallback_type>\w+)/fallback$', 'views.twilio_fallback', name='home'),
    url(r'^queue/', include(queue_urlpatterns)),
    url(r'^admin/', include(admin.site.urls)),
)