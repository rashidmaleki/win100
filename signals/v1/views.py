from django.contrib.auth import get_user_model
from signals.v1.serializers import SignalSerializer
from signals.models import Signal
from rest_framework import generics
from accounts.models import Transaction
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError


User = get_user_model()


class UserSignalViewSet(generics.ListAPIView):
    serializer_class = SignalSerializer

    def get_queryset(self):
        if 'token' in self.request.data:
            try:
                token = self.request.data['token']
                user = Token.objects.get(key=token).user
            except:
                raise ValidationError({
                    'Success': False,
                    'Message': 'توکن وجود ندارد'
                })
        else:
            raise ValidationError({
                'Success': False,
                'Message': 'توکن نیاز است'
            })

        try:
            user_transaction = Transaction.objects.get(user=user)
            plan = user_transaction.plan
        except:
            raise ValidationError({
                'Success': False,
                'Message': 'کاربر اشتراک ندارد'
            })

        signal = Signal.objects.filter(plan=plan)
        return signal

    def post(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
