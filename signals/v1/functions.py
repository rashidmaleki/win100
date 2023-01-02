from django.shortcuts import HttpResponse
from fcm_django.models import FCMDevice
from firebase_admin.messaging import Message, Notification


# Create your views here.
def send_notification():
    FCMDevice.objects.send_message(
        Message(notification=Notification(
            title="title", body="body", image="image_url"))
    )
