from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Locations
from django.contrib.auth import get_user_model


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Locations
        fields = '__all__'



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = '__all__'



class SignUpSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=45)
    password = serializers.CharField(min_length=8, write_only=True)


    class Meta:
        User = get_user_model()
        model = User
        fields = ["email", "username", "password"]

    def validate(self, attrs):
        User = get_user_model()
        email_exists = User.objects.filter(email=attrs["email"]).exists()

        if email_exists:
            raise ValidationError("Email has already been used")

        return super().validate(attrs)

    def create(self, validated_data):
        password = validated_data.pop("password")

        user = super().create(validated_data)

        user.set_password(password)

        user.save()

        # Token.objects.create(user=user)

        return user
