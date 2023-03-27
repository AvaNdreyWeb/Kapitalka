# Generated by Django 4.1.7 on 2023-03-12 17:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0004_remove_profile_deposits_operation_depositor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='operation',
            name='depositor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='deposits', to='wallet.profile'),
        ),
    ]
