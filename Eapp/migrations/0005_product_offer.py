# Generated by Django 5.0.1 on 2024-01-29 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Eapp', '0004_remove_contact_us_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='offer',
            field=models.CharField(choices=[('YES', 'YES'), ('N0', 'NO')], default='NO', max_length=10),
        ),
    ]