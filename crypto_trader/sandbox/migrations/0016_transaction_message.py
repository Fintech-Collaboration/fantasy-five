# Generated by Django 3.2.8 on 2021-10-16 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sandbox', '0015_auto_20211013_0846'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='message',
            field=models.CharField(default='', max_length=35),
        ),
    ]
