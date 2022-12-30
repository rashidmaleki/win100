from django.contrib.auth import get_user_model
from django.contrib.auth import password_validation
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework.validators import UniqueValidator
from accounts.models import Plan, Profile, Transaction

User = get_user_model()

class ProfileSerializerF(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('phone', 'status')


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ['id', 'name', 'price', 'daily_credit']


class TransactionSerializer(serializers.ModelSerializer):
    plan = PlanSerializer()

    class Meta:
        model = Transaction
        fields = ('plan', 'expire_date_time')


class UserSerializerF(serializers.ModelSerializer):
    profile = ProfileSerializerF()
    package = TransactionSerializer()
    class Meta:
        model = User
        fields = ('email', 'profile', 'package')






class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('phone',)



class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='profile.phone')
    class Meta:
        model = User
        fields = ('id','phone')

class UserSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
    profile = UserProfileSerializer()
    # transaction = TransactionSerializer(many=True)


# Serializer to Register User
class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    profile = ProfileSerializer(required=False)
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User

        fields = ('email', 'profile', 'password')

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        if 'profile' in validated_data:
            profile = Profile.objects.get(user=user)
            profile.phone = validated_data['profile']['phone']
            profile.save()
        return user


