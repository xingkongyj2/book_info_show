# Generated by Django 2.1.3 on 2018-12-28 01:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rabbit', '0003_booklist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booklist',
            name='bookID',
            field=models.CharField(max_length=300),
        ),
    ]