from rest_framework import serializers
from ..models.account import Account, Token

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=12)
    password = serializers.CharField(max_length=12)

    