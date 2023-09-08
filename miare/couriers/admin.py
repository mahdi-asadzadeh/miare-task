from django.contrib import admin

from couriers import models


@admin.register(models.Transaction)
class TransactionAdmin(admin.ModelAdmin):
    pass


@admin.register(models.TransactionDaily)
class TransactionDailyAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Courier)
class CourierAdmin(admin.ModelAdmin):
    pass
