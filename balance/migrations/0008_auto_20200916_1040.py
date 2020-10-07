# Generated by Django 3.0.6 on 2020-09-16 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('balance', '0007_auto_20200826_1639'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='ls',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='company_info',
            name='credit_limit',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='history_info',
            name='credit_limit',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
    ]