import logging

logger = logging.getLogger(__name__)

from django.urls import re_path, path
from . import consumer
from product import consumer as con
from seller import consumer as sel

websocket_urlpatterns = [
    path('', consumer.HomeConsumer.as_asgi()),
    path('product/<int:pk>/', con.ProductConsumer.as_asgi()),
    path('users/chat/<str:pk>/', sel.UserChat.as_asgi()),
]

logger.info('routing conf is loaded')