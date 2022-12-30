from django.contrib.auth import get_user_model
from rest_framework import serializers
from notifications.models import Notification, Faq
from rest_framework.authtoken.models import Token
from accounts.v1.functions import check_user_status, check_token

User = get_user_model()


class NotificationSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField(source='get_created_date')
    class Meta:
        model = Notification
        fields = ('id','subject', 'text', 'created')


class FaqSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField(source='get_created_date')
    class Meta:
        model = Faq
        fields = ('id','question', 'answer', 'created')