from rest_framework.authentication import SessionAuthentication

from codinglife import settings
from user.models import User


class UserAuthentication(SessionAuthentication):
    def authenticate(self, request):
        uid = request.session.get('uid')
        if not uid:
            return None

        user = User.objects.get(pk=uid)
        if not user:
            return None

        # if settings.CSRF_ENABLE:
        #     self.enforce_csrf(request)
        return (user, None)
