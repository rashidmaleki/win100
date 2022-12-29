from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from accounts.models import Profile, Transaction
from rest_framework import status
from rest_framework.response import Response
from datetime import datetime
from django.utils import timezone


def check_token(token):
    try:
        user = Token.objects.get(key=token).user
        return user
    except:
        raise ValidationError(
            {
                'Success': False,
                'ErrorCode': 101,
                'ErrorMessage': 'توکن نا معتبر است',
            }
        )


def check_user_status(token):
    user = check_token(token)
    profile = Profile.objects.get(user=user)

    if not profile.status:
        raise ValidationError(
            {
                'Success': False,
                'ErrorCode': 102,
                'ErrorMessage': 'حساب کاربری غیر فعال است',
            }
        )

    try:
        user_plan = Transaction.objects.get(user=user)
    except:
        raise ValidationError(
            {
                'Success': False,
                'ErrorCode': 103,
                'ErrorMessage': 'کاربر اشتراک ندارد',
            }
        )

    if datetime.now() > user_plan.expire_date:
        raise ValidationError(
            {
                'Success': False,
                'ErrorCode': 104,
                'ErrorMessage': 'اشتراک کاربر منقضی شده است',
            }
        )
