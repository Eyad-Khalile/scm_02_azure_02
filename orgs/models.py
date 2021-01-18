from django.urls import reverse
import PIL
from django.core.files.storage import default_storage as storage
from multiselectfield import MultiSelectField
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_countries.fields import CountryField
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator
from PIL import Image
from django.core.mail import send_mail
from django.template.loader import get_template
from django.template import Context
from django.conf import settings
import os
from ckeditor.fields import RichTextField


# https://github.com/akjasim/cb_dj_dependent_dropdown


class MyChoices(models.Model):
    country_CHOICES = (
        ('IQ', _('العراق')),
        ('LB', _('لبنان')),
        ('JO', _('اﻷردن')),
        ('TR', _('تركيا')),
        ('SY', _('سوريا')),
    )

    type_CHOICES = (
        ('establishment', _('مؤسسة')),
        ('org', _('جمعية أو منظمة')),
        ('team', _('مبادرة / فريق')),
        ('union', _('اتحاد / تحالف / تجمع')),
        ('group', _('لجنة / تنسيقية / مجموعة'))
    )

    syr_city_CHOICES = (
        ('aleppo', _('حلب')),
        ('damascus', _('دمشق')),
        ('suburb of damascus', _('ريف دمشق')),
        ('daraa', _('درعا')),
        ('deir ez-Zor', _('دير الزور')),
        ('hama', _('حماه')),
        ('al-Hasakah', _('الحسكة')),
        ('homs', _('حمص')),
        ('idlib', _('إدلب')),
        ('latakia', _('اللاذقية')),
        ('quneitra', _('القنيطرة')),
        ('raqqa', _('الرقة')),
        ('as-Suwayda', _('السويداء')),
        ('tartus', _('طرطوس')),
    )

    turky_city_CHOICES = (
        ('Adana', _('أضنة')),
        ('Adıyaman', _('أديامان')),
        ('Afyon', _('أفيون')),
        ('Ağrı', _('أغري')),
        ('Amasya', _('أماسيا')),
        ('Ankara', _('أنقرة')),
        ('Antalya', _('أنطاليا')),
        ('Artvin', _('أرتوين')),
        ('Aydın', _('أيطن')),
        ('Balıkesir', _('بالق أسير')),
        ('Bilecik', _('بيله جك')),
        ('Bingöl', _('بينكُل')),
        ('Bitlis', _('بيطليس')),
        ('Bolu', _('بولو')),
        ('Burdur', _('بوردور')),
        ('Bursa', _('بورصة')),
        ('Çanakkale', _('جاناكالي')),
        ('Çankırı', _('جانقري')),
        ('Çorum', _('جوروم')),
        ('Denizli', _('دنيزلي')),
        ('Diyarbakır', _('ديار بكر')),
        ('Edirne', _('أدرنة')),
        ('Elazığ', _('إلازِغ')),
        ('Erzincan', _('أرزينجان')),
        ('Erzurum', _('أرضروم')),
        ('Eskişehir', _('أسكي شهر')),
        ('Gaziantep', _('غازي عينتاب')),
        ('Giresun', _('غيرسون')),
        ('Gümüşhane', _('كوموش خانة')),
        ('Hakkari', _('حقاري')),
        ('Hattay', _('خطاي')),
        ('Isparta', _('إسبرطة')),
        ('Mersin', _('مرسين')),
        ('İstanbul', _('إسطنبول')),
        ('İzmir', _('إزمير')),
        ('Kars', _('كارس')),
        ('Kastamonu', _('قسطموني')),
        ('Kayseri', _('قيصرية')),
        ('Kırklareli', _('كيركلاريلي')),
        ('Kırşehir', _('قرشهر')),
        ('Kocaeli', _('قوجه ايلي')),
        ('Konya', _('قونية')),
        ('Kütahya', _('كوتاهيا')),
        ('Malatya', _('ملاطية')),
        ('Manisa', _('مانيسا')),
        ('Kahramanmaraş', _('كارامان')),
        ('Mardin', _('ماردين')),
        ('Muğla', _('موغلا')),
        ('Muş', _('موس')),
        ('Nevşehir', _('نوشهر')),
        ('Niğde', _('نيدا')),
        ('Ordu', _('أردو')),
        ('Rize', _('ريزه')),
        ('Sakarya', _('صقاريا')),
        ('Samsun', _('سامسون')),
        ('Siirt', _('سيرت')),
        ('Sinop', _('سينوب')),
        ('Sivas', _('سيواس')),
        ('Tekirdağ', _('تكيرطاغ')),
        ('Tokat', _('توكات')),
        ('Trabzon', _('طرابزون')),
        ('Tunceli', _('تونجلي')),
        ('Şanlıurfa', _('شانلي أورفا')),
        ('Uşak', _('أوشاك')),
        ('Van', _('وان')),
        ('Yozgat', _('يوزكات')),
        ('Zonguldak', _('زونغولداك')),
        ('Aksaray', _('أق سراي')),
        ('Bayburt', _('بايبورت')),
        ('Karaman', _('قرة مان')),
        ('Kırıkkale', _('كيرِك قلعة')),
        ('Batman', _('باتمان')),
        ('Şırnak', _('شرناق')),
        ('Bartın', _('بارتين')),
        ('Ardahan', _('أرض خان')),
        ('Iğdır', _('إغدير')),
        ('Yalova', _('يالوفا')),
        ('Karabük', _('قرة بوك')),
        ('Kilis', _('كيليس')),
        ('Osmaniye', _('عثمانية')),
        ('Düzce', _('دوزجه')),
    )

    jordan_city_CHOICES = (
        ('irbid', _('إربد')),
        ('balka', _('البلقاء')),
        ('jerash', _('جرش')),
        ('zarqa', _('الزرقاء')),
        ('tafilah', _('الطفيلة')),
        ('ajlon', _('عجلون')),
        ('aqaba', _('العقبة')),
        ('amman', _('عمان')),
        ('karak', _('الكرك')),
        ('madaba', _('مادبا')),
        ('ma`an', _('معان')),
        ('mafraq', _('المفرق')),
    )

    liban_city_CHOICES = (
        ('Beirut', _('بيروت')),
        ('Mount Lebanon', _('جبل لبنان')),
        ('North', _('لبنان الشمالي')),
        ('South', _('لبنان الجنوبي')),
        ('Beqaa', _('البقاع')),
        ('Nabatieh', _('النبطية')),
        ('Akkar', _('عكار')),
        ('Baalbek-Hermel', _('بعبلك الهرمل')),
        ('kiserwan', _('كسروان جبيل')),
    )

    iraq_city_CHOICES = (
        ('Erbil', _('أربيل')),
        ('Al Anbar', _('اﻷنبار')),
        ('Babil', _('بابل')),
        ('Baghdad', _('بغداد')),
        ('Basra', _('البصرة')),
        ('Halabja', _('حلبجة')),
        ('Duhok', _('دهوك')),
        ('Al-Qādisiyyah', _('القادسية')),
        ('Diyala', _('ديالي')),
        ('Dhi Qar', _('ذي قار')),
        ('Sulaymaniyah', _('السليمانية')),
        ('Saladin', _('صلاح الدين')),
        ('Kirkuk', _('كركوك')),
        ('Karbala', _('كربلاء')),
        ('Muthanna', _('المثنى')),
        ('Maysan', _('ميسان')),
        ('Najaf', _('النجف')),
        ('Nineveh', _('نينوى')),
        ('Wasit', _('واسط')),
    )

    domain_CHOICES = (
        ('Media', _('اﻹعلام و المناصرة')),
        ('Education', _('تعليم')),
        ('Protection', _('حماية و الصحة النفسية')),
        ('Livelihoods and food security', _('سبل العيش واﻷمن الغذائي')),
        ('Project of clean & water & sanitation',
         _('النظافة والمياه والصرف الصحي')),
        ('Development', _('تنمية و بناء قدرات و ثقافة')),
        ('Law & suport & policy', _(
            'المواطنة و الحوكمة و الديموقراطية و السلام و السياسة')),
        ('Donors and support volunteering', _('اﻷسرة و الجندرة و قضايا المرأة')),
        ('Religious org', _('المأوى و البنة التحتية')),
        ('Prof association and assembles', _('تنسيق و تجمعات المجتمع المدني')),
        ('Health', _('صحة')),
        ('Studies and research', _('دراسات وأبحاث')),
        ('Other', _('أخرى')),
    )

    target_CHOICES = (
        ('No category selected', _('لا يوجد فئة محددة')),
        ('womans', _('نساء')),
        ('Mans', _('رجال')),
        ('Youth 18-24', _('شباب 18-24')),
        ('Child 0-18', _('أطفال 0-18')),
        ('Religious groups', _('مجموعات دینیة')),
        ('Ethnic groups', _('مجموعة عرقیة')),
        ('Persons lacking breadwinner', _('فاقدي المعیل')),
        ('Handicapped', _('ذوي الاحتیاجات الخاصة')),
        ('Refugees', _('لاجئین')),
        ('Displaced', _('نازحین')),
        ('Returned', _('عائدین')),
        ('Other civil society organizations', _('منظمات مجتمع مدني اخرى')),
        ('Other', _('أخرى')),
    )

    bool_CHOICES = (
        ('0', _('لا')),
        ('1', _('نعم')),
    )

    polic_CHOICES = (
        ('No', _('لا يوجد')),
        ('Code of conduct', _('مدونة السلوك')),
        ('Child protection', _('حماية الطفل')),
        ('Anti-corruption', _('مكافحة الفساد')),
        ('Human resources policy', _('سياسة الموارد البشرية')),
        ('Procurement policy', _('سياسة المشتريات')),
        ('Volunteering policy', _('سياسة التطوع')),
        ('Anti-harassment Policy', _('سياسة منع التحرش')),
        ('Financial policy', _('السياسة المالية')),
        ('Equipment use Policy', _('سياسة استخدام المعدات')),
        ('privacy policy', _('سياسة الخصوصية')),
        ('Other', _('أخرى')),
    )

    # JOBS
    job_CHOICES = (
        ('Full time', _('دوام كامل')),
        ('Part time', _('دوام جزئي')),
        ('Expert', _('استشاري')),
        ('Traning', _('تدريب')),
        ('Volunteering', _('تطوع')),
        ('Fellowship', _('زمالة')),

    )
    expereince_CHOICES = (
        ('Not necessary', _('الخبرة غير ضرورية')),
        ('1-2 year', _('1-2 سنة')),
        ('2-5 years', _('2-5 سنة')),
        ('5-9 years', _('5-9 سنة')),
        ('up of 10 years', _('10 وفوق')),
        ('Othre', _('أخرى')),
    )

    # FUND ORGS
    period_CHOICES = (
        ('less of 6 months', _('أقل من 6 أشهر')),
        ('from 6 mths to one year', _('ستة أشهر لسنة')),
        ('from one to 2 years', _('سنة إلى سنتين')),
        ('more than 2 years', _('أكثر من سنتين')),
        ('other', _('أخرى')),
    )
    amount_CHOICES = (
        ('less than 5000 ', _('أقل من 5000 دولار')),
        ('from 5000 to 10000 dollar', _('بين 5000 و 10000 دولار')),
        ('from 10000 to 50000', _('بين 10000 و50000 دولار')),
        ('from 50000 to 100000', _('بين 50000 و100000 دولار')),
        ('more than  100000', _('بين 50000 و100000 دولار')),
        ('other', _('أخرى')),
    )

    # FUND PERSO
    cat_CHOICES = (
        ('total', _('كلية')),
        ('part', _('جزئية')),
    )
    fund_perso_type_CHOICES = (
        ('study', _('دراسية')),
        ('prod', _('انتاجية')),
        ('study & reserch', _('دراسات و أبحاث')),
    )
    level_study_CHOICES = (
        ('licence', _('إجازة جامعية')),
        ('m1', _('دبلوم')),
        ('m2', _('ماجيستير')),
        ('doctorat', _('دكتوراه')),
    )
    comp_study_CHOICES = (
        ('1', _('إعلام/ اتصالات/ علاقات عامة')),
        ('2', _('أعمال وإدارة')),
        ('3', _('اقتصاد/ محاسبة')),
        ('4', _('تعليم/ تربية/ رياض أطفال')),
        ('5', _('حاسوب وتكنولوجيا المعلومات')),
        ('6', _('دراسات إسلامية')),
        ('7', _('دراسات إنسانية/ لغات')),
        ('8', _('زراعة وعلوم بيئية')),
        ('9', _('سياحة وعلوم فندقية')),
        ('10', _('علوم إنسانية')),
        ('11', _('علوم طبية/ طب/ صيدلة/ تمريض')),
        ('12', _('علوم طبيعية')),
        ('13', _('عمارة وتصميم')),
        ('14', _('فنون ومسارح وموسيقى')),
        ('15', _('قانون ودراسات قانونية')),
        ('16', _('هندسة وعلوم هندسية')),
    )
    lang_CHOICES = (
        ('ar', _('عربي')),
        ('en', _('English')),
        ('ku', _('Kurdî')),
    )

