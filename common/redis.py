# coding: utf-8
from redis import StrictRedis
from django.conf import settings
host = settings.REDIS_HOST
port = settings.REDIS_PORT
# rds = StrictRedis(**settings.REDIS_CONF)
rds = StrictRedis(host=host, port=port)

