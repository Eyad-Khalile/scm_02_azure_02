# Generated by Django 3.0 on 2021-02-03 11:26

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orgs', '0017_auto_20210203_1116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orgprofile',
            name='message_en',
            field=ckeditor.fields.RichTextField(blank=True, max_length=5000, null=True, verbose_name='الرؤية و الرسالة باللغة الانكليزية'),
        ),
    ]