# PROFILE / AUTO CREATE
class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.user:
            return self.user.username


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


# :::::::::::: CITYES ::::::::::::::::::::::
class City(models.Model):

    position_work = models.CharField(
        max_length=150, null=False, default=None, choices=MyChoices.country_CHOICES, verbose_name=_('الدولة'))
    city_work = models.CharField(max_length=255, null=False,
                                 verbose_name=_('اسم المحافظة'))
    city_work_en = models.CharField(max_length=255, null=True, blank=True, default='',
                                    verbose_name=_('اسم المدينة بالانكليزية'))
    city_work_ku = models.CharField(max_length=255, null=True, blank=True, default='',
                                    verbose_name=_('اسم المدينة بالكردية'))

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True, default=None)

    def __str__(self):
        if self.city_work:
            return self.city_work


# :::::::::::: ORGS PROFILE ::::::::::::::::::::::
class OrgProfile(models.Model):

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, verbose_name=_("اسم المستخدم"), help_text=_('المستخدمون الذين ليس لديهم طلبات بروفايل فقط'))

    staff = models.CharField(max_length=100, null=True, blank=True)

    name = models.CharField(max_length=255, null=False,
                            verbose_name=_("اسم المنظمة"))
    name_en_ku = models.CharField(max_length=255, null=True, blank=True,
                                  verbose_name=_("اسم المنظمة باللغة الانكليزية أو الكردية"))
    short_cut = models.CharField(
        max_length=255, null=True, blank=True, verbose_name=_("الاسم المختصر"))
    org_type = models.CharField(
        max_length=150, null=False, choices=MyChoices.type_CHOICES, verbose_name=_("نوع المنظمة"))

    # position_work = CountryField(
    #     max_length=255, null=False, verbose_name=_("مكان العمل"))

    # city_work = models.ForeignKey(
    #     City, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("المحافظة"))
    # city_work = models.CharField(
    #     max_length=150, choices=syr_city_CHOICES, null=True, blank=True, verbose_name=_("المحافظة"))

    # position = models.ForeignKey(
    #     Position, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('مكان العمل'))

    logo = models.ImageField(upload_to="org_logos",
                             null=True, blank=True, default='org_logos/default_logo.jpg', verbose_name=_("شعار المنظمة"))
    message = RichTextField(
        max_length=5000, null=False, verbose_name=_("الرؤية و الرسالة"))

    name_managing_director = models.CharField(
        max_length=255, null=True, blank=True, verbose_name=_("اسم رئيس مجلس اﻹدارة"))
    name_ceo = models.CharField(
        max_length=255, null=True, blank=True, verbose_name=_('اسم المدير التنفيذي'))

    # CONTACT INFO
    site_web = models.URLField(
        max_length=255, null=True, blank=True, verbose_name=_('الموقع الالكتروني'))
    facebook = models.URLField(
        max_length=255, null=True, blank=True, verbose_name=_('صفحة فيسبوك'))
    twitter = models.URLField(
        max_length=255, null=True, blank=True, verbose_name=_('صفحة تويتر'))
    email = models.EmailField(max_length=255, null=True,
                              blank=True, verbose_name=_('البريد الاكتروني'))
    phone = models.CharField(max_length=100, null=True,
                             blank=True, verbose_name=_('رقم الهاتف'))
    name_person_contact = models.CharField(
        max_length=255, null=True, blank=True, verbose_name=_('اسم الشخص المسؤول عن التواصل'))
    email_person_contact = models.EmailField(
        max_length=255, null=True, blank=True, verbose_name=_('البريد الاكتروني للشخص المسؤول عن التواصل'))
    org_adress = models.CharField(
        max_length=255, null=False, verbose_name=_('عنوان المقر الرئيسي'))

    # ORG INFO
    work_domain = MultiSelectField(
        max_length=255, choices=MyChoices.domain_CHOICES, null=False, verbose_name=_('مجال العمل'))
    target_cat = MultiSelectField(
        max_length=255, null=False, choices=MyChoices.target_CHOICES, verbose_name=_('الفئات المستهدفة'))
    date_of_establishment = models.CharField(
        max_length=150, null=True, blank=True, verbose_name=_('تاريخ سنة التأسيس'))
    is_org_registered = models.CharField(
        max_length=100, null=False, choices=MyChoices.bool_CHOICES, verbose_name=_('هل المنظمة مسجلة ؟'))
    org_registered_country = CountryField(
        max_length=255, null=True, blank=True, verbose_name=_("بلد التسجيل"))

    org_members_count = models.PositiveIntegerField(
        validators=[MinValueValidator(1)], null=True, blank=True, verbose_name=_('عدد اﻷعضاء'))
    org_members_womans_count = models.PositiveIntegerField(
        validators=[MinValueValidator(1)], null=True, blank=True, verbose_name=_('عدد النساء من اﻷعضاء'))
    w_polic_regulations = MultiSelectField(
        max_length=200, null=False, choices=MyChoices.polic_CHOICES, verbose_name=_('السياسات واللوائح المكتوبة'))
    org_member_with = models.CharField(max_length=100, null=True, blank=True, choices=MyChoices.bool_CHOICES, verbose_name=_(
        'ھل المؤسسة عضو في اي شبكة او تحالف او جسم تنسیقي؟'))
    coalition_name = models.CharField(
        max_length=255, null=True, blank=True, verbose_name=_('اسم الشبكة / التحالف'))

    publish = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(blank=True, null=True, default=None)
    updated_at = models.DateTimeField(blank=True, null=True, default=None)

    def __str__(self):
        if self.name:
            # return '%s %s' % (self.name, self.user.username)
            # return '%s' % (self.user.username) + ' / ' + '%s' % (self.name)
            return self.name

    def get_absolute_url(self):
        return reverse("particip_detail", kwargs={"par_id": self.id})

    # def formatted_phone(self, country=None):
    #     return phonenumbers.parse(self.phone, country)

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     if self.work_domain:
    #         self.work_domain = eval(self.work_domain)

    # def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
    #     super().save(force_insert, force_update, using, update_fields)
    #     path = 'https://scgmedia.blob.core.windows.net/media'
    #     img = Image.open(self.logo.path)
    #     img = Image.open(self.logo.path)
    #     if img.height > 300 or img.width > 300:
    #         output_size = (300, 300)
    #         img.thumbnail(output_size)
    #         img.save(self.logo.path)

