from rest_framework import serializers
from .models import User

class UserCreateSerializer(serializers.ModelSerializer):

    def save(self, **kwargs):
        password = self.validated_data['password']
        user = User(username=self.validated_data['username'],
                    first_name=self.validated_data['first_name'],
                    last_name=self.validated_data['last_name'],
                    email=self.validated_data['email'])
        user.set_password(password)

        user.save()

    class Meta:
        model = User
        fields = ('user_uuid', 'username', 'password', 'first_name', 'last_name', 'email')
        read_only_fields = ('user_uuid',)
        extra_kwargs = {
            'username': {'write_only': True},
            'email': {'write_only': True},
            'password': {'write_only': True}
        }

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('user_uuid', 'username', 'first_name', 'last_name', 'email')