from rest_framework import serializers
from clients.models import Subscription, get_user_model
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model

class CustomUserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email', 'password', 'date_birth', 'photo')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        return user

class SubscribeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ("channel",)

    def create(self, validated_data):
        subscriber = self.context["request"].user
        channel = validated_data["channel"]

        if subscriber != channel:
            sub, created = Subscription.objects.get_or_create(
                subscriber=subscriber,
                channel=channel,
            )
            return sub
        raise serializers.ValidationError("You cannot subscribe to yourself.")


class PublicAuthorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("username", "email")


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["id", "username", "email", "date_birth", "first_name"]