# :::::::::::: POSITION OF WORKS ::::::::::::::::::::::


class Position(models.Model):

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, verbose_name=_("اسم المستخدم"))
    org_profile = models.ForeignKey(
        OrgProfile, on_delete=models.CASCADE, null=True, blank=True, verbose_name=_("اسم المنظمة"))

    # org_id = models.IntegerField(
    #     max_length=100, null=True, blank=True, default=None)

    position_work = CountryField(
        max_length=255, null=True, blank=True, verbose_name=_("مكان العمل"))
    city_work = models.ForeignKey(
        City, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("المحافظة"))

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True, default=None)

    def __str__(self):
        return '%s %s' % (self.position_work, self.city_work)


# :::::::::::::: ORGS NEWS ::::::::::::::::
class OrgNews(models.Model):
    lang = models.CharField(max_length=100, choices=MyChoices.lang_CHOICES, null=False, blank=False, default='ar', verbose_name=_('اللغة'))
    user = models.ForeignKey(
        User, on_delete=models.CASCADE)
    staff = models.CharField(max_length=100, null=True, blank=True)
    org_name = models.ForeignKey(
        OrgProfile, on_delete=models.CASCADE, null=False, blank=True, verbose_name=_('اسم المنظمة'))

    title = models.CharField(max_length=255, null=False,
                             verbose_name=_('عنوان الخبر'))
    content = RichTextField(
        max_length=5000, null=False, verbose_name=_('تفاصيل الخبر'))
    image = models.ImageField(upload_to="news_images",
                              null=False, default='news_images/article_img.jpg', verbose_name=_("صورة الخبر"))

    publish = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(blank=True, null=True, default=None)
    updated_at = models.DateTimeField(blank=True, null=True, default=None)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("news_detail", kwargs={"news_id": self.id})

    # def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
    #     super().save(force_insert, force_update, using, update_fields)
    #     path = 'https://scgmedia.blob.core.windows.net/media'
    #     img = Image.open(self.image.path)
    #     if img.height > 1000 or img.width > 1000:
    #         output_size = (1000, 1000)
    #         img.thumbnail(output_size)
    #         img.save(self.image.path)


