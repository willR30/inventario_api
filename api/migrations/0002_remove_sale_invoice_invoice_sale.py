# Generated by Django 4.2.1 on 2023-10-15 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sale',
            name='invoice',
        ),
        migrations.AddField(
            model_name='invoice',
            name='sale',
            field=models.ManyToManyField(to='api.sale'),
        ),
    ]
