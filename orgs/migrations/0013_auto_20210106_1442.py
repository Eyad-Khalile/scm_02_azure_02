# Generated by Django 3.0 on 2021-01-06 14:42

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('orgs', '0012_auto_20201222_1225'),
    ]

    operations = [
        migrations.RenameField(
            model_name='newsletter',
            old_name='email',
            new_name='nl_email',
        ),
        migrations.RenameField(
            model_name='newsletter',
            old_name='name',
            new_name='nl_name',
        ),
        migrations.RenameField(
            model_name='newsletter',
            old_name='org_name',
            new_name='nl_org_name',
        ),
        migrations.RenameField(
            model_name='newsletter',
            old_name='work',
            new_name='nl_work',
        ),
        migrations.AlterField(
            model_name='orgprofile',
            name='target_cat',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('No category selected', 'لا يوجد فئة محددة'), ('womans', 'نساء'), ('Mans', 'رجال'), ('Youth 18-24', 'شباب 18-24'), ('Child 0-18', 'أطفال 0-18'), ('Religious groups', 'مجموعات دینیة'), ('Ethnic groups', 'مجموعة عرقیة'), ('Persons lacking breadwinner', 'فاقدي المعیل'), ('Handicapped', 'ذوي الاحتیاجات الخاصة'), ('Refugees', 'لاجئین'), ('Displaced', 'نازحین'), ('Returned', 'عائدین'), ('Other civil society organizations', 'منظمات مجتمع مدني اخرى'), ('Other', 'أخرى')], max_length=255, verbose_name='الفئات المستهدفة'),
        ),
    ]
