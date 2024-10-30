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
from django.contrib.auth.models import User
from rest_framework import status


class SubscribeCreate(mixins.CreateModelMixin, GenericViewSet):
    serializer_class = SubscribeCreateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Subscription.objects.none()

    def perform_create(self, serializer):
        serializer.save()


class ProfileViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        user = request.user
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)


class Currentuser(ViewSet):
    lookup_field = "username"

    def retrieve(self, request, username=None):
        queryset = get_object_or_404(User, username=username)

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
