from django.contrib.auth import get_user_model
from signals.serializers import SignalSerializer
from signals.models import Signal
from rest_framework import viewsets

User = get_user_model()

class SignalViewSet(viewsets.ModelViewSet):
    queryset = Signal.objects.all()
    serializer_class = SignalSerializer