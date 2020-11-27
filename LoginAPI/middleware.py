from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.models import AnonymousUser


def JWTAuthMiddleware(get_response):
    """
    middleware to add user to request object.
    So default django behaviour can be assumed
    """
    def middleware(request):
        auth = JWTAuthentication()
        user = None
        try:
            user = auth.authenticate(request)
            #authenticate method returns tuple of user, validated_token or none
        except Exception:
            pass
        if user is not None:
            user = user[0]
        else:
            user = AnonymousUser()
        request.user = user
        response = get_response(request)

        return response

    return middleware