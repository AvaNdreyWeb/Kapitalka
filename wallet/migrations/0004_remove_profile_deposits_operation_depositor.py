# Generated by Django 4.1.7 on 2023-03-12 16:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0003_profile_alter_operation_benefitors_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='deposits',
        ),
        migrations.AddField(
            model_name='operation',
            name='depositor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='deposits', to='wallet.profile'),
        ),
    ]