from django.db import migrations

from .. import scipts

class Migration(migrations.Migration):
    dependencies = [
        ('accounts', '0002_customuser_business_type_alter_customuser_phone_and_more'),
        ('pages', '0001_initial'),
        ('stock', '0002_product_user_alter_category_name_alter_product_name_and_more'),
    ]

    operations = [
        migrations.RunPython(scipts.create_default_data),
    ]
