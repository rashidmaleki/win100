from django.contrib.auth import get_user_model
from rest_framework import serializers
from support.models import Departman

User = get_user_model()


class DepartmansSerializer(serializers.ModelSerializer):

    class Meta:
        model = Departman
        fields = ('id', 'name')
