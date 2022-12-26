from django.contrib import admin
from django.contrib import admin

from support.models import Departman, Ticket

# Register your models here.
@admin.register(Departman)
class DepartmanAdmin(admin.ModelAdmin):
    pass


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('user', 'departman', 'subject', 'created', 'answerd')
    exclude = ('answerd',)
    search_fields = ('subject', 'text', 'answer')
    list_filter = (
        ('departman'),
        ('answerd'),
        ('created', admin.DateFieldListFilter),
    )

    readonly_fields = ["user", "departman", "subject", 'text']





