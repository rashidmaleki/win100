from django.contrib.auth import get_user_model
from rest_framework import serializers
from signals.models import Signal, Currency
from accounts.v1.functions import check_user_status

User = get_user_model()


class SignalSerializer(serializers.ModelSerializer):
    price = serializers.IntegerField(required=False)
    presentation_time = serializers.DateTimeField(source='get_presentation_date')
    entry_point = serializers.IntegerField(required=False)
    created = serializers.DateTimeField(source='get_created_date')

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
            'status',
            'created',
        )
        depth = 1

    def validate(self, attrs):
        check_user_status(attrs['token'])
        return super().validate(attrs)
