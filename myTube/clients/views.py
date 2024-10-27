from django.shortcuts import render
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import (
    GenericViewSet,
)
from clients.serializers import SubscribeCreateSerializer
from clients.models import Subscription


class SubscribeCreate(mixins.CreateModelMixin, GenericViewSet):
    serializer_class = SubscribeCreateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Subscription.objects.none()

    def perform_create(self, serializer):
        serializer.save()