# :::::::::: ORGS RAPPORT :::::::::::::::::
class OrgRapport(models.Model):
    lang = models.CharField(max_length=100, choices=MyChoices.lang_CHOICES,
                            null=False, blank=False, default='ar', verbose_name=_('اللغة'))
    user = models.ForeignKey(
        User, on_delete=models.CASCADE)
    staff = models.CharField(max_length=100, null=True, blank=True)
    org_name = models.ForeignKey(
        OrgProfile, on_delete=models.CASCADE, null=False, blank=True, verbose_name=_('اسم المنظمة'))

    title = models.CharField(max_length=255, null=False,
                             verbose_name=_('عنوان التقرير'))
    domain = models.CharField(
        max_length=150, null=False, blank=False, choices=MyChoices.domain_CHOICES, verbose_name=_('مجال التقرير'))
    media = models.FileField(upload_to="rapport_files",
                             verbose_name=_('صورة او ملف التقرير'))

    publish = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(blank=True, null=True, default=None)
    updated_at = models.DateTimeField(blank=True, null=True, default=None)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("orgs_rapport_detail", kwargs={"rapport_id": self.id})

    # def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
    #     super().save(force_insert, force_update, using, update_fields)
    #     extension = os.path.splitext(self.media.name)
    #     # path = 'https://scgmedia.blob.core.windows.net/media'
    #     if not '.pdf' in list(extension):
    #         img = Image.open(self.media)
    #         if img.height > 1600 or img.width > 1600:
    #             # output_size = (1600, 1600)
    #             # img.thumbnail(output_size)
    #             # print('=========', img)
    #             # img.save(self.media.path)
    #             # img.thumbnail(output_size, PIL.Image.ANTIALIAS)
    #             # fh = storage.open(self.media.name, "wb")
    #             # img.save(fh)
    #             # fh.close()
    #             img = Image.open(self.media)
    #             resized_image = img.resize((1600, 1600), PIL.Image.ANTIALIAS)

    #             fh = storage.open(self.media.name, "wb")
    #             # picture_format = 'jpg'
    #             resized_image.save(fh)
    #             fh.close()

    # def delete(self, force_insert=False, force_update=False, using=None, update_fields=None):
    #     self.media.delete()
    #     super().delete(force_insert, force_update, using, update_fields)


