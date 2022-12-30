from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from .serializers import NotificationSerializer, FaqSerializer
from accounts.v1.serializers import UserSerializer, PlanSerializer, ProfileSerializerF, UserSerializerF
from notifications.models import Notification, Faq
from django.shortcuts import get_object_or_404
from accounts.v1.functions import check_token
User = get_user_model()


class NotificationViewSet(generics.ListAPIView):
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all()

    def post(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class FaqViewSet(generics.ListAPIView):
    serializer_class = FaqSerializer
    queryset = Faq.objects.all()

    def post(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
