# Generated by Django 5.1.4 on 2025-02-21 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_customuser_is_sub_account_customuser_parent_account'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='address',
            field=models.CharField(blank=True, max_length=255, null=True, default='sin dirección'),
        ),
    ]
