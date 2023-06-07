# Generated by Django 4.2.1 on 2023-05-29 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_customuser_managers'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='rejection_reason',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='status',
            field=models.CharField(choices=[('W', '대기'), ('A', '승인'), ('R', '거절')], default='W', max_length=1),
        ),
    ]