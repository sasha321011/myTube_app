from rest_framework import serializers
from clients.models import Subscription, get_user_model


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
