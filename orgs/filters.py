import django_filters
from django_filters import DateFilter, CharFilter
from .models import OrgProfile, OrgNews, OrgRapport, OrgData, OrgResearch, OrgJob, OrgFundingOpp, OrgCapacityOpp, DevOrgOpp, PersFundingOpp
from django.utils.translation import gettext_lazy as _


from multiselectfield import MultiSelectField

# DOMAIN_CHOICES = tuple(
#     OrgProfile.objects.filter(work_domain__name='work_domain').values_list('id', 'option'))


class OrgsFilter(django_filters.FilterSet):
    domain_CHOICES = (
        ('Media', _('اﻹعلام و المناصرة')),
        ('Education', _('تعليم')),
        ('Protection', _('حماية و الصحة النفسية')),
        ('Livelihoods and food security', _('سبل العيش واﻷمن الغذائي')),
        ('Project of clean ,water, sanitation ', _(
            'النظافة والمياه والصرف الصحي')),
        ('Development', _('تنمية و بناء قدرات و ثقافة')),
        ('Law, suport, policy', _('المواطنة و الحوكمة و الديموقراطية و السلام و السياسة')),
        ('Donors and support volunteering', _('اﻷسرة و الجندرة و قضايا المرأة')),
        ('Religious org', _('المأوى و البنة التحتية')),
        ('Prof association and assembles', _('تنسيق و تجمعات المجتمع المدني')),
        ('Health', _('صحة')),
        ('Studies and research', _('دراسات وأبحاث')),
        ('Other', _('أخرى')),
    )
    # langue
    # language = CharFilter(field_name="language",label='Langue')
    # auther = CharFilter(field_name="auther", lookup_expr='gte',label='Auteur')
    # category = CharFilter(field_name="category", label='Catégorie')
    # sub_category = CharFilter(label='Sous-Catégorie')

    # work_domain = MultiSelectField(choices=MyChoices.domain_CHOICES)

    # work_domain = django_filters.CharFilter(
    #     field_name='work_domain', lookup_expr='gte', method='filter_work_domain', label=_('مجال العمل'))
    #   MultipleChoiceFilter
    # work_domain = django_filters.ModelMultipleChoiceFilter(
    #     method='filter_domain')
    # work_domain = django_filters.MultipleChoiceFilter(choices=DOMAIN_CHOICES,
    #                                                   method='filter_domain')
    work_domain = django_filters.MultipleChoiceFilter(
        choices=domain_CHOICES, lookup_expr='contains', label=_('مجال العمل'))

    start_date = CharFilter(field_name="date_of_establishment",
                            lookup_expr='gte', label=_('تاريخ التأسيس / من :'))
    end_date = CharFilter(field_name="date_of_establishment",
                          lookup_expr='lte', label=_('إلى :'))
    name = CharFilter(field_name="name",
                      lookup_expr='icontains', label=_('اسم المنظمة'))
    start_date_pub = DateFilter(field_name="created_at",
                                lookup_expr='gte', label=_('تاريخ نشر الخبر / من :'))
    end_date_pub = DateFilter(field_name="created_at",
                              lookup_expr='lte', label=_('إلى :'))
    # description = CharFilter(field_name="description",
    #                          lookup_expr='icontains', label='Description')

    # def filter_domain(self, qs, name, value):
    #     result = qs.filter(Q(attribute_values__attribute__name='work_domain',
    #                          attribute_values__value_option__in=value))
    #     return result

    class Meta:
        model = OrgProfile
        fields = [
            'user',
            'staff',
            'name',
            # 'position_work',
            'work_domain',
            'start_date',
            'end_date',
            'target_cat',
            'published_at',
        ]

        # def filter_work_domain(self, queryset, name, work_domain):
        #     return queryset.filter(work_domain__contains=work_domain.split(','))

        # exclude = ['date_published', 'date_updated', 'likes', 'is_published']


