from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings

from django.contrib.auth.models import update_last_login


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    @classmethod
    def get_token(cls, user, *args, **kwargs):
        token = super().get_token(user)
        ip = kwargs.get('ip', None)
        if ip:
            token['ip'] = ip
        return token

    def validate(self, attrs):
        request = self.context['request']
        ip = self.get_client_ip(request)

        data = super().validate(attrs)
        refresh = self.get_token(self.user, **{'ip': ip})

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data
