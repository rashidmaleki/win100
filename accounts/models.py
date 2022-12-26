from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import ugettext_lazy as _


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
    user = models.ForeignKey(User, verbose_name=_("کاربر"), on_delete=models.CASCADE)
    txid = models.CharField(verbose_name='کد تراکنش', max_length=100)
    payment_status = models.BooleanField(verbose_name='وضعیت پرداخت')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت')
    
    def __str__(self) -> str:
        return self.txid
    
    class Meta:
        verbose_name_plural = "پرداخت ها"
        verbose_name = "پرداخت"


class Plan(models.Model):
    name = models.CharField(max_length=50, verbose_name='نام پکیج')
    price = models.IntegerField(verbose_name='قیمت')
    daily_credit = models.IntegerField(default=0, verbose_name='مدت زمان اعتبار')

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name_plural = "پکیج ها"
        verbose_name = "پکیج"


class Transaction(models.Model):
    user = models.ForeignKey(User, verbose_name=_("کاربر"), on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, verbose_name=_("پکیج"), on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, verbose_name=_("تراکنش"), on_delete=models.CASCADE)
    expire_date = models.DateTimeField(verbose_name='تاریخ انقضاء')

    class Meta:
        verbose_name_plural = "اشتراک کاربران"
        verbose_name = "اشتراک کاربر"
