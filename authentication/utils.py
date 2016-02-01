from rest_framework_jwt.utils import jwt_payload_handler

def new_payload_handler(user):
    payload = jwt_payload_handler(user)
    payload['uuid'] = user.user_uuid.__str__()
    return payload