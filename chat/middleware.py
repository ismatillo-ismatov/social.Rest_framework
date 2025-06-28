from urllib.parse import parse_qs
from channels.middleware import BaseMiddleware
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async
from watchfiles import awatch


@database_sync_to_async
def get_user_from_token(token_key):
    try:
        token = Token.objects.get(key=token_key)
        return token.user
    except Token.DoesNotExist:
        return AnonymousUser()


# class JWTAuthMiddleware(BaseMiddleware):
#     async def __call__(self, scope, receive,send):
#         query_string = scope['query_string'].decode()
#         token = parse_qs(query_string).get('token')
#         if token:
#             scope['user'] = await get_user(token[0])
#         else:
#             scope['user'] = AnonymousUser()
#         return await super().__call__(scope,receive,send)




class TokenAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        query_string = scope["query_string"].decode()
        token = parse_qs(query_string).get('token')
        if token:
                scope["user"] = await get_user_from_token(token[0])
        else:
            scope["user"] = AnonymousUser()
        return await super().__call__(scope,receive,send)

