# Generated by Django 4.2.2 on 2023-06-10 23:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('albums', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='album',
            name='bucket',
        ),
    ]
