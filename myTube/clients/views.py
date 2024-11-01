from django.shortcuts import get_object_or_404
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import (
    GenericViewSet,
)
from clients.serializers import (
    SubscribeCreateSerializer,
    PublicAuthorProfileSerializer,
    UserProfileSerializer,
)
from clients.models import Subscription
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from rest_framework import status


class SubscribeCreate(mixins.CreateModelMixin,
                       mixins.DestroyModelMixin,
                       GenericViewSet):
    serializer_class = SubscribeCreateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Subscription.objects.filter(subscriber=self.request.user)

    def perform_create(self, serializer):
        serializer.save(subscriber=self.request.user)

    def destroy(self, request, *args, **kwargs):
        channel_id = self.request.data.get("channel_id")
        if not channel_id:
            return Response(
                {"detail": "Необходимо указать ID канала для отписки."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            subscription = Subscription.objects.get(
                subscriber=request.user, channel_id=channel_id
            )
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Subscription.DoesNotExist:
            return Response(
                {"detail": "Подписка не найдена."},
                status=status.HTTP_404_NOT_FOUND,
            )


class ProfileViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        user = request.user
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)


class Currentuser(ViewSet):
    lookup_field = "username"

    def retrieve(self, request, username=None):
        queryset = get_object_or_404(get_user_model(), username=username)

        serializer = PublicAuthorProfileSerializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SubsUser(ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        user = request.user
        subscriptions = Subscription.objects.filter(subscriber=user).select_related(
            "channel"
        )
        authors = [subscription.channel for subscription in subscriptions]
        serializer = PublicAuthorProfileSerializer(authors, many=True)
        return Response(serializer.data)
