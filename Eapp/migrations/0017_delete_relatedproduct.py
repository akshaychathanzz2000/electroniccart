# Generated by Django 5.0.1 on 2024-02-02 08:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Eapp', '0016_remove_wishlist_products_alter_wishlist_user_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Relatedproduct',
        ),
    ]
