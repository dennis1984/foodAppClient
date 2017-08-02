from django.utils.timezone import now

from Business_Users.models import BusinessUser


class BusinessUserBackend(object):
    def authenticate(self, username=None, password=None):
        try:
            user = BusinessUser.objects.get(phone=username)
        except BusinessUser.DoesNotExist:
            pass
        else:
            if user.check_password(password):
                user.last_login = now()
                user.save()
                return user
        return None

    def get_user(self, user_id):
        try:
            return BusinessUser.objects.get(pk=user_id)
        except BusinessUser.DoesNotExist:
            return None