# :::::::::: ORGS DATA :::::::::::::::::
class OrgData(models.Model):
    lang = models.CharField(max_length=100, choices=MyChoices.lang_CHOICES,
                            null=False, blank=False, default='ar', verbose_name=_('اللغة'))
    user = models.ForeignKey(
        User, on_delete=models.CASCADE)
    staff = models.CharField(max_length=100, null=True, blank=True)
    org_name = models.ForeignKey(
        OrgProfile, on_delete=models.CASCADE, null=False, blank=True, verbose_name=_('اسم المنظمة'))

    title = models.CharField(max_length=255, null=False,
                             verbose_name=_('عنوان البيان'))
    media = models.FileField(upload_to="rapport_files",
                             verbose_name=_('صورة او ملف البيان'))

    publish = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(blank=True, null=True, default=None)
    updated_at = models.DateTimeField(blank=True, null=True, default=None)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("data_detail", kwargs={"data_id": self.id})

    # def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
    #     super().save(force_insert, force_update, using, update_fields)
    #     extension = os.path.splitext(self.media.name)
    #     path = 'https://scgmedia.blob.core.windows.net/media'
    #     if not '.pdf' in list(extension):
    #         img = Image.open(self.media.path)
    #         if img.height > 1600 or img.width > 1600:
    #             output_size = (1600, 1600)
    #             img.thumbnail(output_size)
    #             img.save(self.media.path)


# :::::::::: ORGS MEDIA :::::::::::::::::
class OrgMedia(models.Model):
    lang = models.CharField(max_length=100, choices=MyChoices.lang_CHOICES,
                            null=False, blank=False, default='ar', verbose_name=_('اللغة'))
    user = models.ForeignKey(
        User, on_delete=models.CASCADE)
    staff = models.CharField(max_length=100, null=True, blank=True)
    org_name = models.ForeignKey(
        OrgProfile, on_delete=models.CASCADE, null=False, blank=True, verbose_name=_('اسم المنظمة'))

    title = models.CharField(max_length=255, null=False,
                             verbose_name=_('عنوان المحتوى'))
    media = models.FileField(upload_to="rapport_files",
                             verbose_name=_('صورة او ملف المحتوى'))
    url = models.URLField(blank=True, max_length=255,
                          null=True, verbose_name=_('رابط المحتوى'))

    publish = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(blank=True, null=True, default=None)
    updated_at = models.DateTimeField(blank=True, null=True, default=None)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("media_detail", kwargs={"media_id": self.id})

    # def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
    #     super().save(force_insert, force_update, using, update_fields)
    #     extension = os.path.splitext(self.media.name)
    #     path = 'https://scgmedia.blob.core.windows.net/media'
    #     if not '.pdf' in list(extension):
    #         img = Image.open(self.media.path)
    #         if img.height > 1600 or img.width > 1600:
    #             output_size = (1600, 1600)
    #             img.thumbnail(output_size)
    #             img.save(self.media.path)


# :::::::::: ORGS RESEARCH :::::::::::::::::
class OrgResearch(models.Model):

    lang = models.CharField(max_length=100, choices=MyChoices.lang_CHOICES,
                            null=False, blank=False, default='ar', verbose_name=_('اللغة'))
    user = models.ForeignKey(
        User, on_delete=models.CASCADE)
    # org_name = models.ForeignKey(
    #     OrgProfile, on_delete=models.CASCADE, null=False, blank=True)
    staff = models.CharField(max_length=100, null=True, blank=True)

    name_entity = models.CharField(
        max_length=255, null=False,  verbose_name=_('اسم الجهة'))

    title = models.CharField(max_length=255, null=False,
                             verbose_name=_('عنوان البحث'))
    domaine = models.CharField(max_length=150, null=False, blank=False,
                               choices=MyChoices.domain_CHOICES, verbose_name=_('مجال البحث'))
    media = models.FileField(upload_to="rapport_files",
                             verbose_name=_('ملف أو صورة البحث'))
    url = models.URLField(blank=True, max_length=255,
                          null=True, verbose_name=_('رابط البحث'))

    publish = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(blank=True, null=True, default=None)
    updated_at = models.DateTimeField(blank=True, null=True, default=None)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("research_detail", kwargs={"research_id": self.id})

    # def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
    #     super().save(force_insert, force_update, using, update_fields)
    #     extension = os.path.splitext(self.media.name)
    #     path = 'https://scgmedia.blob.core.windows.net/media'
    #     if not '.pdf' in list(extension):
    #         img = Image.open(self.media.path)
    #         if img.height > 1600 or img.width > 1600:
    #             output_size = (1600, 1600)
    #             img.thumbnail(output_size)
    #             img.save(self.media.path)


