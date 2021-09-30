from django.contrib import admin
from users import models


@admin.register(models.Wallet)
class WalletAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Company)
class CompanyAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Employee)
class EmployeeAdmin(admin.ModelAdmin):
    pass
