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
from rest_framework.viewsets import ViewSet, ReadOnlyModelViewSet, ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from rest_framework import status
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page


class SubscribeCreateDestroy(
    mixins.CreateModelMixin, mixins.DestroyModelMixin, GenericViewSet
):
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


class ProfileViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    queryset = get_user_model().objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    @method_decorator(cache_page(settings.CACHE_TTL))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class SelectedUserViewSet(ReadOnlyModelViewSet):
    lookup_field = "username"
    serializer_class = PublicAuthorProfileSerializer

    def get_queryset(self):
        return get_user_model().objects.all()

    def list(self, request, *args, **kwargs):
        return Response(None)

    def retrieve(self, request, username=None):
        queryset = get_object_or_404(get_user_model(), username=username)
        serializer = self.get_serializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @method_decorator(cache_page(settings.CACHE_TTL))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class SubsUserViewSet(ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PublicAuthorProfileSerializer

    def get_queryset(self):
        user = self.request.user
        return get_user_model().objects.filter(channels__subscriber=user)

    @method_decorator(cache_page(settings.CACHE_TTL))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
