# Generated by Django 5.0.1 on 2024-02-01 17:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Eapp', '0012_rename_review_review_review_desp'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='rating',
            new_name='ratings',
        ),
    ]
