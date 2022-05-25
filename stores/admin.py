from django.contrib import admin
from .models import Store


@admin.register(Store)
class RequestAdmin(admin.ModelAdmin):
    transaction_display = [field.name for field in Store._meta.get_fields()]
