from rest_framework import serializers
from users.models import User

class UserAutheticationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('user_uuid', 'username', 'first_name')