# here is the sources of civiltey gate
# add post (job opri)


# OTHER ORGS
class OtherOrgs(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(
        max_length=255, null=True, blank=True, verbose_name=_('اضف اسم المنظمة اﻷخرى'))
    logo = models.ImageField(upload_to="other_org_logos",
                             null=True, blank=True, default='org_logos/default_logo.jpg', verbose_name=_("شعار المنظمة"))

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True, default=None)

    def __str__(self):
        return self.name

    # def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
    #     super().save(force_insert, force_update, using, update_fields)
    #     path = 'https://scgmedia.blob.core.windows.net/media'
    #     img = Image.open(self.logo.path)
    #     if img.height > 300 or img.width > 300:
    #         output_size = (300, 300)
    #         img.thumbnail(output_size)
    #         img.save(self.logo.path)


class OrgJob(models.Model):
    lang = models.CharField(max_length=100, choices=MyChoices.lang_CHOICES,
                            null=False, blank=False, default='ar', verbose_name=_('اللغة'))
    user = models.ForeignKey(
        User, on_delete=models.CASCADE)
    staff = models.CharField(max_length=100, null=True, blank=True)
    org_name = models.ForeignKey(
        OrgProfile, on_delete=models.CASCADE, null=True, blank=True, verbose_name=_('اسم المنظمة'))
    other_org_name = models.ForeignKey(
        OtherOrgs, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('اسم المنظمة اﻷخرى'))

    job_title = models.CharField(max_length=255, null=False,
                                 verbose_name=_('عنوان الوظيفة'))
    period_months = models.PositiveIntegerField(
        null=True, blank=True, verbose_name=_('مدة العقد بالأشهر'))
    job_description = RichTextField(
        max_length=5000, null=False, verbose_name=_('وصف الوظيفة'))
    job_type = models.CharField(max_length=255, null=False, choices=MyChoices.job_CHOICES,
                                verbose_name=_('نوع الوظيفة'))
    experience = models.CharField(max_length=255, null=False, choices=MyChoices.expereince_CHOICES,
                                  verbose_name=_('الخبرة'))
    position_work = CountryField(
        max_length=255, null=False, verbose_name=_("مكان العمل"))
    city_work = models.ForeignKey(
        City, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("المحافظة"))
    # job_city = models.CharField(
    #     max_length=150, choices=MyChoices.syr_city_CHOICES, null=True, blank=True, verbose_name=_("المحافظة"))
    job_area = models.CharField(
        max_length=150, null=True, blank=True, verbose_name=_("المنطقة"))
    job_domain = models.CharField(
        max_length=255, choices=MyChoices.domain_CHOICES, null=False, verbose_name=_('مجال العمل'))
    dead_date = models.DateField(
        null=False, default=None, verbose_name=_('تاريخ إغلاق الوظيفة'))
    job_aplay = RichTextField(
        max_length=5000, null=False, verbose_name=_('طريقة التقدم للوظيفة'))

    publish = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(blank=True, null=True, default=None)
    updated_at = models.DateTimeField(blank=True, null=True, default=None)

    def __str__(self):
        return self.job_title

    def get_absolute_url(self):
        return reverse("jobs_detail", kwargs={"job_id": self.id})

    # def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
    #     super().save(force_insert, force_update, using, update_fields)
    #     path = 'https://scgmedia.blob.core.windows.net/media'
    #     img = Image.open(self.logo.path)
    #     if img.height > 300 or img.width > 300:
    #         output_size = (300, 300)
    #         img.thumbnail(output_size)
    #         img.save(self.logo.path)


# Organizations funding opportunities
class OrgFundingOpp(models.Model):
    lang = models.CharField(max_length=100, choices=MyChoices.lang_CHOICES,
                            null=False, blank=False, default='ar', verbose_name=_('اللغة'))
    user = models.ForeignKey(
        User, on_delete=models.CASCADE)
    staff = models.CharField(max_length=100, null=True, blank=True)
    org_name = models.ForeignKey(
        OrgProfile, on_delete=models.CASCADE, null=True, blank=True, verbose_name=_('اسم المنظمة'))

    name_funding = models.CharField(max_length=255, null=True, blank=True,
                                    verbose_name=_("الجهة المانحة"))
    logo = models.ImageField(upload_to="funding_logos",
                             null=True, blank=True, default='org_logos/default_logo.jpg', verbose_name=_("لوغو الجهة المانحة"))

    funding_org_description = RichTextField(
        max_length=5000, null=False, verbose_name=_("لمحة عن الجهة المانحة"))
    work_domain = models.CharField(
        max_length=255, choices=MyChoices.domain_CHOICES, null=False, verbose_name=_('قطاع المنحة'))
    position_work = CountryField(
        max_length=255, null=False, verbose_name=_("دول المنحة"))
    city_work = models.ForeignKey(
        City, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("المحافظة"))
    funding_dead_date = models.DateField(
        null=False, verbose_name=_('تاريخ إغلاق المنحة'))
    funding_period = models.CharField(
        max_length=255, choices=MyChoices.period_CHOICES, null=False, verbose_name=_('مدة المنحة'))
    funding_amounte = models.CharField(
        max_length=255, choices=MyChoices.amount_CHOICES, null=False, verbose_name=_('حجم المنحة'))

    # RICHTEXT
    funding_description = RichTextField(
        max_length=5000, null=False, verbose_name=_("وصف المنحة"))
    funding_conditions = RichTextField(
        max_length=5000, null=False, verbose_name=_("شروط المنحة"))
    funding_reqs = RichTextField(
        max_length=5000, null=False, verbose_name=_("متطلبات التقديم"))
    funding_guid = RichTextField(
        max_length=5000, null=False, verbose_name=_("كيفية التقديم"))

    funding_url = models.URLField(
        max_length=255, null=True, blank=True, verbose_name=_('الرابط الأصلي'))

    publish = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(blank=True, null=True, default=None)
    updated_at = models.DateTimeField(blank=True, null=True, default=None)

    def __str__(self):
        if self.name_funding:
            return self.name_funding
        else:
            return self.org_name

    def get_absolute_url(self):
        return reverse("funding_detail", kwargs={"funding_id": self.id})

    # def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
    #     super().save(force_insert, force_update, using, update_fields)
    #     path = 'https://scgmedia.blob.core.windows.net/media'
    #     img = Image.open(self.logo.path)
    #     if img.height > 300 or img.width > 300:
    #         output_size = (300, 300)
    #         img.thumbnail(output_size)
    #         img.save(self.logo.path)


