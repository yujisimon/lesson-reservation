# https://qiita.com/kaki-m/items/0991d718212912a3808f
# DjangoのCustomUserModelでログインができないバグを解消した
# pyc110カスタムUser関係.doc

from django.contrib.auth.backends import BaseBackend
from .models import CustomUser

class CustomUserBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        print('$$$$$ CustomUserBackend $$$$',username, 'password', password, 'kwargs', kwargs, '$$$$')
        # $$$$$ CustomUserBackend $$$$ taro password jirojiro kwargs {} $$$$ ログイン画面で打ち込んだデータのまま
        try:
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            return None

        if user.check_password(password):
            return user

        return None
