# Generated by Django 4.2.1 on 2023-05-30 02:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_customuser_last_login'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='quit_reason',
            field=models.TextField(blank=True),
        ),
    ]