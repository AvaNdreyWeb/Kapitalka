# Generated by Django 4.1.7 on 2023-03-20 10:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0008_remove_operation_benefitors_operation_benefitors'),
    ]

    operations = [
        migrations.AlterField(
            model_name='operation',
            name='benefitors',
            field=models.ManyToManyField(blank=True, related_name='benefits', to='wallet.profile'),
        ),
        migrations.AlterField(
            model_name='wallet',
            name='operations',
            field=models.ManyToManyField(blank=True, related_name='wallet', to='wallet.operation'),
        ),
        migrations.CreateModel(
            name='Debt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField(default=0)),
                ('is_income', models.BooleanField(default=False, verbose_name='Доход')),
                ('description', models.TextField(default='', verbose_name='Описание')),
                ('creditor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='credits', to='wallet.profile')),
                ('currency', models.ForeignKey(default='RUB', on_delete=django.db.models.deletion.SET_DEFAULT, to='wallet.currency', to_field='code')),
                ('debtor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='debts', to='wallet.profile')),
            ],
        ),
    ]
