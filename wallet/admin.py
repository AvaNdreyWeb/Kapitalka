from django.contrib import admin

from .models import Currency, Debt, Operation, Profile, Wallet

# Register your models here.
admin.site.register(Currency)
admin.site.register(Profile)
admin.site.register(Wallet)
admin.site.register(Operation)
admin.site.register(Debt)
