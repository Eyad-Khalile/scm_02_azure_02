# Generated by Django 3.0 on 2021-01-14 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orgs', '0015_auto_20210107_2056'),
    ]

    operations = [
        migrations.AddField(
            model_name='devorgopp',
            name='lang',
            field=models.CharField(choices=[('ar', 'عربي'), ('en', 'English'), ('ku', 'Kurdî')], default='ar', max_length=100, verbose_name='اللغة'),
        ),
        migrations.AddField(
            model_name='orgcapacityopp',
            name='lang',
            field=models.CharField(choices=[('ar', 'عربي'), ('en', 'English'), ('ku', 'Kurdî')], default='ar', max_length=100, verbose_name='اللغة'),
        ),
        migrations.AddField(
            model_name='orgdata',
            name='lang',
            field=models.CharField(choices=[('ar', 'عربي'), ('en', 'English'), ('ku', 'Kurdî')], default='ar', max_length=100, verbose_name='اللغة'),
        ),
        migrations.AddField(
            model_name='orgfundingopp',
            name='lang',
            field=models.CharField(choices=[('ar', 'عربي'), ('en', 'English'), ('ku', 'Kurdî')], default='ar', max_length=100, verbose_name='اللغة'),
        ),
        migrations.AddField(
            model_name='orgjob',
            name='lang',
            field=models.CharField(choices=[('ar', 'عربي'), ('en', 'English'), ('ku', 'Kurdî')], default='ar', max_length=100, verbose_name='اللغة'),
        ),
        migrations.AddField(
            model_name='orgmedia',
            name='lang',
            field=models.CharField(choices=[('ar', 'عربي'), ('en', 'English'), ('ku', 'Kurdî')], default='ar', max_length=100, verbose_name='اللغة'),
        ),
        migrations.AddField(
            model_name='orgnews',
            name='lang',
            field=models.CharField(choices=[('ar', 'عربي'), ('en', 'English'), ('ku', 'Kurdî')], default='ar', max_length=100, verbose_name='اللغة'),
        ),
        migrations.AddField(
            model_name='orgrapport',
            name='lang',
            field=models.CharField(choices=[('ar', 'عربي'), ('en', 'English'), ('ku', 'Kurdî')], default='ar', max_length=100, verbose_name='اللغة'),
        ),
        migrations.AddField(
            model_name='orgresearch',
            name='lang',
            field=models.CharField(choices=[('ar', 'عربي'), ('en', 'English'), ('ku', 'Kurdî')], default='ar', max_length=100, verbose_name='اللغة'),
        ),
        migrations.AddField(
            model_name='persfundingopp',
            name='lang',
            field=models.CharField(choices=[('ar', 'عربي'), ('en', 'English'), ('ku', 'Kurdî')], default='ar', max_length=100, verbose_name='اللغة'),
        ),
    ]
