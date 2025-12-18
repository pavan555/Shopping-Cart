from djoser.serializers import UserCreateSerializer as DjoserUserCreateSerializer
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