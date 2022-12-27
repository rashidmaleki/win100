from django.contrib.auth import get_user_model
from rest_framework import serializers
from signals.models import Signal, Currency

User = get_user_model()



class SignalSerializer(serializers.ModelSerializer):

    class Meta:
        model = Signal
        fields = (
            'id',
            'currency',
            'price',
            'presentation_time',
            'entry_point',
            'loss_limit',
            'target1',
            'target2',
            'target3',
            'target4',
            'target5',
            'lever',
            'plan',
            'created',
            'edited',
        )
        depth = 1 


class CurrencySerializer(serializers.ModelSerializer):
    signal_list = SignalSerializer(many=True, read_only=True)
    class Meta:
        model = Currency
        fields = ('id')