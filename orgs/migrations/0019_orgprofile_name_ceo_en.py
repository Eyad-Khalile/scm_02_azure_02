# Generated by Django 3.0 on 2021-02-03 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orgs', '0018_auto_20210203_1126'),
    ]

    operations = [
        migrations.AddField(
            model_name='orgprofile',
            name='name_ceo_en',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='اسم المدير التنفيذي باللغة الانجليزية'),
        ),
    ]
