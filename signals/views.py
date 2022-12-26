from django.contrib.auth import get_user_model
from rest_framework import generics
from signals.serializers import SignalSerializer
from signals.models import Signal
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework import status

User = get_user_model()

class SignalViewSet(generics.ListCreateAPIView):
    queryset = Signal.objects.all()
    serializer_class = SignalSerializer
