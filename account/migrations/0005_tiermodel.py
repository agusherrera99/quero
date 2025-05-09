# Generated by Django 5.1.4 on 2025-01-29 13:57

from django.db import migrations, models

from account import scripts


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_notification'),
    ]

    operations = [
        migrations.CreateModel(
            name='TierModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='gratuito', max_length=50)),
                ('duration', models.IntegerField(default=15)),
            ],
        ),
        migrations.RunPython(scripts.create_default_tiers),
    ]
