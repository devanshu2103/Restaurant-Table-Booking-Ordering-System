# Generated by Django 5.2.3 on 2025-06-18 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_alter_menuitem_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='seat_number',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
