from django.shortcuts import render
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import (
    GenericViewSet,
)
from clients.serializers import SubscribeCreateSerializer


class SubscribeCreate(mixins.CreateModelMixin, GenericViewSet):
    serializer_class = SubscribeCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()
