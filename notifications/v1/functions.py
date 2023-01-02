from django.shortcuts import HttpResponse
from fcm_django.models import FCMDevice
from firebase_admin.messaging import Message, Notification
from signals import models
from django.contrib.auth import get_user_model
from accounts.models import Transaction
from datetime import datetime
from django.db.models import Q

User = get_user_model()

# Create your views here.


def notif_add_signal(instance):
    plan = instance.plan.all()
    user = User.objects.filter(
        transAsUser__plan__in=plan).filter(transAsUser__expire_date__gte=datetime.now())
    device = FCMDevice.objects.filter(user__in=user)
    device.send_message(
        Message(notification=Notification(
            title="New Signal",
            body=f"New signal for {instance.currency.name}"))
    )


def notif_change_signal(instance):
    plan = instance.plan.all()
    user = User.objects.filter(transAsUser__plan__in=plan).filter(
        transAsUser__expire_date__gte=datetime.now())
    device = FCMDevice.objects.filter(user__in=user)
    device.send_message(
        Message(notification=Notification(
            title="Updaye Signal",
            body=f"Update signal for {instance.currency.name}"))
    )
