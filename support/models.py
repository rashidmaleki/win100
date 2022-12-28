from django.db import models
from django.contrib.auth import get_user_model
from django.contrib import admin
from django.db.models.signals import pre_save
from django.dispatch import receiver
import jdatetime

User = get_user_model()

# Create your models here.


class Departman(models.Model):
    name = models.CharField(verbose_name='واحد', max_length=50)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name_plural = "واحدها"
        verbose_name = "واحد"


class Ticket(models.Model):
    user = models.ForeignKey(User, verbose_name="کاربر",
                             on_delete=models.CASCADE)
    departman = models.ForeignKey(
        Departman, verbose_name=("واحد"), on_delete=models.CASCADE)
    subject = models.CharField(verbose_name='عنوان', max_length=50)
    text = models.TextField(verbose_name="متن تیکت")
    answer = models.TextField(verbose_name="پاسخ", blank=True, null=True)
    answerd = models.BooleanField(verbose_name='وضعیت پاسخ', default=False)
    created = models.DateTimeField(
        auto_now_add=True, verbose_name='ایجاد شده در')

    def __str__(self) -> str:
        return f'تیکت شماره {self.id}'

    class Meta:
        verbose_name_plural = "تیکت ها"
        verbose_name = "تیکت"


@receiver(pre_save, sender=Ticket)
def signal_name(sender, instance, **kwargs):
    if instance.answer:
        instance.answerd = True
    else:
        instance.answerd = False
