# Generated by Django 3.1.1 on 2020-12-16 20:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('orgs', '0010_auto_20201207_1431'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='city_work_en',
            field=models.CharField(blank=True, default='', max_length=255, null=True, verbose_name='اسم المدينة بالانكليزية'),
        ),
        migrations.AlterField(
            model_name='city',
            name='city_work_ku',
            field=models.CharField(blank=True, default='', max_length=255, null=True, verbose_name='اسم المدينة بالكردية'),
        ),
        migrations.AlterField(
            model_name='orgcapacityopp',
            name='capacity_domain',
            field=models.CharField(choices=[('Media', 'اﻹعلام و المناصرة'), ('Education', 'تعليم'), ('Protection', 'حماية و الصحة النفسية'), ('Livelihoods and food security', 'سبل العيش واﻷمن الغذائي'), ('Project of clean & water & sanitation ', 'النظافة والمياه والصرف الصحي'), ('Development', 'تنمية و بناء قدرات و ثقافة'), ('Law & suport & policy', 'المواطنة و الحوكمة و الديموقراطية و السلام و السياسة'), ('Donors and support volunteering', 'اﻷسرة و الجندرة و قضايا المرأة'), ('Religious org', 'المأوى و البنة التحتية'), ('Prof association and assembles', 'تنسيق و تجمعات المجتمع المدني'), ('Health', 'صحة'), ('Studies and research', 'دراسات وأبحاث'), ('Other', 'أخرى')], max_length=255, verbose_name='قطاع الفرصة'),
        ),
        migrations.AlterField(
            model_name='orgfundingopp',
            name='work_domain',
            field=models.CharField(choices=[('Media', 'اﻹعلام و المناصرة'), ('Education', 'تعليم'), ('Protection', 'حماية و الصحة النفسية'), ('Livelihoods and food security', 'سبل العيش واﻷمن الغذائي'), ('Project of clean & water & sanitation ', 'النظافة والمياه والصرف الصحي'), ('Development', 'تنمية و بناء قدرات و ثقافة'), ('Law & suport & policy', 'المواطنة و الحوكمة و الديموقراطية و السلام و السياسة'), ('Donors and support volunteering', 'اﻷسرة و الجندرة و قضايا المرأة'), ('Religious org', 'المأوى و البنة التحتية'), ('Prof association and assembles', 'تنسيق و تجمعات المجتمع المدني'), ('Health', 'صحة'), ('Studies and research', 'دراسات وأبحاث'), ('Other', 'أخرى')], max_length=255, verbose_name='قطاع المنحة'),
        ),
        migrations.AlterField(
            model_name='orgjob',
            name='job_domain',
            field=models.CharField(choices=[('Media', 'اﻹعلام و المناصرة'), ('Education', 'تعليم'), ('Protection', 'حماية و الصحة النفسية'), ('Livelihoods and food security', 'سبل العيش واﻷمن الغذائي'), ('Project of clean & water & sanitation ', 'النظافة والمياه والصرف الصحي'), ('Development', 'تنمية و بناء قدرات و ثقافة'), ('Law & suport & policy', 'المواطنة و الحوكمة و الديموقراطية و السلام و السياسة'), ('Donors and support volunteering', 'اﻷسرة و الجندرة و قضايا المرأة'), ('Religious org', 'المأوى و البنة التحتية'), ('Prof association and assembles', 'تنسيق و تجمعات المجتمع المدني'), ('Health', 'صحة'), ('Studies and research', 'دراسات وأبحاث'), ('Other', 'أخرى')], max_length=255, verbose_name='مجال العمل'),
        ),
        migrations.AlterField(
            model_name='orgmedia',
            name='org_name',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='orgs.orgprofile', verbose_name='اسم المنظمة'),
        ),
        migrations.AlterField(
            model_name='orgprofile',
            name='target_cat',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('No category selected', 'لا يوجد فئة محددة'), ('womans', 'نساء'), ('Mans', 'رجال'), ('Youth 18-24', 'شباب 18-24'), ('Child 0-18', 'أطفال 0-18'), ('Religious groups', 'مجموعات دینیة'), ('Ethnic groups', 'مجموعة عرقیة'), ('Persons lacking breadwinner ', 'فاقدي المعیل'), ('Handicapped', 'ذوي الاحتیاجات الخاصة'), ('Refugees', 'لاجئین'), ('Displaced', 'نازحین'), ('Returned', 'عائدین'), ('Other civil society organizations', 'منظمات مجتمع مدني اخرى'), ('Other', 'أخرى')], max_length=255, verbose_name='الفئات المستهدفة'),
        ),
        migrations.AlterField(
            model_name='orgprofile',
            name='user',
            field=models.ForeignKey(blank=True, help_text='المستخدمون الذين ليس لديهم طلبات بروفايل فقط', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='اسم المستخدم'),
        ),
        migrations.AlterField(
            model_name='orgprofile',
            name='work_domain',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('Media', 'اﻹعلام و المناصرة'), ('Education', 'تعليم'), ('Protection', 'حماية و الصحة النفسية'), ('Livelihoods and food security', 'سبل العيش واﻷمن الغذائي'), ('Project of clean & water & sanitation ', 'النظافة والمياه والصرف الصحي'), ('Development', 'تنمية و بناء قدرات و ثقافة'), ('Law & suport & policy', 'المواطنة و الحوكمة و الديموقراطية و السلام و السياسة'), ('Donors and support volunteering', 'اﻷسرة و الجندرة و قضايا المرأة'), ('Religious org', 'المأوى و البنة التحتية'), ('Prof association and assembles', 'تنسيق و تجمعات المجتمع المدني'), ('Health', 'صحة'), ('Studies and research', 'دراسات وأبحاث'), ('Other', 'أخرى')], max_length=255, verbose_name='مجال العمل'),
        ),
        migrations.AlterField(
            model_name='orgrapport',
            name='domain',
            field=models.CharField(choices=[('Media', 'اﻹعلام و المناصرة'), ('Education', 'تعليم'), ('Protection', 'حماية و الصحة النفسية'), ('Livelihoods and food security', 'سبل العيش واﻷمن الغذائي'), ('Project of clean & water & sanitation ', 'النظافة والمياه والصرف الصحي'), ('Development', 'تنمية و بناء قدرات و ثقافة'), ('Law & suport & policy', 'المواطنة و الحوكمة و الديموقراطية و السلام و السياسة'), ('Donors and support volunteering', 'اﻷسرة و الجندرة و قضايا المرأة'), ('Religious org', 'المأوى و البنة التحتية'), ('Prof association and assembles', 'تنسيق و تجمعات المجتمع المدني'), ('Health', 'صحة'), ('Studies and research', 'دراسات وأبحاث'), ('Other', 'أخرى')], max_length=150, verbose_name='مجال التقرير'),
        ),
        migrations.AlterField(
            model_name='orgresearch',
            name='domaine',
            field=models.CharField(choices=[('Media', 'اﻹعلام و المناصرة'), ('Education', 'تعليم'), ('Protection', 'حماية و الصحة النفسية'), ('Livelihoods and food security', 'سبل العيش واﻷمن الغذائي'), ('Project of clean & water & sanitation ', 'النظافة والمياه والصرف الصحي'), ('Development', 'تنمية و بناء قدرات و ثقافة'), ('Law & suport & policy', 'المواطنة و الحوكمة و الديموقراطية و السلام و السياسة'), ('Donors and support volunteering', 'اﻷسرة و الجندرة و قضايا المرأة'), ('Religious org', 'المأوى و البنة التحتية'), ('Prof association and assembles', 'تنسيق و تجمعات المجتمع المدني'), ('Health', 'صحة'), ('Studies and research', 'دراسات وأبحاث'), ('Other', 'أخرى')], max_length=150, verbose_name='مجال البحث'),
        ),
        migrations.AlterField(
            model_name='orgresearch',
            name='media',
            field=models.FileField(upload_to='rapport_files', verbose_name='ملف أو صورة البحث'),
        ),
        migrations.AlterField(
            model_name='persfundingopp',
            name='domain',
            field=models.CharField(blank=True, choices=[('Media', 'اﻹعلام و المناصرة'), ('Education', 'تعليم'), ('Protection', 'حماية و الصحة النفسية'), ('Livelihoods and food security', 'سبل العيش واﻷمن الغذائي'), ('Project of clean & water & sanitation ', 'النظافة والمياه والصرف الصحي'), ('Development', 'تنمية و بناء قدرات و ثقافة'), ('Law & suport & policy', 'المواطنة و الحوكمة و الديموقراطية و السلام و السياسة'), ('Donors and support volunteering', 'اﻷسرة و الجندرة و قضايا المرأة'), ('Religious org', 'المأوى و البنة التحتية'), ('Prof association and assembles', 'تنسيق و تجمعات المجتمع المدني'), ('Health', 'صحة'), ('Studies and research', 'دراسات وأبحاث'), ('Other', 'أخرى')], max_length=255, null=True, verbose_name='قطاع المنحة'),
        ),
    ]
