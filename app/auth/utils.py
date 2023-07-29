from datetime import datetime, timedelta

import jwt

JWT_SECRET = 'meowmeow'  # секретное слово для подписи
JWT_ACCESS_TTL = 60 * 5  # время жизни access токена в секундах (5 мин)
JWT_REFRESH_TTL = 3600 * 24 * 7  # время жизни refresh токена в секундах (неделя)


def create_jwt_token(user_id: int):
    access_payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(seconds=JWT_ACCESS_TTL),
        'type': 'access'
    }
    access = jwt.encode(payload=access_payload, key=JWT_SECRET)

    refresh_payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(seconds=JWT_REFRESH_TTL),
        'type': 'refresh'
    }
    refresh = jwt.encode(payload=refresh_payload, key=JWT_SECRET)

    return {
        'access': access,
        'refresh': refresh,
    }

