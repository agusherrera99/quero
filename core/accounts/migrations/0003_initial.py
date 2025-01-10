from django.db import migrations

from .. import scipts

class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('accounts', '0002_initial'),
        ('stock', '0001_initial'),
        ('pos', '0001_initial'),
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(scipts.create_default_data),
    ]