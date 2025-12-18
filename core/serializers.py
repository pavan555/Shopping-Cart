from djoser.serializers import UserCreateSerializer as DjoserUserCreateSerializer, UserSerializer as DjoserUserSerializer
from django.conf import settings
from .models import User

class UserCreateSerializer(DjoserUserCreateSerializer):
    
    class Meta(DjoserUserCreateSerializer.Meta):
        fields = tuple(User.REQUIRED_FIELDS) + (
            "id",
            "username",
            "password",
            'first_name',
            'last_name',
        )

class UserSerializer(DjoserUserSerializer):
    class Meta(DjoserUserCreateSerializer.Meta):
        fields = tuple(User.REQUIRED_FIELDS) + (
            "id",
            "username",
            'first_name',
            'last_name',
        )
        read_only_fields = ("username", "email")