# Persons funding opportunities
class PersFundingOpp(models.Model):
    lang = models.CharField(max_length=100, choices=MyChoices.lang_CHOICES,
                            null=False, blank=False, default='ar', verbose_name=_('اللغة'))
    user = models.ForeignKey(
        User, on_delete=models.CASCADE)
    staff = models.CharField(max_length=100, null=True, blank=True)
    org_name = models.ForeignKey(
        OrgProfile, on_delete=models.CASCADE, null=True, blank=True, verbose_name=_('اسم المنظمة'))

    name_funding = models.CharField(max_length=255, null=True, blank=True,
                                    verbose_name=_("الجهة المانحة"))
    logoo = models.ImageField(upload_to="funding_logos",
                              null=True, blank=True, default='org_logos/default_logo.jpg', verbose_name=_("لوغو الجهة المانحة"))

    category = models.CharField(max_length=100, null=True, blank=True,
                                choices=MyChoices.cat_CHOICES, verbose_name=_('فئة المنحة'))
    fund_type = models.CharField(
        max_length=150, null=False, choices=MyChoices.fund_perso_type_CHOICES, verbose_name=_('نوع المنحة'))

    study_level = models.CharField(max_length=255, null=True, blank=True,
                                   choices=MyChoices.level_study_CHOICES, verbose_name=_('المستوى التعليمي'))
    comp_study = models.CharField(max_length=255, null=True, blank=True,
                                  choices=MyChoices.comp_study_CHOICES, verbose_name=_('الاختصاص التعليمي'))
    domain = models.CharField(max_length=255, null=True, blank=True,
                              choices=MyChoices.domain_CHOICES, verbose_name=_('قطاع المنحة'))

    position_work = CountryField(
        max_length=255, null=False, verbose_name=_("دول المنحة"))
    city_work = models.ForeignKey(
        City, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("المحافظة"))

    fund_org_description = RichTextField(
        max_length=5000, null=False, verbose_name=_("لمحة عن الجهة المانحة"))

    funding_dead_date = models.DateField(
        null=False, verbose_name=_('تاريخ إغلاق المنحة'))
    funding_period = models.CharField(
        max_length=255, choices=MyChoices.period_CHOICES, null=False, verbose_name=_('مدة المنحة'))
    funding_amounte = models.CharField(
        max_length=255, choices=MyChoices.amount_CHOICES, null=False, verbose_name=_('حجم المنحة'))

    # RICHTEXT
    funding_description = RichTextField(
        max_length=5000, null=False, verbose_name=_("وصف المنحة"))
    funding_conditions = RichTextField(
        max_length=5000, null=False, verbose_name=_("شروط المنحة"))
    funding_reqs = RichTextField(
        max_length=5000, null=False, verbose_name=_("متطلبات التقديم"))
    funding_guid = RichTextField(
        max_length=5000, null=False, verbose_name=_("كيفية التقديم"))

    funding_url = models.URLField(
        max_length=255, null=True, blank=True, verbose_name=_('الرابط الأصلي'))

    publish = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(blank=True, null=True, default=None)
    updated_at = models.DateTimeField(blank=True, null=True, default=None)

    def __str__(self):
        if self.name_funding:
            return self.name_funding
        else:
            return self.org_name

    def get_absolute_url(self):
        return reverse("finance_perso_detail", kwargs={"pk": self.id})

    # def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
    #     super().save(force_insert, force_update, using, update_fields)
    #     path = 'https://scgmedia.blob.core.windows.net/media'
    #     img = Image.open(self.logo.path)
    #     if img.height > 300 or img.width > 300:
    #         output_size = (300, 300)
    #         img.thumbnail(output_size)
    #         img.save(self.logo.path)


