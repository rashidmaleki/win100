from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from accounts.models import Profile, Transaction, Payment, Plan, WalletAddress
from datetime import datetime, timedelta
import requests


def check_token(token):
    try:
        user = Token.objects.get(key=token).user
        return user
    except:
        raise ValidationError(
            {'Error': {
                'Success': False,
                'ErrorCode': 101,
                'ErrorMessage': 'The token is invalid',
            }}
        )


def check_user_status(token):
    user = check_token(token)
    profile = Profile.objects.get(user=user)

    if not profile.status:
        raise ValidationError(
            {'Error': {
                'Success': False,
                'ErrorCode': 102,
                'ErrorMessage': 'حساب کاربری غیر فعال است',
            }}
        )

    try:
        user_plan = Transaction.objects.get(user=user)
    except:
        raise ValidationError(
            {'Error': {
                'Success': False,
                'ErrorCode': 103,
                'ErrorMessage': 'The user does not have a subscription',
            }}
        )

    if datetime.now() > user_plan.expire_date:
        raise ValidationError(
            {'Error': {
                'Success': False,
                'ErrorCode': 104,
                'ErrorMessage': 'User subscription has expired',
            }}
        )


def check_transfer(user, hash, plan_id):

    url = f"https://apilist.tronscanapi.com/api/transaction-info?hash={hash}"

    headers = {"accept": "application/json"}

    try:
        response = requests.get(url, headers=headers).json()
    except:
        raise ValidationError(
            {'Error': {
                'Success': False,
                'ErrorCode': 109,
                'ErrorMessage': 'Could not connect to the server',
            }}
        )

    try:
        response['tokenTransferInfo']
    except:
        raise ValidationError(
            {'Error': {
                'Success': False,
                'ErrorCode': 108,
                'ErrorMessage': 'The hash is not valid',
            }}
        )

    check_payment = Payment.objects.filter(txid=hash)
    if check_payment.exists():
        raise ValidationError(
            {'Error': {
                'Success': False,
                'ErrorCode': 110,
                'ErrorMessage': 'The hash code is duplicated',
            }}
        )

    address = WalletAddress.objects.filter(
        code=response['tokenTransferInfo']['to_address'])
    if not address.exists():
        raise ValidationError(
            {'Error': {
                'Success': False,
                'ErrorCode': 111,
                'ErrorMessage': 'The destination account is not valid',
            }}
        )

    amount_str = response['tokenTransferInfo']['amount_str']
    amount_int = int(amount_str)

    decimals = response['tokenTransferInfo']['decimals']

    amount = amount_int / (10 ** decimals)
    plan = Plan.objects.get(id=plan_id)
    if plan.price-1 <= amount <= plan.price+1:
        payment = Payment.objects.create(
            user=user,
            txid=hash,
            payment_status=True,
        )
        payment.save()

        transaction, created = Transaction.objects.get_or_create(user=user)
        transaction.plan = plan
        transaction.payment = payment
        print('----------------------------')

        if datetime.now() < transaction.expire_date:
            delta_time = timedelta(days=plan.daily_credit)
            transaction.expire_date = transaction.expire_date + delta_time
        else:
            transaction.expire_date = datetime.now() + timedelta(days=plan.daily_credit)

        transaction.save()

        return True
    else:
        raise ValidationError(
            {'Error': {
                'Success': False,
                'ErrorCode': 107,
                'ErrorMessage': 'The deposit amount is not correct',
            }}
        )
