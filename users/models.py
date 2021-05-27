from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Token(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    active = models.BooleanField(default=False)
    value = models.CharField(null=False, unique=True, max_length=50)

    @classmethod
    def validate_token(cls, token_value):
        token = cls.objects.filter(value=token_value).select_related('user').first()
        if token is None or not token.active:
            return None
        return token.user