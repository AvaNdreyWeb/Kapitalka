import uuid

from django.contrib.auth.models import User
from django.db import models


class Currency(models.Model):
    name = models.CharField(
        max_length=200,
        default="Российский рубль",
        null=False
    )
    code = models.CharField(
        max_length=10,
        unique=True,
        default='RUB'
    )
    symbol = models.CharField(max_length=10)

    def __str__(self):
        return self.symbol


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, default="", null=False)
    slug = models.SlugField(default="", null=False)

    def __str__(self):
        return self.name


class Wallet(models.Model):
    title = models.CharField(max_length=200, default="", null=False)
    slug = models.SlugField(default="", null=False)
    balance = models.FloatField(
        verbose_name='Баланс',
        default=0,
        null=False
    )
    currency = models.ForeignKey(
        Currency,
        on_delete=models.SET_DEFAULT,
        to_field='code',
        default='RUB'
    )
    members = models.ManyToManyField(
        Profile,
        related_name='wallets'
    )
    operations = models.ManyToManyField(
        "Operation",
        related_name='wallet',
        blank=True
    )

    def __str__(self):
        return self.title


class Operation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, null=False)
    name = models.CharField(max_length=200, default="", null=False)
    value = models.FloatField(default=0, null=False)
    is_income = models.BooleanField(
        verbose_name='Доход',
        default=False,
        null=False
    )
    currency = models.ForeignKey(
        Currency,
        on_delete=models.SET_DEFAULT,
        to_field='code',
        default='RUB'
    )
    description = models.TextField(
        verbose_name='Описание',
        default="",
        null=False
    )
    date = models.DateTimeField(auto_now=True)
    depositor = models.ForeignKey(
        Profile,
        related_name="deposits",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    benefitors = models.ManyToManyField(
        Profile,
        related_name='benefits',
        blank=True,
    )

    class Meta:
        ordering = ['-date', 'name']

    def __str__(self):
        return self.name


class Debt(models.Model):
    value = models.FloatField(default=0, null=False)
    is_income = models.BooleanField(
        verbose_name='Доход',
        default=False,
        null=False
    )
    currency = models.ForeignKey(
        Currency,
        on_delete=models.SET_DEFAULT,
        to_field='code',
        default='RUB'
    )
    description = models.TextField(
        verbose_name='Описание',
        default="",
        null=False
    )
    creditor = models.ForeignKey(
        Profile,
        related_name="credits",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    debtor = models.ForeignKey(
        Profile,
        related_name="debts",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return f'{self.debtor} -$> {self.creditor}'
