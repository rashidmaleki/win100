from django.contrib.auth import get_user_model
from signals.v1.serializers import SignalSerializer
from signals.models import Signal
from rest_framework import generics
from accounts.models import Transaction
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from accounts.v1.functions import check_user_status
from rest_framework.views import APIView
import requests
from .functions import send_notification
User = get_user_model()


class UserSignalViewSet(generics.ListAPIView):
    serializer_class = SignalSerializer

    def get_queryset(self):
        check_user_status(self.request.data['token'])
        token = self.request.data['token']
        user = Token.objects.get(key=token).user
        user_transaction = Transaction.objects.get(user=user)
        plan = user_transaction.plan

        signal = Signal.objects.filter(plan=plan)
        return signal

    def post(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class CoinsViewSet(APIView):
    def post(self, request):
        url = 'https://api.coinranking.com/v2/coins'
        responce = requests.get(url=url).json()
        return Response(responce)


class SendNotifViewSet(APIView):
    def get(self, request, format=None):
        send_notification()
        return Response('sent')
