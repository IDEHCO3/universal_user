
from rest_framework_jwt import utils

def new_payload_handler(user):
    payload = utils.jwt_payload_handler(user)
    payload['uuid'] = str(user.user_uuid)
    return payload
