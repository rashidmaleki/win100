from django.contrib.auth import get_user_model
from signals.serializers import SignalSerializer
from signals.models import Signal
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from accounts.models import Transaction
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

User = get_user_model()


class SignalViewSet(generics.ListAPIView):
    queryset = Signal.objects.all()
    serializer_class = SignalSerializer
    permission_classes = [IsAuthenticated]


class SignalByEmailViewSet(generics.ListAPIView):
    
    serializer_class = SignalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        email = self.request.query_params.get('email')
        user = get_object_or_404(User, email=email)
        user_plan = Transaction.objects.get(user=user)
        signal = Signal.objects.filter(plan=user_plan.plan)
        return signal
    