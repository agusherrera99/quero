# Generated by Django 5.1.4 on 2025-01-29 13:58

import account.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_tiermodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='tier',
            field=models.ForeignKey(blank=True, default=account.models.get_default_tier, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.tiermodel'),
        ),
    ]
