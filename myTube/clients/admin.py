from django.contrib import admin
from django.contrib.auth import get_user_model

from django.contrib import admin

from clients.models import Subscription

admin.site.register(Subscription)