# capacity buildinng for opportunities
class OrgCapacityOpp(models.Model):

    type_CHOICES = (
        ('traning', _('تدريب')),
        ('college', _('زمالة')),
    )

    lang = models.CharField(max_length=100, choices=MyChoices.lang_CHOICES,
                            null=False, blank=False, default='ar', verbose_name=_('اللغة'))
    user = models.ForeignKey(
        User, on_delete=models.CASCADE)
    staff = models.CharField(max_length=100, null=True, blank=True)
    org_name = models.ForeignKey(
        OrgProfile, on_delete=models.CASCADE, null=True, blank=True, verbose_name=_('اسم المنظمة'))

    name_capacity = models.CharField(max_length=255, null=True, blank=True,
                                     verbose_name=_("اسم الجهة الممولة"))
    title_capacity = models.CharField(
        max_length=255, null=False, verbose_name=_("عنوان الفرصة"))
    capacity_description = RichTextField(
        max_length=5000, null=False, verbose_name=_("وصف الفرصة"))
    capacity_type = models.CharField(
        max_length=255, choices=type_CHOICES, null=False, verbose_name=_('نوع الفرصة'))

    # capacity_country = CountryField(
    #     max_length=255, null=False, verbose_name=_("مكان الفرصة"))
    # capacity_city = models.CharField(
    #     max_length=150, choices=MyChoices.syr_city_CHOICES, null=True, blank=True, verbose_name=_("المحافظة"))

    position_work = CountryField(
        max_length=255, null=False, verbose_name=_("مكان الفرصة"))
    city_work = models.ForeignKey(
        City, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("المحافظة"))

    capacity_domain = models.CharField(
        max_length=255, choices=MyChoices.domain_CHOICES, null=False, verbose_name=_('قطاع الفرصة'))
    capacity_dead_date = models.DateField(
        null=False, verbose_name=_('تاريخ إغلاق المنحة'))

    capacity_reqs = RichTextField(
        max_length=5000, null=False, verbose_name=_("متطلبات التقديم"))
    capacity_guid = RichTextField(
        max_length=5000, null=False, verbose_name=_("طريقة التقديم"))

    capacity_url = models.URLField(
        max_length=255, null=True, blank=True, verbose_name=_('الرابط الأصلي'))

    publish = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(blank=True, null=True, default=None)
    updated_at = models.DateTimeField(blank=True, null=True, default=None)

    def __str__(self):
        return self.name_capacity

    def get_absolute_url(self):
        return reverse("capacity_detail", kwargs={"capacity_id": self.id})


# dev guid
class DevOrgOpp(models.Model):

    subject_CHOICES = (
        ('Project development and management', _('تطوير وإدارة المشاريع')),
        ('Organizational governance', _('الحوكمة التنظيمية')),
        ('Advocacy and Campaigns', _('المناصرة والحملات')),
        ('Civil Society Library', _('مكتبة المجتمع المدني')),
        ('other', _('أخرى')),
    )

    lang = models.CharField(max_length=100, choices=MyChoices.lang_CHOICES,
                            null=False, blank=False, default='ar', verbose_name=_('اللغة'))
    user = models.ForeignKey(
        User, on_delete=models.CASCADE)
    staff = models.CharField(max_length=100, null=True, blank=True)
    org_name = models.ForeignKey(
        OrgProfile, on_delete=models.CASCADE, null=True, blank=True, verbose_name=_('اسم المنظمة'))
    name_devv = models.CharField(
        max_length=255, null=True, blank=True, verbose_name=_("اسم الجهة "))

    title_dev = models.CharField(
        max_length=255, null=False, verbose_name=_("عنوان المادة"))
    dev_date = models.DateTimeField(
        null=True, blank=True, verbose_name=_('تاريخ الإعداد/النشر/التأليف'))
    dev_description = RichTextField(
        max_length=5000, null=False, verbose_name=_("لمحة عن الجهة"))

    subject = models.CharField(
        max_length=255, null=False, choices=subject_CHOICES, verbose_name=_("موضوع المادة"))
    content = models.FileField(upload_to="dev_files",
                               null=True, blank=True, default='org_logos/default_logo.jpg', verbose_name=_("المادة "))
    video = models.URLField(max_length=255, null=True,
                            blank=True, verbose_name=_("رابط فيديو"))

    publish = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(blank=True, null=True, default=None)
    updated_at = models.DateTimeField(blank=True, null=True, default=None)

    def __str__(self):
        return self.title_dev

    def get_extension(self):
        title_dev, extension = os.path.splitext(self.content.name)
        return self.extension

    def get_absolute_url(self):
        return reverse("devs_detail", kwargs={"devs_id": self.id})

    # def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
    #     super().save(force_insert, force_update, using, update_fields)
    #     extension = os.path.splitext(self.content.name)
    #     path = 'https://scgmedia.blob.core.windows.net/media'
    #     if not '.pdf' in list(extension):
    #         img = Image.open(self.content.path)
    #         if img.height > 1600 or img.width > 1600:
    #             output_size = (1600, 1600)
    #             img.thumbnail(output_size)
    #             img.save(self.content.path)


# News letter for members in our site
class NewsLetter(models.Model):
    nl_name = models.CharField(max_length=255, null=False,
                               verbose_name=_('الاسم و الكنية'))
    nl_work = models.CharField(max_length=255, null=False,
                               verbose_name=_('العمل'))
    nl_org_name = models.CharField(
        max_length=255, null=True, blank=True, verbose_name=_('اسم المنظمة'))
    nl_email = models.EmailField(
        max_length=255, null=False, verbose_name=_('البريد الاكتروني'))

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# Invitation Modle to invite orgs
class Invitation(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=True,
                            blank=True, verbose_name=_('اسم المنظمة'))
    email = models.EmailField(
        max_length=255, null=False, verbose_name=_('البريد الاكتروني'))

    def __unicode__(self):
        return u'%s, %s' % (self.sender.username, self.email)

    def send(self):
        subject = u'Invitation to join Django Bookmarks'
        template = get_template('orgs/our_news/invitation_email.html')
        context = Context(
            {'name': self.name, 'sender': self.sender.username, })
        message = template.render(context)
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [self.email])
