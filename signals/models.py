from django.db import models
from django.contrib import admin
from django.urls import reverse
from accounts.models import Plan
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from notifications.v1.functions import notif_add_signal, notif_change_signal
# Create your models here.


class Currency(models.Model):
    name = models.CharField(verbose_name='نام ارز', max_length=50)
    code = models.CharField(verbose_name='اختصار', max_length=50)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name_plural = "ارزها"
        verbose_name = "ارز"


class Signal(models.Model):
    currency = models.ForeignKey(Currency, verbose_name=(
        "نام ارز"), on_delete=models.CASCADE)
    price = models.IntegerField(verbose_name=("قیمت فعلی"))
    presentation_time = models.DateTimeField(
        verbose_name=("تاریخ و ساعت ارائه"))
    entry_point = models.FloatField(verbose_name=("نقطه ورود"))
    loss_limit = models.FloatField(
        blank=True, null=True, verbose_name=("حد ضرر"))
    target1 = models.FloatField(
        blank=True, null=True, verbose_name=("تارگت اول"))
    target2 = models.FloatField(
        blank=True, null=True, verbose_name=("تارگت دوم"))
    target3 = models.FloatField(
        blank=True, null=True, verbose_name=("تارگت سوم"))
    target4 = models.FloatField(
        blank=True, null=True, verbose_name=("تارگت چهارم"))
    target5 = models.FloatField(
        blank=True, null=True, verbose_name=("تارگت پنجم"))
    lever = models.FloatField(blank=True, null=True, verbose_name=("اهرم"))
    plan = models.ManyToManyField(
        Plan, verbose_name=("پکیج"), related_name='planneke')
    status = models.BooleanField(default=True, verbose_name='فعال')
    created = models.DateTimeField(
        auto_now_add=True, verbose_name='تاریخ ثبت سیگنال')
    edited = models.DateTimeField(auto_now=True)

    @admin.display(description="پکیج")
    def get_plans(self):
        return ", ".join([str(p.name) for p in self.plan.all()])

    def get_presentation_date(self):
        return self.presentation_time.strftime('%Y/%m/%d - %H:%M')

    def get_created_date(self):
        return self.created.strftime('%Y/%m/%d - %H:%M')

    def __str__(self) -> str:
        return f'سیگنال شماره {self.id}'

    class Meta:
        verbose_name_plural = "سیگنال ها"
        verbose_name = "سیگنال"
        ordering = ['-created']


@receiver(m2m_changed, sender=Signal.plan.through)
def add_signal(sender, instance, action, reverse, **kwargs):
    if action == 'post_add':
        notif_add_signal(instance)


@receiver(post_save, sender=Signal)
def Update_signal(sender, instance, created, **kwargs):
    if not created:
        notif_change_signal(instance)
