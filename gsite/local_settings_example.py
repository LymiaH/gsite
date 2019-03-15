from gsite.settings import *

# Generate a new key with:
# from django.core.management.utils import get_random_secret_key
# get_random_secret_key()
# Source: https://github.com/django/django/blob/d46bf119799f4d319f41d890366bc8154017b432/django/core/management/utils.py#L76
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'cinh8)xlmg16(q@6g^3mx)z&qb@qx@5zmgh4+y9i6vk)t#%xgb'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Put your actual domain here
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '[::1]',
]
