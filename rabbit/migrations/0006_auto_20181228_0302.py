# Generated by Django 2.1.3 on 2018-12-28 03:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rabbit', '0005_booklist_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booklist',
            name='price',
            field=models.CharField(max_length=32),
        ),
    ]
