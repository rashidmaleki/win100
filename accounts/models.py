from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from datetime import datetime
from django.utils import timezone


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """User model."""

    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()


class Payment(models.Model):
    user = models.ForeignKey(User, verbose_name=_(
        "??????????"), on_delete=models.CASCADE)
    txid = models.CharField(verbose_name='???? ????????????', max_length=100)
    payment_status = models.BooleanField(verbose_name='?????????? ????????????')
    created = models.DateTimeField(auto_now_add=True, verbose_name='?????????? ??????')

    def __str__(self) -> str:
        return self.txid

    class Meta:
        verbose_name_plural = "???????????? ????"
        verbose_name = "????????????"


class Plan(models.Model):
    name = models.CharField(max_length=50, verbose_name='?????? ????????')
    price = models.FloatField(verbose_name='????????')
    daily_credit = models.IntegerField(
        default=0, verbose_name='?????? ???????? ????????????')

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name_plural = "???????? ????"
        verbose_name = "????????"


class Transaction(models.Model):
    user = models.OneToOneField(User, verbose_name=_(
        "??????????"), on_delete=models.CASCADE, related_name='transAsUser')
    plan = models.ForeignKey(Plan, verbose_name=_(
        "????????"), on_delete=models.CASCADE, related_name='transAsPlan', null=True)
    payment = models.ForeignKey(Payment, verbose_name=_(
        "????????????"), on_delete=models.CASCADE, related_name='transAspayment', null=True)
    expire_date = models.DateTimeField(
        verbose_name='?????????? ????????????', default=timezone.now, null=True)

    def expire_date_time(self):
        return self.expire_date.strftime('%Y/%m/%d - %H:%M')

    def has_packege(self):
        if datetime.now() < self.expire_date:
            return True
        else:
            return False

    class Meta:
        verbose_name_plural = "???????????? ??????????????"
        verbose_name = "???????????? ??????????"


class Profile(models.Model):
    user = models.OneToOneField(
        User, verbose_name="??????????????", on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=11, blank=True,
                             null=True, verbose_name='????????????')
    status = models.BooleanField(default=True, verbose_name='????????')

    class Meta:
        verbose_name_plural = "?????????????? ??????????????"
        verbose_name = "?????????????? ??????????"


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        Token.objects.create(user=instance)
    instance.profile.save()


class WalletAddress(models.Model):
    name = models.CharField(verbose_name='??????', max_length=50)
    code = models.CharField(verbose_name='?????????? ????????', max_length=100)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name_plural = "???????? ?????? ?????? ??????"
        verbose_name = "???????? ?????? ??????"