class OrgsNewsFilter(django_filters.FilterSet):

    title = CharFilter(field_name="title",
                       lookup_expr='icontains', label=_('كلمات من عنوان الخبر'))
    content = CharFilter(field_name="content",
                         lookup_expr='icontains', label=_('كلمات من تفاصيل الخبر'))

    start_date_pub = DateFilter(field_name="created_at",
                                lookup_expr='gte', label=_('تاريخ نشر الخبر / من :'))
    end_date_pub = DateFilter(field_name="created_at",
                              lookup_expr='lte', label=_('إلى :'))

    class Meta:
        model = OrgNews
        fields = [
            'user',
            'org_name',
            'title',
            'content',
            'start_date_pub',
            'end_date_pub',
        ]


class OrgsRapportFilter(django_filters.FilterSet):

    title = CharFilter(field_name="title",
                       lookup_expr='icontains', label=_('كلمات من عنوان التقرير'))

    start_date_pub = DateFilter(field_name="created_at",
                                lookup_expr='gte', label=_('تاريخ نشر التقرير / من :'))
    end_date_pub = DateFilter(field_name="created_at",
                              lookup_expr='lte', label=_('إلى :'))

    class Meta:
        model = OrgRapport
        fields = [
            'user',
            'org_name',
            'title',
            'domain',
            'start_date_pub',
            'end_date_pub',
        ]


class OrgsDataFilter(django_filters.FilterSet):

    title = CharFilter(field_name="title",
                       lookup_expr='icontains', label=_('كلمات من عنوان البيان'))

    start_date_pub = DateFilter(field_name="created_at",
                                lookup_expr='gte', label=_('تاريخ نشر البيان / من :'))
    end_date_pub = DateFilter(field_name="created_at",
                              lookup_expr='lte', label=_('إلى :'))

    class Meta:
        model = OrgData
        fields = [
            'user',
            'org_name',
            'title',
            'start_date_pub',
            'end_date_pub',
        ]


class OrgsMediaFilter(django_filters.FilterSet):

    title = CharFilter(field_name="title",
                       lookup_expr='icontains', label=_('كلمات من عنوان المحتوى'))

    start_date_pub = DateFilter(field_name="created_at",
                                lookup_expr='gte', label=_('تاريخ نشر المحتوى / من :'))
    end_date_pub = DateFilter(field_name="created_at",
                              lookup_expr='lte', label=_('إلى :'))

    class Meta:
        model = OrgData
        fields = [
            'user',
            'org_name',
            'title',
            'start_date_pub',
            'end_date_pub',
        ]


class OrgsResearchFilter(django_filters.FilterSet):
    name_entity = CharFilter(field_name="name_entity",
                             lookup_expr='icontains', label=_('كلمات من اسم الجهة'))
    title = CharFilter(field_name="title",
                       lookup_expr='icontains', label=_('كلمات من عنوان البحث'))

    start_date_pub = DateFilter(field_name="created_at",
                                lookup_expr='gte', label=_('تاريخ نشر البحث / من :'))
    end_date_pub = DateFilter(field_name="created_at",
                              lookup_expr='lte', label=_('إلى :'))

    class Meta:
        model = OrgResearch
        fields = [
            'user',
            'name_entity',
            'title',
            'domaine',
            'start_date_pub',
            'end_date_pub',
        ]
# resources filters
# job filters


class OrgsJobsFilter(django_filters.FilterSet):

    title = CharFilter(field_name="job_title",
                       lookup_expr='icontains', label=_('كلمات من فرصة العمل  '))
    job_type = CharFilter(field_name="job_title",
                          lookup_expr='icontains', label=_('نوع الوظيفة'))
    experience = CharFilter(field_name="experience",
                            lookup_expr='icontains', label=_('الخبرة'))
    # position_work = CharFilter(field_name="job_country",
    #                            lookup_expr='icontains', label=_('مكان العمل'))
    city_work = CharFilter(field_name="job_country",
                           lookup_expr='icontains', label=_('المحافظة'))
    job_domain = CharFilter(field_name="job_domain",
                            lookup_expr='icontains', label=_('مجال العمل'))
    start_date_pub = DateFilter(field_name="created_at",
                                lookup_expr='gte', label=_('تاريخ نشر فرصة العمل / من :'))
    end_date_pub = DateFilter(field_name="created_at",
                              lookup_expr='lte', label=_('إلى :'))

    class Meta:
        model = OrgJob
        fields = [
            'user',
            'org_name',
            'job_title',
            'job_type',
            'experience',
            'position_work',
            'city_work',
            'job_domain',
            'start_date_pub',
            'end_date_pub',
        ]
