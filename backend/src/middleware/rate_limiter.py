from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

RATE_LIMITS = {
    'review': '5/minute',
    'auth': '10/minute',
    'general': '30/minute'
}
