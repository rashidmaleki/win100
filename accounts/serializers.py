from django.contrib.auth import get_user_model
from rest_framework import serializers

from accounts.models import Plan, Profile

from rest_framework.response import Response
from rest_framework import status
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

User = get_user_model()


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ('phone',)


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ("id", "email", "password", "profile")

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        profile = Profile.objects.get(user=user)
        profile.phone = validated_data['profile']['phone']
        profile.save()

        return user


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ['id', 'name', 'price', 'daily_credit']
