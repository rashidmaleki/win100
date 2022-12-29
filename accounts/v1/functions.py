from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from accounts.models import Profile, Transaction
from rest_framework import status
from rest_framework.response import Response
from datetime import datetime
from django.utils import timezone


def check_user_status(token):
    try:
        user = Token.objects.get(key=token).user
        profile = Profile.objects.get(user=user)
    except:
        raise ValidationError(
            {"errors": [{"Success": False, "message": "توکن معتبر نیست"}]})

    if not profile.status:
        raise ValidationError(
            {"errors": [{"Success": False, "message": "حساب کاربری غیر فعال است"}]})

    try:
        user_plan = Transaction.objects.get(user=user)
    except:
        raise ValidationError(
            {"errors": [{"Success": False, "message": "کاربر اشتراک ندارد"}]})

    if datetime.now() > user_plan.expire_date:
        raise ValidationError(
            {"errors": [{"Success": False, "message": "اشتراک کاربر منقضی شده است"}]})
