# Generated by Django 3.1.1 on 2020-12-02 21:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orgs', '0003_auto_20201202_2047'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orgprofile',
            name='position',
        ),
        migrations.RemoveField(
            model_name='position',
            name='org_id',
        ),
        migrations.AddField(
            model_name='position',
            name='org_profile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='orgs.orgprofile', verbose_name='اسم المنظمة'),
        ),
    ]
