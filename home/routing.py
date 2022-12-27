import logging

logger = logging.getLogger(__name__)

from django.urls import re_path, path
from . import consumer
from product import consumer as con

websocket_urlpatterns = [
    path('product/<int:id>/', con.ProductConsumer.as_asgi()),
    path('', consumer.HomeConsumer.as_asgi()),

    #re_path(r'^product/(?P<pk>\d+)/$', con.ProductConsumer.as_asgi()),
    #re_path(r'^$', consumer.HomeConsumer.as_asgi()),
]

logger.info('routing conf is loaded')
print('this is url patterns {}'.format(websocket_urlpatterns))