# org funding filters


class OrgsFundingFilter(django_filters.FilterSet):

    name_funding = CharFilter(field_name="name_funding",
                              lookup_expr='icontains', label=_('الجهة المانحة'))
    # job_country = CharFilter(field_name="position_work",
    #                          lookup_expr='icontains', label=_('مكان العمل'))
    # job_city = CharFilter(field_name="city_work",
    #                       lookup_expr='icontains', label=_('المحافظة'))
    # work_domain = CharFilter(field_name="work_domain",
    #                          lookup_expr='icontains', label=_('مجال العمل'))
    funding_amounte = CharFilter(field_name="funding_amounte",
                                 lookup_expr='icontains', label=_('حسب المبلغ المالي'))
    start_date_pub = DateFilter(field_name="created_at",
                                lookup_expr='gte', label=_('تاريخ نشر المنحة  / من :'))
    end_date_pub = DateFilter(field_name="created_at",
                              lookup_expr='lte', label=_('إلى :'))

    class Meta:
        model = OrgFundingOpp
        fields = [
            'user',
            'name_funding',
            'funding_org_description',
            'work_domain',
            'position_work',
            'city_work',
            'funding_dead_date',
            'funding_period',
            'funding_amounte',
            'funding_description',
            'funding_conditions',
            'publish',
            'created_at',
            'published_at',
            'updated_at'
        ]
# org capacity filters


class OrgsCapacityFilter(django_filters.FilterSet):

    title_capacity = CharFilter(field_name="title_capacity",
                                lookup_expr='icontains', label=_('عنوان الفرصة '))
    start_date_pub = DateFilter(field_name="created_at",
                                lookup_expr='gte', label=_('تاريخ نشر المنحة  / من :'))
    end_date_pub = DateFilter(field_name="created_at",
                              lookup_expr='lte', label=_('إلى :'))

    class Meta:
        model = OrgCapacityOpp
        fields = [
            'user',
            'org_name',
            'name_capacity',
            'title_capacity',
            'capacity_description',
            'capacity_type',
            'position_work',
            'city_work',
            'capacity_domain',
            'capacity_dead_date',
            'capacity_reqs',
            'capacity_guid',
            'capacity_url',
        ]
# org devs filters


class OrgsDevFilter(django_filters.FilterSet):

    title_dev = CharFilter(field_name="title_dev",
                           lookup_expr='icontains', label=_('عنوان المادة'))
    dev_description = CharFilter(field_name="dev_description",
                                 lookup_expr='icontains', label=_('لمحة عن الجهة'))

    start_date_pub = DateFilter(field_name="created_at",
                                lookup_expr='gte', label=_('تاريخ نشر المنحة  / من :'))
    end_date_pub = DateFilter(field_name="created_at",
                              lookup_expr='lte', label=_('إلى :'))

    class Meta:
        model = DevOrgOpp
        fields = [
            'user',
            'org_name',
            'name_dev',
            'title_dev',
            'dev_date',
            'subject',
            'dev_description',
            'start_date_pub',
            'end_date_pub',
        ]


class PersoFundFilter(django_filters.FilterSet):

    start_date_pub = DateFilter(field_name="created_at",
                                lookup_expr='gte', label=_('تاريخ نشر المنحة  / من :'))
    end_date_pub = DateFilter(field_name="created_at",
                              lookup_expr='lte', label=_('إلى :'))

    class Meta:
        model = PersFundingOpp
        fields = [
            'user',
            'category',
            'fund_type',
            'domain',
            'start_date_pub',
            'end_date_pub',
        ]
