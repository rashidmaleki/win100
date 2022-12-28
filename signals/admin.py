from django.contrib import admin
from signals.models import Signal, Currency


# Register your models here.
@admin.register(Signal)
class SignalAdmin(admin.ModelAdmin):
    list_display = ('currency', 'price', 'get_plans',
                    'presentation_time', 'entry_point', 'loss_limit', 'status')
    list_filter = (
        ('created'),
        ('currency'),
        ('price'),
        ('plan'),
        ('entry_point'),
        ('loss_limit'),
        ('status'),
    )


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    pass
