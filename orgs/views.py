# import phonenumbers
from urllib.parse import quote_plus
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.sites.shortcuts import get_current_site

from django.contrib.auth.decorators import login_required
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .forms import *
from .models import *
from django.contrib import messages
from .tokens import account_activation_token
import os
from django.conf import settings
from django.urls import reverse_lazy, reverse
from django.core.mail import EmailMessage
from django.utils.timezone import datetime
from django.utils.translation import gettext as _
from django.core.paginator import Paginator
from .filters import *
import traceback
from django.db.models import Q
from datetime import date, timedelta
from django.utils.datastructures import MultiValueDictKeyError
# BOKEH
from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource
from bokeh.palettes import Spectral6
from bokeh.plotting import figure
from bokeh.transform import factor_cmap
from bokeh.embed import components
# from excel_response import ExcelResponse
from django.core.mail import send_mail, send_mass_mail
from django.template.loader import get_template
from django.template import Context


# SendGrid
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


# ::::::::::::: SIGNE UP :::::::::::::::
def signe_up(request):

    if request.user.is_authenticated and not request.user.is_superuser:
        return redirect('home')
    else:
        # users = User.objects.all()
        # emails = []
        # for user in users:
        #     emails += user.email,

        if request.method == 'POST':
            form = SignUpForm(request.POST or None)
            # user_email = request.POST.get('email')
            # if user_email not in emails:
            if form.is_valid():
                user = form.save(commit=False)
                if request.user.is_superuser:
                    user.is_active = True
                else:
                    user.is_active = False
                user.save()

                if not request.user.is_superuser:
                    current_site = get_current_site(request)
                    subject = 'Activate Your Account.'
                    message = render_to_string('register/account_activation_email.html', {
                        'user': user,
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': account_activation_token.make_token(user),
                    })
                    to_email = form.cleaned_data.get('email')
                    email = EmailMessage(
                        subject, message, to=[to_email]
                    )

                    # print(email)
                    email.send()
                    username = form.cleaned_data.get('username')
                    # messages.success(
                    #     request, f'Your Account has been created Successful with username ( {username} ) !, Please confirm your email address to complete the registration ')
                    messages.success(
                        request, _(f'تم إنشاء حسابك بنجاح باسم المستخدم ( {username} ) !, يرجى تأكيد عنوان بريدك الإلكتروني لإكمال التسجيل '))
                    return redirect('home')

                else:
                    username = form.cleaned_data.get('username')
                    # messages.success(
                    #     request, f'Your Account has been created Successful with username ( {username} ) !, Please confirm your email address to complete the registration ')
                    messages.success(
                        request, _(f'لقد تم تسجيل حساب المستخدم ( {username} ) بنجاح'))
                    return redirect('signe_up')

            # else:

            #     if user_email in emails:
            #         # messages.error(
            #         #     request, f'Please Sign-up with another email address, this email ( {user_email} ) is already in use')
            #         messages.error(
            #             request, _(f'يرجى التسجيل باستخدام عنوان بريد إلكتروني آخر، هذا البريد الإلكتروني ( {user_email} ) مستخدم مسبقاً'))
            #         return redirect('signe_up')
            #     # else:

        else:
            form = SignUpForm()

        context = {
            'form': form
        }
        return render(request, 'register/signe-up.html', context)


# ACTIVATION ACCOUNT


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'register/active.html')


# CITYES
@login_required(login_url='signe_in')
def add_city(request):

    if request.method == 'POST':
        form = CityForm(request.POST or None)
        if form.is_valid():
            form.save()
            form = CityForm()

            # messages.success(
            #     request, 'لقد تمت إضافة المحافظة بنجاح')

            # return redirect('city')
    else:
        form = CityForm()

    context = {
        'form': form
    }
    return render(request, 'city/add_city.html', context)


@login_required(login_url='signe_in')
def edit_city(request, city_id):
    city = get_object_or_404(City, id=city_id)

    if request.method == 'POST':
        form = CityForm(request.POST or None, instance=city)
        if form.is_valid():
            date = form.save(commit=False)
            date.updated_at = datetime.utcnow()
            date.save()

            form = CityForm()

            messages.success(
                request, 'لقد تمت تعديل المحافظة بنجاح')

            # return redirect('city')

    else:
        form = CityForm(instance=city)

    context = {
        'city': city,
        'form': form
    }
    return render(request, 'city/edite_city.html', context)


@login_required(login_url='signe_in')
def delete_city(request, city_id):
    city = get_object_or_404(City, id=city_id)

    if request.method == 'POST' and request.user.is_superuser:
        city.delete()

        messages.success(request, _(
            'لقد تم حذف المحافظه بنجاح'))
        return redirect('city')

    context = {
        'city': city,
    }
    return render(request, 'city/delete_city.html', context)


@login_required(login_url='signe_in')
def view_city(request):
    cityes = City.objects.all().order_by('id')

    context = {
        'cityes': cityes,
    }
    return render(request, 'city/view_city.html', context)


# AJAX
def load_cities(request):
    position_work = request.GET.get('position_work')
    cities = City.objects.filter(position_work=position_work).all()
    return render(request, 'city/city_dropdown_list_options.html', {'cities': cities})
    # return JsonResponse(list(cities.values('id', 'name')), safe=False)

# =========== Page 404 ==================


def page_not_found_view(request, exception):
    return render(request, 'errors/404.html')


# NEWS LETTER
# def NewsLetter(request):
#     if request.is_ajax():
#         formNews = NewsLetterForm(request.POST or None)
#         if formNews.is_valid():
#             formNews.save()
#             # formNews = NewsLetterForm()
#             return JsonResponse({
#                 'msg': 'Success',
#             }, status=200)

#             messages.success(request, _(
#                 'لقد تم طلب الاشتراك بآخر اﻷخبار بنجاح'))

#     else:
#         formNews = NewsLetterForm()
#     context = {
#         'formNews': formNews,
#     }

#     return render(request, 'combonents/footer.html', context)


# HOME PAGE
def home(request):
    orgs = OrgProfile.objects.filter(publish=True).order_by('-published_at')
    news = OrgNews.objects.filter(publish=True).order_by('-published_at')
    jobs = OrgJob.objects.filter(publish=True).order_by('-published_at')
    capacites = OrgCapacityOpp.objects.filter(
        publish=True).order_by('-published_at')

    # the Last orgs
    if orgs.first():
        first_org = orgs.first().id
    else:
        first_org = _('لا يوجد حاليا منظمات')

    # the Last news
    if news.first():
        first_news = news.first().id
    else:
        first_news = _('لا يوجد أخبار حالياً')

    # the Last job
    if jobs.first():
        first_job = jobs.first().id
    else:
        first_job = _('لا يوجد')

    # the Last job
    if capacites.first():
        first_capacity = capacites.first().id
    else:
        first_capacity = _('لا يوجد حاليا فرص بناء')

    # if request.is_ajax():
    if request.method == 'POST':
        formNews = NewsLetterForm(request.POST or None)
        if formNews.is_valid():
            formNews.save()
            formNews = NewsLetterForm()

            messages.success(request, _(
                'لقد تم طلب الاشتراك بآخر اﻷخبار بنجاح'))

            # return JsonResponse({
            #     'msg': 'Success',
            # }, status=200)

        else:
            messages.error(request, _(
                'هذا البريد الالكتروني موجود مسبقاً يرجى التسجيل ببريد الكتروني أخر'))

    else:
        formNews = NewsLetterForm()

    context = {
        'orgs': orgs,
        'first_org': first_org,
        'news': news,
        'first_news': first_news,
        'jobs': jobs,
        'first_job': first_job,
        'capacites': capacites,
        'first_capacity': first_capacity,
        'formNews': formNews,
    }
    return render(request, 'orgs/home.html', context)


# L'AFFICHAGE DES ORGS PUBLISHED
def guide(request):
    orgs = OrgProfile.objects.filter(publish=True).order_by('-published_at')

    myFilter = OrgsFilter(request.GET, queryset=orgs)
    orgs = myFilter.qs

    # PAGINATEUR
    paginator = Paginator(orgs, 12)
    page = request.GET.get('page')
    try:
        orgs = paginator.get_page(page)
    except(EmptyPage, InvalidPage):
        orgs = paginator.page(paginator.num_pages)

    context = {
        'orgs': orgs,
        'myFilter': myFilter,
    }
    return render(request, 'orgs//guid/orgs_guide.html', context)


# @register.filter(name='phonenumber')
# def phonenumber(value, country=None):
#     return phonenumbers.parse(value, country)


def guide_filter(request, work_id):
    id = work_id

    list_work = ''
    if id == '1':
        list_work = 'اﻹعلام'
    elif id == '2':
        list_work = 'التعليم'
    elif id == '3':
        list_work = 'الحماية'
    elif id == '4':
        list_work = 'سبل العيش و اﻷمن الغذائي'
    elif id == '5':
        list_work = 'مشاريع النظافة و المياه و الصرف الصحي'
    elif id == '6':
        list_work = 'التنمية'
    elif id == '7':
        list_work = 'القانون و مناصرة و سياسة'
    elif id == '8':
        list_work = 'المانحين و دعم العمل التطوعي'
    elif id == '9':
        list_work = 'المنظمات دينية'
    elif id == '10':
        list_work = 'التجمعات و الاتحادات المهنية'
    elif id == '11':
        list_work = 'الصحة'
    elif id == '12':
        list_work = 'الدراسات و اﻷبحاث'

    context = {
        'id': id,
        'list_work': list_work
    }
    return render(request, 'orgs/guid/orgs_guide_filter.html', context)


# أخبار المجتمع المدني
def news(request):
    return render(request, 'orgs/news/orgs_news.html')


# ORGS NEWS / NEWS PUBLISHED أخبار المنظمات
def orgs_news(request):
    news = OrgNews.objects.filter(Q(publish=True) & ~Q(
        org_name__name='khalil')).order_by('-created_at')
    if request.user.is_authenticated:
        org_prof_pub_check = OrgProfile.objects.filter(
            user=request.user).first()
    else:
        org_prof_pub_check = OrgProfile.objects.all()

    myFilter = OrgsNewsFilter(request.GET, queryset=news)
    news = myFilter.qs

    # PAGINATEUR
    paginator = Paginator(news, 12)
    page = request.GET.get('page')
    try:
        news = paginator.get_page(page)
    except(EmptyPage, InvalidPage):
        news = paginator.page(paginator.num_pages)

    context = {
        'news': news,
        'myFilter': myFilter,
        'org_prof_pub_check': org_prof_pub_check,
    }
    return render(request, 'orgs/news/orgs_news_news.html', context)


# ORGS ADD NEWS
@login_required(login_url='signe_in')
def orgs_add_news(request):

    if request.user.is_authenticated:
        org_prof_pub_check = OrgProfile.objects.filter(
            user=request.user).first()
    else:
        org_prof_pub_check = OrgProfile.objects.all()

    if request.method == 'POST':
        form = NewsForm(request.POST or None, files=request.FILES)
        if form.is_valid():
            user = form.save(commit=False)

            prof_user = OrgProfile.objects.filter(user=request.user)
            user.user = request.user
            org_name = form.cleaned_data.get('org_name')

            if org_name:
                user.org_name = org_name
            else:
                user.org_name = prof_user.first()
            user.save()

            messages.success(request, _(
                'لقد تمت إضافة الخبر بنجاح و ستتم دراسته قريباً'))

            return redirect('orgs_news')
    else:
        form = NewsForm()

    context = {
        'form': form,
        'org_prof_pub_check': org_prof_pub_check,
    }
    return render(request, 'orgs/news/org_add_news.html', context)


# أخبار المنظمات قيد الدراسة
@login_required(login_url='signe_in')
def org_news_not_pub(request):
    news = OrgNews.objects.filter(Q(publish=False) & ~Q(
        org_name__name='khalil')).order_by('-created_at')

    filter_user_id = request.GET.get('user', None)

    myFilter = OrgsNewsFilter(request.GET, queryset=news)
    news = myFilter.qs

    if request.user.is_authenticated:
        org_prof_pub_check = OrgProfile.objects.filter(
            user=request.user).first()
    else:
        org_prof_pub_check = OrgProfile.objects.all()

    # PAGINATEUR
    paginator = Paginator(news, 12)
    page = request.GET.get('page')
    try:
        news = paginator.get_page(page)
    except(EmptyPage, InvalidPage):
        news = paginator.page(paginator.num_pages)

    context = {
        'news': news,
        'myFilter': myFilter,
        'org_prof_pub_check': org_prof_pub_check,
        'filter_user_id': filter_user_id,
    }
    return render(request, 'orgs/news/org_news_not_pub.html', context)


# أخبار المركز قيد الدراسة
@login_required(login_url='signe_in')
def our_news_not_pub(request):
    news = OrgNews.objects.filter(Q(publish=False) & Q(
        org_name__name='khalil')).order_by('-created_at')

    filter_user_id = request.GET.get('user', None)

    myFilter = OrgsNewsFilter(request.GET, queryset=news)
    news = myFilter.qs

    if request.user.is_authenticated:
        org_prof_pub_check = OrgProfile.objects.filter(
            user=request.user).first()
    else:
        org_prof_pub_check = OrgProfile.objects.all()

    # PAGINATEUR
    paginator = Paginator(news, 12)
    page = request.GET.get('page')
    try:
        news = paginator.get_page(page)
    except(EmptyPage, InvalidPage):
        news = paginator.page(paginator.num_pages)

    context = {
        'news': news,
        'myFilter': myFilter,
        'org_prof_pub_check': org_prof_pub_check,
        'filter_user_id': filter_user_id,
    }
    return render(request, 'orgs/our_news/our_news_not_pub.html', context)


# ORG NEWS DETAIL
def news_detail(request, news_id):
    new = get_object_or_404(OrgNews, id=news_id)
    news = OrgNews.objects.filter(publish=True).order_by('-created_at')
    share_string = quote_plus(new.title)

    if request.method == 'POST':
        form = NewsConfirmForm(request.POST or None, instance=new)
        if form.is_valid():
            at = form.save(commit=False)
            at.published_at = datetime.utcnow()
            at.save()

            messages.success(request, _(
                'لقد تم تغيير حالة الخبر بنجاح'))
            return redirect('orgs_news')
    else:
        form = NewsConfirmForm(instance=new)

    context = {
        'new': new,
        'news': news,
        'form': form,
        'share_string': share_string,
    }
    return render(request, 'orgs/news/orgs_news_detail.html', context)


# NEWS EDIT
@login_required(login_url='signe_in')
def news_edit(request, news_id):
    new = get_object_or_404(OrgNews, id=news_id)

    if request.method == 'POST':
        form = NewsForm(request.POST or None,
                        files=request.FILES, instance=new)
        if form.is_valid():
            at = form.save(commit=False)
            at.updated_at = datetime.utcnow()
            prof_user = OrgProfile.objects.filter(user=request.user)
            org_name = form.cleaned_data.get('org_name')
            if org_name:
                at.org_name = org_name
            else:
                at.org_name = prof_user.first()
            at.save()

            messages.success(request, _(
                'لقد تم تعديل الخبر بنجاح'))
            return redirect('orgs_news')
    else:
        form = NewsForm(instance=new)

    context = {
        'new': new,
        'form': form,
    }
    return render(request, 'orgs/news/org_edit_news.html', context)

# :: NEWS DELETE ::


@login_required(login_url='signe_in')
def news_delete(request, news_id):
    new = get_object_or_404(OrgNews, id=news_id)

    if request.method == 'POST' and request.user.is_superuser:
        new.delete()

        messages.success(request, _(
            'لقد تم حذف الخبر بنجاح'))
        return redirect('orgs_news')

    context = {
        'new': new,
    }
    return render(request, 'orgs/news/org_news_delete.html', context)


# ::::::::::::: RAPPORT ::::::::::::::::::::::
@login_required(login_url='signe_in')
def add_rapport(request):
    if request.user.is_authenticated:
        org_prof_pub_check = OrgProfile.objects.filter(
            user=request.user).first()
    else:
        org_prof_pub_check = OrgProfile.objects.all()

    if request.method == 'POST':
        form = RapportForm(request.POST or None, files=request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.user = request.user
            prof_user = OrgProfile.objects.filter(user=request.user)
            org_name = form.cleaned_data.get('org_name')
            if org_name:
                user.org_name = org_name
            else:
                user.org_name = prof_user.first()
            user.save()

            messages.success(request, _(
                'لقد تمت إضافة التقرير بنجاح و ستتم دراسته قريباً'))

            return redirect('orgs_rapport')
    else:
        form = RapportForm()

    context = {
        "form": form,
        'org_prof_pub_check': org_prof_pub_check,
    }
    return render(request, 'orgs/rapport/add_rapport.html', context)


# ::::::::: L'AFFICHAGE DES ORGS RAPPORTS ::::::::::::::::
def orgs_rapport(request):
    rapports = OrgRapport.objects.filter(publish=True).order_by('-created_at')
    if request.user.is_authenticated:
        org_prof_pub_check = OrgProfile.objects.filter(
            user=request.user).first()
    else:
        org_prof_pub_check = OrgProfile.objects.all()

    myFilter = OrgsRapportFilter(request.GET, queryset=rapports)
    rapports = myFilter.qs

    # PAGINATEUR
    paginator = Paginator(rapports, 12)
    page = request.GET.get('page')
    try:
        rapports = paginator.get_page(page)
    except(EmptyPage, InvalidPage):
        rapports = paginator.page(paginator.num_pages)

    context = {
        'rapports': rapports,
        'myFilter': myFilter,
        'org_prof_pub_check': org_prof_pub_check,
    }
    return render(request, 'orgs/rapport/rapport.html', context)


@login_required(login_url='signe_in')
def orgs_rapport_not_pub(request):
    rapports = OrgRapport.objects.filter(publish=False).order_by('-created_at')

    filter_user_id = request.GET.get('user', None)

    myFilter = OrgsRapportFilter(request.GET, queryset=rapports)
    rapports = myFilter.qs

    if request.user.is_authenticated:
        org_prof_pub_check = OrgProfile.objects.filter(
            user=request.user).first()
    else:
        org_prof_pub_check = OrgProfile.objects.all()

    # PAGINATEUR
    paginator = Paginator(rapports, 12)
    page = request.GET.get('page')
    try:
        rapports = paginator.get_page(page)
    except(EmptyPage, InvalidPage):
        rapports = paginator.page(paginator.num_pages)

    context = {
        'rapports': rapports,
        'myFilter': myFilter,
        'org_prof_pub_check': org_prof_pub_check,
        'filter_user_id': filter_user_id,
    }
    return render(request, 'orgs/rapport/rapport_not_pub.html', context)


# RAPPORT DETAIL
def orgs_rapport_detail(request, rapport_id):
    rapport = get_object_or_404(OrgRapport, id=rapport_id)
    share_string = quote_plus(rapport.title)
    rapports = OrgRapport.objects.filter(publish=True).order_by('-created_at')

    if request.method == 'POST':
        form = RapportConfirmForm(request.POST or None,
                                  files=request.FILES, instance=rapport)
        if form.is_valid():
            at = form.save(commit=False)
            at.published_at = datetime.utcnow()
            at.save()

            messages.success(request, _(
                'لقد تم تعديل حالة التقرير بنجاح'))
            return redirect('orgs_rapport')
    else:
        form = RapportConfirmForm(instance=rapport)

    context = {
        'rapport': rapport,
        'form': form,
        'share_string': share_string,
        'rapports': rapports,

    }
    return render(request, 'orgs/rapport/detail_rapport.html', context)


# UPDATE RAPPORT
@login_required(login_url='signe_in')
def edit_rapport(request, rapport_id):
    rapport = get_object_or_404(OrgRapport, id=rapport_id)

    if request.method == 'POST':
        form = RapportForm(request.POST or None,
                           files=request.FILES, instance=rapport)
        if form.is_valid():
            user = form.save(commit=False)
            user.updated_at = datetime.utcnow()
            prof_user = OrgProfile.objects.filter(user=request.user)
            org_name = form.cleaned_data.get('org_name')
            if org_name:
                user.org_name = org_name
            else:
                user.org_name = prof_user.first()
            user.save()

            messages.success(request, _(
                'لقد تمت تعديل التقرير بنجاح'))

            return redirect('orgs_rapport')
    else:
        form = RapportForm(instance=rapport)

    context = {
        "rapport": rapport,
        "form": form,
    }
    return render(request, 'orgs/rapport/edit_rapport.html', context)


# DELETE RAPPORT
@login_required(login_url='signe_in')
def orgs_rapport_delete(request, rapport_id):
    rapport = get_object_or_404(OrgRapport, id=rapport_id)

    if request.method == 'POST' and request.user.is_superuser:
        rapport.delete()

        messages.success(request, _(
            'لقد تم حذف التقرير بنجاح'))
        return redirect('orgs_rapport')

    context = {
        'rapport': rapport,
    }
    return render(request, 'orgs/rapport/delete_rapport.html', context)


# ::::::::::: DATA :::::::::::::::
# DATA PUB
def data(request):
    datas = OrgData.objects.filter(publish=True).order_by('-created_at')
    if request.user.is_authenticated:
        org_prof_pub_check = OrgProfile.objects.filter(
            user=request.user).first()
    else:
        org_prof_pub_check = OrgProfile.objects.all()

    myFilter = OrgsDataFilter(request.GET, queryset=datas)
    datas = myFilter.qs

    # PAGINATEUR
    paginator = Paginator(datas, 12)
    page = request.GET.get('page')
    try:
        datas = paginator.get_page(page)
    except(EmptyPage, InvalidPage):
        datas = paginator.page(paginator.num_pages)

    context = {
        'datas': datas,
        'myFilter': myFilter,
        'org_prof_pub_check': org_prof_pub_check,
    }
    return render(request, 'orgs/data/data.html', context)


@login_required(login_url='signe_in')
def add_data(request):
    if request.user.is_authenticated:
        org_prof_pub_check = OrgProfile.objects.filter(
            user=request.user).first()
    else:
        org_prof_pub_check = OrgProfile.objects.all()

    if request.method == 'POST':
        form = DataForm(request.POST or None, files=request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.user = request.user
            prof_user = OrgProfile.objects.filter(user=request.user)
            org_name = form.cleaned_data.get('org_name')
            if org_name:
                user.org_name = org_name
            else:
                user.org_name = prof_user.first()
            user.save()

            messages.success(request, _(
                'لقد تمت إضافة البيان بنجاح و ستتم دراسته قريباً'))

            return redirect('data')
    else:
        form = DataForm()
    context = {
        'form': form,
        'org_prof_pub_check': org_prof_pub_check,
    }

    return render(request, 'orgs/data/add_data.html', context)


def data_detail(request, data_id):
    data = get_object_or_404(OrgData, id=data_id)
    share_string = quote_plus(data.title)
    datas = OrgData.objects.filter(publish=True).order_by('-created_at')

    if request.method == 'POST':
        form = DataConfirmForm(request.POST or None,
                               files=request.FILES, instance=data)
        if form.is_valid():
            at = form.save(commit=False)
            at.published_at = datetime.utcnow()
            at.save()

            messages.success(request, _(
                'لقد تم تعديل حالة البيان بنجاح'))
            return redirect('data')

    else:
        form = DataConfirmForm(instance=data)

    context = {
        'data': data,
        'form': form,
        'share_string': share_string,
        'datas': datas,
    }
    return render(request, 'orgs/data/detail_data.html', context)


@login_required(login_url='signe_in')
def data_not_pub(request):
    datas = OrgData.objects.filter(publish=False).order_by('-created_at')

    filter_user_id = request.GET.get('user', None)

    if request.user.is_authenticated:
        org_prof_pub_check = OrgProfile.objects.filter(
            user=request.user).first()
    else:
        org_prof_pub_check = OrgProfile.objects.all()

    myFilter = OrgsDataFilter(request.GET, queryset=datas)
    datas = myFilter.qs

    # PAGINATEUR
    paginator = Paginator(datas, 12)
    page = request.GET.get('page')
    try:
        datas = paginator.get_page(page)
    except(EmptyPage, InvalidPage):
        datas = paginator.page(paginator.num_pages)

    context = {
        'datas': datas,
        'myFilter': myFilter,
        'org_prof_pub_check': org_prof_pub_check,
        'filter_user_id': filter_user_id,
    }
    return render(request, 'orgs/data/data_not_pub.html', context)


@login_required(login_url='signe_in')
def edit_data(request, data_id):
    data = get_object_or_404(OrgData, id=data_id)

    if request.method == 'POST':
        form = DataForm(request.POST or None,
                        files=request.FILES, instance=data)
        if form.is_valid():
            at = form.save(commit=False)
            at.updated = datetime.utcnow()
            prof_user = OrgProfile.objects.filter(user=request.user)
            org_name = form.cleaned_data.get('org_name')
            if org_name:
                at.org_name = org_name
            else:
                at.org_name = prof_user.first()
            at.save()

            messages.success(request, _(
                'لقد تم تعديل البيان بنجاح'))
            return redirect('data')

    else:
        form = DataForm(instance=data)

    context = {
        'form': form,
    }
    return render(request, 'orgs/data/edit_data.html', context)


@login_required(login_url='signe_in')
def delete_data(request, data_id):
    data = get_object_or_404(OrgData, id=data_id)
    if request.method == 'POST' and request.user.is_superuser:
        data.delete()

        messages.success(request, _(
            'لقد تم حذف البيان بنجاح'))
        return redirect('data')
    context = {
        'data': data,
    }
    return render(request, 'orgs/data/delete_data.html', context)


# :::::::::: MEDIA :::::::::::::::
def media(request):
    medias = OrgMedia.objects.filter(publish=True).order_by('-created_at')
    if request.user.is_authenticated:
        org_prof_pub_check = OrgProfile.objects.filter(
            user=request.user).first()
    else:
        org_prof_pub_check = OrgProfile.objects.all()

    myFilter = OrgsMediaFilter(request.GET, queryset=medias)
    medias = myFilter.qs

    # PAGINATEUR
    paginator = Paginator(medias, 12)
    page = request.GET.get('page')
    try:
        medias = paginator.get_page(page)
    except(EmptyPage, InvalidPage):
        medias = paginator.page(paginator.num_pages)

    context = {
        'medias': medias,
        'myFilter': myFilter,
        'org_prof_pub_check': org_prof_pub_check,
    }
    return render(request, 'orgs/media/media.html', context)


@login_required(login_url='signe_in')
def add_media(request):
    if request.user.is_authenticated:
        org_prof_pub_check = OrgProfile.objects.filter(
            user=request.user).first()
    else:
        org_prof_pub_check = OrgProfile.objects.all()

    if request.method == 'POST':
        form = MediaForm(request.POST or None, files=request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.user = request.user
            prof_user = OrgProfile.objects.filter(user=request.user)
            org_name = form.cleaned_data.get('org_name')
            if org_name:
                user.org_name = org_name
            else:
                user.org_name = prof_user.first()
            user.save()

            messages.success(request, _(
                'لقد تمت إضافة المحتوى بنجاح و ستتم دراسته قريباً'))

            return redirect('media')
    else:
        form = MediaForm()

    context = {
        'form': form,
        'org_prof_pub_check': org_prof_pub_check,
    }

    return render(request, 'orgs/media/add_media.html', context)


def media_detail(request, media_id):
    media = get_object_or_404(OrgMedia, id=media_id)
    share_string = quote_plus(media.title)
    medias = OrgMedia.objects.filter(publish=True).order_by('-created_at')

    if request.method == 'POST':
        form = MediaConfirmForm(request.POST or None,
                                files=request.FILES, instance=media)
        if form.is_valid():
            at = form.save(commit=False)
            at.published_at = datetime.utcnow()
            at.save()

            messages.success(request, _(
                'لقد تم تعديل حالة المحتوى بنجاح'))
            return redirect('media')

    else:
        form = MediaConfirmForm(instance=media)

    context = {
        'media': media,
        'form': form,
        'share_string': share_string,
        'medias': medias,
    }
    return render(request, 'orgs/media/media_detail.html', context)


@login_required(login_url='signe_in')
def media_not_pub(request):
    medias = OrgMedia.objects.filter(publish=False).order_by('-created_at')

    filter_user_id = request.GET.get('user', None)

    myFilter = OrgsMediaFilter(request.GET, queryset=medias)
    medias = myFilter.qs

    if request.user.is_authenticated:
        org_prof_pub_check = OrgProfile.objects.filter(
            user=request.user).first()
    else:
        org_prof_pub_check = OrgProfile.objects.all()

    # PAGINATEUR
    paginator = Paginator(medias, 12)
    page = request.GET.get('page')
    try:
        medias = paginator.get_page(page)
    except(EmptyPage, InvalidPage):
        medias = paginator.page(paginator.num_pages)

    context = {
        'medias': medias,
        'myFilter': myFilter,
        'org_prof_pub_check': org_prof_pub_check,
        'filter_user_id': filter_user_id,
    }
    return render(request, 'orgs/media/media_not_pub.html', context)


@login_required(login_url='signe_in')
def edit_media(request, media_id):
    media = get_object_or_404(OrgMedia, id=media_id)

    if request.method == 'POST':
        form = MediaForm(request.POST or None,
                         files=request.FILES, instance=media)
        if form.is_valid():
            at = form.save(commit=False)
            at.updated = datetime.utcnow()
            prof_user = OrgProfile.objects.filter(user=request.user)
            org_name = form.cleaned_data.get('org_name')
            if org_name:
                at.org_name = org_name
            else:
                at.org_name = prof_user.first()
            at.save()

            messages.success(request, _(
                'لقد تم تعديل المحتوى بنجاح'))
            return redirect('media')

    else:
        form = MediaForm(instance=media)

    context = {
        'media': media,
        'form': form,
    }
    return render(request, 'orgs/media/edit_media.html', context)


@login_required(login_url='signe_in')
def delete_media(request, media_id):
    media = get_object_or_404(OrgMedia, id=media_id)
    if request.method == 'POST' and request.user.is_superuser:
        media.delete()

        messages.success(request, _(
            'لقد تم حذف المحتوى بنجاح'))
        return redirect('media')
    context = {
        'media': media,
    }
    return render(request, 'orgs/media/delete_media.html', context)


# RESEARCH
def research(request):
    researchs = OrgResearch.objects.filter(
        publish=True).order_by('-created_at')
    if request.user.is_authenticated:
        org_prof_pub_check = OrgProfile.objects.filter(
            user=request.user).first()
    else:
        org_prof_pub_check = OrgProfile.objects.all()

    myFilter = OrgsResearchFilter(request.GET, queryset=researchs)
    researchs = myFilter.qs

    # PAGINATEUR
    paginator = Paginator(researchs, 12)
    page = request.GET.get('page')
    try:
        researchs = paginator.get_page(page)
    except(EmptyPage, InvalidPage):
        researchs = paginator.page(paginator.num_pages)

    context = {
        'researchs': researchs,
        'myFilter': myFilter,
        'org_prof_pub_check': org_prof_pub_check,
    }
    return render(request, 'orgs/research/research.html', context)


@login_required(login_url='signe_in')
def add_research(request):
    if request.user.is_authenticated:
        org_prof_pub_check = OrgProfile.objects.filter(
            user=request.user).first()
    else:
        org_prof_pub_check = OrgProfile.objects.all()

    if request.method == 'POST':
        form = ResearchForm(request.POST or None, files=request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.user = request.user
            org_name = form.cleaned_data.get('org_name')
            if org_name:
                user.org_name = org_name
            else:
                user.org_name = request.user
            user.save()

            messages.success(request, _(
                'لقد تمت إضافة البحث بنجاح و ستتم دراسته قريباً'))

            return redirect('research')
    else:
        form = ResearchForm()

    context = {
        'form': form,
        'org_prof_pub_check': org_prof_pub_check,
    }

    return render(request, 'orgs/research/add_research.html', context)


def research_detail(request, research_id):
    research = get_object_or_404(OrgResearch, id=research_id)
    researchs = OrgResearch.objects.filter(
        publish=True).order_by('-created_at')

    share_string = quote_plus(research.title)

    if request.method == 'POST':
        form = ResearchConfirmForm(request.POST or None,
                                   files=request.FILES, instance=research)
        if form.is_valid():
            at = form.save(commit=False)
            at.published_at = datetime.utcnow()
            at.save()

            messages.success(request, _(
                'لقد تم تعديل حالة البحث بنجاح'))
            return redirect('research')

    else:
        form = ResearchConfirmForm(instance=research)

    context = {
        'research': research,
        'form': form,
        'share_string': share_string,
        'researchs': researchs,
    }
    return render(request, 'orgs/research/detail_research.html', context)


@login_required(login_url='signe_in')
def research_not_pub(request):
    researchs = OrgResearch.objects.filter(
        publish=False).order_by('-created_at')

    myFilter = OrgsResearchFilter(request.GET, queryset=researchs)
    researchs = myFilter.qs

    filter_user_id = request.GET.get('user', None)

    if request.user.is_authenticated:
        org_prof_pub_check = OrgProfile.objects.filter(
            user=request.user).first()
    else:
        org_prof_pub_check = OrgProfile.objects.all()

    # PAGINATEUR
    paginator = Paginator(researchs, 12)
    page = request.GET.get('page')
    try:
        researchs = paginator.get_page(page)
    except(EmptyPage, InvalidPage):
        researchs = paginator.page(paginator.num_pages)

    context = {
        'researchs': researchs,
        'myFilter': myFilter,
        'org_prof_pub_check': org_prof_pub_check,
        'filter_user_id': filter_user_id,
    }
    return render(request, 'orgs/research/research_not_pub.html', context)


@login_required(login_url='signe_in')
def edit_research(request, research_id):
    research = get_object_or_404(OrgResearch, id=research_id)

    if request.method == 'POST':
        form = ResearchForm(request.POST or None,
                            files=request.FILES, instance=research)
        if form.is_valid():
            at = form.save(commit=False)
            at.updated = datetime.utcnow()
            at.save()

            messages.success(request, _(
                'لقد تم تعديل البحث بنجاح'))
            return redirect('research')

    else:
        form = ResearchForm(instance=research)

    context = {
        'research': research,
        'form': form,
    }
    return render(request, 'orgs/research/edit_research.html', context)


@login_required(login_url='signe_in')
def delete_research(request, research_id):
    research = get_object_or_404(OrgResearch, id=research_id)
    if request.method == 'POST' and request.user.is_superuser:
        research.delete()

        messages.success(request, _(
            'لقد تم حذف البحث بنجاح'))
        return redirect('research')
    context = {
        'research': research,
    }
    return render(request, 'orgs/research/delete_research.html', context)


# CENTRE NEWS
def centre_news(request):
    return render(request, 'orgs/centre_news.html')


def centre_news_detail(request, id):
    id = id

    context = {
        'id': id,
    }
    return render(request, 'orgs/centre_news_detail.html', context)


# SITE POLITIQUE
def site_politic(request):
    return render(request, 'orgs/politic.html')


# CONTACT-US
def contact(request):

    if request.method == 'POST':
        form = ContactUsForm(request.POST or None)

        contact_name = request.POST['contact_name']
        contact_email = request.POST['contact_email']
        contact_subject = request.POST['contact_email']
        contact_message = request.POST['contact_message']

        send_mail(
            # subject,
            # message,
            # from email,
            # to email,
            contact_subject + ' ' + contact_name + ' ' + contact_email,
            contact_message,
            contact_email,
            ['khalile.eyad@gmail.com'],

        )

        messages.success(
            request, 'لقد تم الارسال بنجاح و سيتم الرد باقرب وقت ممكن')
        return redirect('home')

    else:
        form = ContactUsForm()

    context = {
        'form': form,
    }

    return render(request, 'contact/contact.html', context)


# Recourses of civilty this is the befor last tab
def resources(request):
    return render(request, 'orgs/resources/org_recources.html')

####################################################################
# Org_jobs show all jobs with order by pub_at


def orgs_jobs(request):
    jobs = OrgJob.objects.filter(publish=True).order_by('-created_at')
    if request.user.is_authenticated:
        org_prof_pub_check = OrgProfile.objects.filter(
            user=request.user).first()
    else:
        org_prof_pub_check = OrgProfile.objects.all()

    myFilter = OrgsJobsFilter(request.GET, queryset=jobs)
    jobs = myFilter.qs

    # PAGINATEUR
    paginator = Paginator(jobs, 12)
    page = request.GET.get('page')
    try:
        jobs = paginator.get_page(page)
    except(EmptyPage, InvalidPage):
        jobs = paginator.page(paginator.num_pages)

    context = {
        'jobs': jobs,
        'myFilter': myFilter,
        'org_prof_pub_check': org_prof_pub_check,
    }
    return render(request, 'orgs/resources/org_jobs.html', context)
# add job to recourse


@login_required(login_url='signe_in')
def orgs_add_job(request):
    if request.user.is_authenticated:
        org_prof_pub_check = OrgProfile.objects.filter(
            user=request.user).first()
    else:
        org_prof_pub_check = OrgProfile.objects.all()

    other = OtherOrgs.objects.all().count()

    if request.method == 'POST':
        form = JobsForm(request.POST or None, files=request.FILES)
        form_other = OtherOrgsForm(request.POST or None, files=request.FILES)
        if form.is_valid() and form_other.is_valid():

            user = form.save(commit=False)
            user.user = request.user

            org_name = form.cleaned_data.get('org_name')
            other_org_name = form.cleaned_data.get('other_org_name')
            other_name = form_other.cleaned_data.get('name')

            prof_user = OrgProfile.objects.filter(user=request.user)
            # if (org_name and other_org_name) and other_name :

            if org_name:
                user.org_name = org_name
                user.staff = request.user
                user.save()

                messages.success(request, _(
                    'لقد تمت إضافة فرصة العمل بنجاح و ستتم دراستها قريباً'))

                return redirect('orgs_jobs')

            elif other_org_name:
                user.other_org_name = other_org_name
                user.staff = request.user
                user.save()

                messages.success(request, _(
                    'لقد تمت إضافة فرصة العمل بنجاح و ستتم دراستها قريباً'))

                return redirect('orgs_jobs')

            elif other_name:
                creater = form_other.save(commit=False)
                creater.created_by = request.user
                creater.staff = request.user
                creater.job = user
                creater.save()

                user.other_org_name = creater
                user.save()

                messages.success(request, _(
                    'لقد تمت إضافة فرصة العمل بنجاح و ستتم دراستها قريباً'))

                return redirect('orgs_jobs')

            else:
                # messages.error(request, _(
                #     'يجب إدخال اسم منظمة لتتم معالجة و نشر فرصة العمل'))
                request_org_name = OrgProfile.objects.filter(
                    user=request.user).first()
                user.org_name = request_org_name
                user.save()

                messages.success(request, _(
                    'لقد تمت إضافة فرصة العمل بنجاح و ستتم دراستها قريباً'))

                return redirect('orgs_jobs')
    else:
        form = JobsForm()
        form_other = OtherOrgsForm()

    context = {
        'form': form,
        'other': other,
        'form_other': form_other,
        'org_prof_pub_check': org_prof_pub_check,
    }
    return render(request, 'orgs/resources/org_add_job.html', context)
# jobs list to confirme


@login_required(login_url='signe_in')
def org_jobs_not_pub(request):
    jobs = OrgJob.objects.filter(publish=False).order_by('-created_at')
    others = OtherOrgs.objects.all()

    myFilter = OrgsJobsFilter(request.GET, queryset=jobs)
    jobs = myFilter.qs

    filter_user_id = request.GET.get('user', None)

    if request.user.is_authenticated:
        org_prof_pub_check = OrgProfile.objects.filter(
            user=request.user).first()
    else:
        org_prof_pub_check = OrgProfile.objects.all()

    # PAGINATEUR
    paginator = Paginator(jobs, 12)
    page = request.GET.get('page')
    try:
        jobs = paginator.get_page(page)
    except(EmptyPage, InvalidPage):
        jobs = paginator.page(paginator.num_pages)

    context = {
        'jobs': jobs,
        'myFilter': myFilter,
        'org_prof_pub_check': org_prof_pub_check,
        'filter_user_id': filter_user_id,
    }

    return render(request, 'orgs/resources/jobs_not_pub.html', context)


# job details
def jobs_detail(request, job_id):
    job = get_object_or_404(OrgJob, id=job_id)
    other = OtherOrgs.objects.filter(job=job_id).first()
    jobs = OrgJob.objects.filter(publish=True).order_by('-created_at')

    share_string = quote_plus(job.job_description)

    job_type = job.get_job_type_display()
    experience = job.get_experience_display()
    position_work = job.get_position_work_display()
    job_domain = job.get_job_domain_display()

    if request.method == 'POST':
        form = NewsConfirmForm(request.POST or None, instance=job)
        if form.is_valid():
            at = form.save(commit=False)
            at.published_at = datetime.utcnow()
            at.save()

            messages.success(request, _(
                'لقد تم تغيير حالة فرصة العمل بنجاح'))
            return redirect('orgs_jobs')
    else:
        form = JobsConfirmForm(instance=job)

    context = {
        'job': job,
        'form': form,
        'other': other,
        'jobs': jobs,
        'job_type': job_type,
        'experience': experience,
        'position_work': position_work,
        'job_domain': job_domain,
        'share_string': share_string,
    }
    return render(request, 'orgs/resources/org_job_details.html', context)
# job edit to modify job details


@login_required(login_url='signe_in')
def jobs_edit(request, job_id):
    job = get_object_or_404(OrgJob, id=job_id)
    other = OtherOrgs.objects.filter(job=job_id).first()
    # other = get_object_or_404(OtherOrgs, job=job_id)

    if request.method == 'POST':
        form = JobsForm(request.POST or None,
                        files=request.FILES, instance=job)
        form_other = OtherOrgsForm(
            request.POST or None, files=request.FILES, instance=other)

        if form.is_valid() and form_other.is_valid():

            other_org_name = form_other.cleaned_data.get('name')

            at = form.save(commit=False)
            at.updated_at = datetime.utcnow()

            if other_org_name:
                other = form_other.save(commit=False)
                other.created_by = request.user
                other.job = at
                other.save()

                at.other_org_name = other
                at.save()

                messages.success(request, _(
                    'لقد تم تعديل فرصة العمل بنجاح'))
                return redirect('orgs_jobs')

            else:
                at.other_org_name = other
                at.save()

            messages.success(request, _(
                'لقد تم تعديل فرصة العمل بنجاح'))
            return redirect('orgs_jobs')
    else:
        form = JobsForm(instance=job)
        form_other = OtherOrgsForm(instance=other)

    context = {
        'job': job,
        'form': form,
        'form_other': form_other,
    }
    return render(request, 'orgs/resources/org_edit_job.html', context)
# delete job


@login_required(login_url='signe_in')
def jobs_delete(request, job_id):
    job = get_object_or_404(OrgJob, id=job_id)

    if request.method == 'POST' and request.user.is_superuser:
        job.delete()

        messages.success(request, _(
            'لقد تم حذف فرصة العمل بنجاح'))
        return redirect('orgs_jobs')

    context = {
        'job': job,
    }
    return render(request, 'orgs/resources/org_job_delete.html', context)
#############################################################################
# FUNDING GENERAL


def funding(request):
    context = {

    }
    return render(request, 'orgs/funding_opport/funding.html', context)

# FINANCE PERSO PUB


def finance_perso(request):
    fundings = PersFundingOpp.objects.filter(
        publish=True).order_by('-created_at')

    myFilter = PersoFundFilter(request.GET, queryset=fundings)
    fundings = myFilter.qs

    # PAGINATEUR
    paginator = Paginator(fundings, 12)
    page = request.GET.get('page')
    try:
        fundings = paginator.get_page(page)
    except(EmptyPage, InvalidPage):
        fundings = paginator.page(paginator.num_pages)

    context = {
        'fundings': fundings,
        'myFilter': myFilter,
    }
    return render(request, 'orgs/funding_opport/pers/pub.html', context)


@login_required(login_url='signe_in')
def add_finance_perso(request):
    if request.method == 'POST':
        form = PersoFunForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            org_name = form.cleaned_data.get('org_name')
            name_funding = form.cleaned_data.get('name_funding')

            if org_name or name_funding:
                user = form.save(commit=False)
                user.user = request.user
                user.save()

                messages.success(request, _(
                    'لقد تم تسجيل طلب فرصة التمويل بنجاح و ستتم دراسته قريباً'))
                return redirect('finance_perso')
            else:
                messages.error(request, _(
                    'رجاءً أدخل اسم المنظمة أو الجهة المانحة لتتم دراسة فرصة التمويل'))
    else:
        form = PersoFunForm()

    context = {
        'form': form,
    }
    return render(request, 'orgs/funding_opport/pers/add.html', context)


# FINANCE PERSO DETAILS


def finance_perso_detail(request, pk):
    perso = get_object_or_404(PersFundingOpp, id=pk)
    persos = PersFundingOpp.objects.filter(
        publish=True).order_by('-created_at')

    share_string = quote_plus(perso.funding_description)

    if request.method == 'POST':
        form = PersoFundConfirmForm(request.POST or None, instance=perso)
        if form.is_valid():
            at = form.save(commit=False)
            at.published_at = datetime.utcnow()
            at.save()

            messages.success(request, _(
                'لقد تم تغيير حالة فرصة التمويل بنجاح'))
            return redirect('finance_perso')
    else:
        form = PersoFundConfirmForm(instance=perso)

    context = {
        'perso': perso,
        'persos': persos,
        'form': form,
        'share_string': share_string,
    }
    return render(request, 'orgs/funding_opport/pers/detail.html', context)


@login_required(login_url='signe_in')
def finance_perso_edit(request, pk):
    perso = get_object_or_404(PersFundingOpp, id=pk)

    if request.method == 'POST':
        form = PersoFunForm(request.POST or None,
                            files=request.FILES, instance=perso)
        if form.is_valid():
            at = form.save(commit=False)
            at.updated_at = datetime.utcnow()
            at.save()

            messages.success(request, _(
                'لقد تم تعديل فرصة التمويل بنجاح'))
            return redirect('finance_perso')
    else:
        form = PersoFunForm(instance=perso)

    context = {
        'perso': perso,
        'form': form,
    }

    return render(request, 'orgs/funding_opport/pers/edit.html', context)


@login_required(login_url='signe_in')
def finance_perso_delete(request, pk):
    funding = get_object_or_404(PersFundingOpp, id=pk)

    if request.method == 'POST' and request.user.is_superuser:
        funding.delete()

        messages.success(request, _(
            'لقد تم حذف فرصة التمويل بنجاح'))
        return redirect('orgs_jobs')

    context = {
        'funding': funding,
    }
    return render(request, 'orgs/funding_opport/pers/delete.html', context)


@login_required(login_url='signe_in')
def finance_perso_not_pub(request):
    fundings = PersFundingOpp.objects.filter(
        publish=False).order_by('-created_at')
    myFilter = PersoFundFilter(request.GET, queryset=fundings)
    fundings = myFilter.qs

    filter_user_id = request.GET.get('user', None)

    # PAGINATEUR
    paginator = Paginator(fundings, 12)
    page = request.GET.get('page')
    try:
        fundings = paginator.get_page(page)
    except(EmptyPage, InvalidPage):
        fundings = paginator.page(paginator.num_pages)

    context = {
        'fundings': fundings,
        'myFilter': myFilter,
        'filter_user_id': filter_user_id,
    }
    return render(request, 'orgs/funding_opport/pers/not_pub.html', context)


# funding org opp
def orgs_funding(request):
    fundings = OrgFundingOpp.objects.filter(
        publish=True).order_by('-created_at')

    myFilter = OrgsFundingFilter(request.GET, queryset=fundings)
    fundings = myFilter.qs

    # PAGINATEUR
    paginator = Paginator(fundings, 12)
    page = request.GET.get('page')
    try:
        fundings = paginator.get_page(page)
    except(EmptyPage, InvalidPage):
        fundings = paginator.page(paginator.num_pages)

    context = {
        'fundings': fundings,
        'myFilter': myFilter,
    }
    return render(request, 'orgs/funding_opport/orgs/org_funding.html', context)
# add funding


@login_required(login_url='signe_in')
def orgs_add_funding(request):

    if request.method == 'POST':
        form = FundingForm(request.POST or None, files=request.FILES)
        if form.is_valid():

            org_name = form.cleaned_data.get('org_name')
            name_funding = form.cleaned_data.get('name_funding')

            if org_name or name_funding:
                user = form.save(commit=False)
                user.user = request.user
                if org_name:
                    user.org_name = org_name
                elif name_funding:
                    user.name_funding = name_funding

                user.save()

                messages.success(request, _(
                    'لقد تمت إضافة فرصة التمويل بنجاح و ستتم دراسته قريباً'))

                return redirect('orgs_funding')
            else:
                messages.error(request, _(
                    'يحب إدخال اسم منظمة أو اسم الجهة المانحة لنتمكن من دراسة فرصة التمويل'))
    else:
        form = FundingForm()

    context = {
        'form': form,
    }
    return render(request, 'orgs/funding_opport/orgs/org_add_funding.html', context)
# funding list to confirme


@login_required(login_url='signe_in')
def org_funding_not_pub(request):
    fundings = OrgFundingOpp.objects.filter(
        publish=False).order_by('-created_at')

    myFilter = OrgsFundingFilter(request.GET, queryset=fundings)
    fundings = myFilter.qs

    filter_user_id = request.GET.get('user', None)

    # PAGINATEUR
    paginator = Paginator(fundings, 12)
    page = request.GET.get('page')
    try:
        fundings = paginator.get_page(page)
    except(EmptyPage, InvalidPage):
        fundings = paginator.page(paginator.num_pages)

    context = {
        'fundings': fundings,
        'myFilter': myFilter,
        'filter_user_id': filter_user_id,
    }
    return render(request, 'orgs/funding_opport/orgs/fundings_not_pub.html', context)
# funding details


def funding_detail(request, funding_id):
    funding = get_object_or_404(OrgFundingOpp, id=funding_id)
    fundings = OrgFundingOpp.objects.filter(
        publish=True).order_by('-created_at')

    share_string = quote_plus(funding.funding_org_description)

    if request.method == 'POST':
        form = FundingConfirmForm(request.POST or None, instance=funding)
        if form.is_valid():
            at = form.save(commit=False)
            at.published_at = datetime.utcnow()
            at.save()

            messages.success(request, _(
                'لقد تم تغيير حالة المنحة  بنجاح'))
            return redirect('orgs_funding')
    else:
        form = FundingConfirmForm(instance=funding)

    context = {
        'funding': funding,
        'form': form,
        'fundings': fundings,
        'share_string': share_string,
    }
    return render(request, 'orgs/funding_opport/orgs/org_funding_details.html', context)
# job edit to modify job details


@login_required(login_url='signe_in')
def funding_edit(request, funding_id):
    funding = get_object_or_404(OrgFundingOpp, id=funding_id)

    if request.method == 'POST':
        form = FundingForm(request.POST or None,
                           files=request.FILES, instance=funding)
        if form.is_valid():
            at = form.save(commit=False)
            at.updated_at = datetime.utcnow()
            at.save()

            messages.success(request, _(
                'لقد تم تعديل فرصة التمويل بنجاح'))
            return redirect('orgs_funding')
    else:
        form = FundingForm(instance=funding)

    context = {
        'funding': funding,
        'form': form,
    }
    return render(request, 'orgs/funding_opport/orgs/org_edit_funding.html', context)
# delete funding


@login_required(login_url='signe_in')
def funding_delete(request, funding_id):
    funding = get_object_or_404(OrgFundingOpp, id=funding_id)

    if request.method == 'POST' and request.user.is_superuser:
        funding.delete()

        messages.success(request, _(
            'لقد تم حذف فرصة التمويل بنجاح'))
        return redirect('orgs_funding')

    context = {
        'funding': funding,
    }
    return render(request, 'orgs/funding_opport/orgs/org_funding_delete.html', context)


# Capacity buildinng for opportunities
def orgs_capacity(request):
    Capacitys = OrgCapacityOpp.objects.filter(
        publish=True).order_by('-created_at')

    myFilter = OrgsCapacityFilter(request.GET, queryset=Capacitys)
    Capacitys = myFilter.qs

    # PAGINATEUR
    paginator = Paginator(Capacitys, 12)
    page = request.GET.get('page')

    try:
        Capacitys = paginator.get_page(page)
    except(EmptyPage, InvalidPage):
        Capacitys = paginator.page(paginator.num_pages)

    context = {
        'Capacitys': Capacitys,
        'myFilter': myFilter,
    }
    return render(request, 'orgs/capacity/org_capacity.html', context)
# add funding


@login_required(login_url='signe_in')
def orgs_add_capacity(request):

    if request.method == 'POST':
        form = CapacityForm(request.POST or None, files=request.FILES)
        if form.is_valid():
            org_name = form.cleaned_data.get('org_name')
            name_capacity = form.cleaned_data.get('name_capacity')
            if org_name or name_capacity:
                user = form.save(commit=False)
                user.user = request.user
                org_name = form.cleaned_data.get('org_name')

                if org_name:
                    user.org_name = org_name
                user.save()

                messages.success(request, _(
                    'لقد تمت إضافة فرصة بناء القدرات بنجاح و ستتم دراسته قريباً'))

                return redirect('orgs_capacity')
            else:
                messages.error(request, _(
                    'يجب إدخال اسم الجهة المانحة لنتمكن من دراسة الفرصة'))
    else:
        form = CapacityForm()

    context = {
        'form': form,
    }
    return render(request, 'orgs/capacity/org_add_capacity.html', context)
# funding list to confirme


@login_required(login_url='signe_in')
def org_capacity_not_pub(request):
    Capacitys = OrgCapacityOpp.objects.filter(
        publish=False).order_by('-created_at')

    myFilter = OrgsCapacityFilter(request.GET, queryset=Capacitys)
    Capacitys = myFilter.qs

    filter_user_id = request.GET.get('user', None)

    # PAGINATEUR
    paginator = Paginator(Capacitys, 12)
    page = request.GET.get('page')

    try:
        Capacitys = paginator.get_page(page)
    except(EmptyPage, InvalidPage):
        Capacitys = paginator.page(paginator.num_pages)

    context = {
        'Capacitys': Capacitys,
        'myFilter': myFilter,
        'filter_user_id': filter_user_id,
    }
    return render(request, 'orgs/capacity/capacity_not_pub.html', context)
# capacity details


def capacity_detail(request, capacity_id):
    capacity = get_object_or_404(OrgCapacityOpp, id=capacity_id)
    capacites = OrgCapacityOpp.objects.filter(
        publish=True).order_by('-created_at')
    share_string = quote_plus(capacity.capacity_description)

    if request.method == 'POST':
        form = CapacityConfirmForm(request.POST or None, instance=capacity)
        if form.is_valid():
            at = form.save(commit=False)
            at.published_at = datetime.utcnow()
            at.save()

            messages.success(request, _(
                'لقد تم تغيير حالة فرصة بناء القدرات  بنجاح'))
            return redirect('orgs_capacity')
    else:
        form = CapacityConfirmForm(instance=capacity)

    context = {
        'capacity': capacity,
        'capacites': capacites,
        'form': form,
        'share_string': share_string,
    }
    return render(request, 'orgs/capacity/org_capacity_details.html', context)
# capacity edit to modify capacity details


@login_required(login_url='signe_in')
def capacity_edit(request, capacity_id):
    capacity = get_object_or_404(OrgCapacityOpp, id=capacity_id)

    if request.method == 'POST':
        form = CapacityForm(request.POST or None,
                            files=request.FILES, instance=capacity)
        if form.is_valid():
            print('salut')
            at = form.save(commit=False)
            at.updated_at = datetime.utcnow()
            at.save()

            messages.success(request, _(
                'لقد تم تعديل فرصة بناء القدرات بنجاح'))

            return redirect('orgs_capacity')
        else:
            messages.error(request, 'the form is not valide')
    else:
        form = CapacityForm(instance=capacity)

    context = {
        'capacity': capacity,
        'form': form,
    }
    return render(request, 'orgs/capacity/org_edit_capacity.html', context)
# delete funding


@login_required(login_url='signe_in')
def capacity_delete(request, capacity_id):
    capacity = get_object_or_404(OrgCapacityOpp, id=capacity_id)

    if request.method == 'POST' and request.user.is_superuser:
        capacity.delete()

        messages.success(request, _(
            'لقد تم حذف فرصة بناء القدرات بنجاح'))
        return redirect('orgs_capacity')

    context = {
        'capacity': capacity,
    }
    return render(request, 'orgs/capacity/org_capacity_delete.html', context)
# dev orgs guide devs


def orgs_devs(request):
    devs = DevOrgOpp.objects.filter(publish=True).order_by('-created_at')

    myFilter = OrgsDevFilter(request.GET, queryset=devs)
    devs = myFilter.qs

    # PAGINATEUR
    paginator = Paginator(devs, 12)
    page = request.GET.get('page')
    try:
        devs = paginator.get_page(page)
    except(EmptyPage, InvalidPage):
        devs = paginator.page(paginator.num_pages)

    context = {
        'devs': devs,
        'myFilter': myFilter,
    }
    return render(request, 'orgs/devs/org_devs.html', context)
# add devs


@login_required(login_url='signe_in')
def orgs_add_devs(request):

    if request.method == 'POST':
        form = DevForm(request.POST or None, files=request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.user = request.user
            org_name = form.cleaned_data.get('org_name')
            if org_name:
                user.org_name = org_name
            # else:
            #     user.org_name = request.user
            user.save()

            messages.success(request, _(
                'لقد تمت إضافة دليل تطوير بنجاح و ستتم دراسته قريباً'))

            return redirect('orgs_devs')
    else:
        form = DevForm()

    context = {
        'form': form,
    }
    return render(request, 'orgs/devs/org_add_dev.html', context)
# devs list to confirme 0


@login_required(login_url='signe_in')
def org_devs_not_pub(request):
    devs = DevOrgOpp.objects.filter(publish=False).order_by('-created_at')

    myFilter = OrgsDevFilter(request.GET, queryset=devs)
    devs = myFilter.qs

    filter_user_id = request.GET.get('user', None)

    # PAGINATEUR
    paginator = Paginator(devs, 12)
    page = request.GET.get('page')
    try:
        devs = paginator.get_page(page)
    except(EmptyPage, InvalidPage):
        devs = paginator.page(paginator.num_pages)

    context = {
        'devs': devs,
        'myFilter': myFilter,
        'filter_user_id': filter_user_id,
    }
    return render(request, 'orgs/devs/dev_not_pub.html', context)
# devs details


def devs_detail(request, devs_id):
    dev = get_object_or_404(DevOrgOpp, id=devs_id)
    devs = DevOrgOpp.objects.filter(publish=True).order_by('-created_at')

    share_string = quote_plus(dev.dev_description)

    if request.method == 'POST':
        form = DevConfirmForm(request.POST or None, instance=dev)
        if form.is_valid():
            at = form.save(commit=False)
            at.published_at = datetime.utcnow()
            at.save()

            messages.success(request, _(
                'لقد تم تغيير حالة دليل تطوير بنجاح'))
            return redirect('orgs_devs')
    else:
        form = DevConfirmForm(instance=dev)

    context = {
        'dev': dev,
        'devs': devs,
        'form': form,
        'share_string': share_string,
    }
    return render(request, 'orgs/devs/org_dev_details.html', context)
# dev edit to modify dev details


@login_required(login_url='signe_in')
def dev_edit(request, devs_id):
    devs = get_object_or_404(DevOrgOpp, id=devs_id)

    if request.method == 'POST':
        form = DevForm(request.POST or None,
                       files=request.FILES, instance=devs)
        if form.is_valid():
            at = form.save(commit=False)
            at.updated_at = datetime.utcnow()
            at.save()

            messages.success(request, _(
                'لقد تم تعديل دليل التطوير بنجاح'))
            return redirect('orgs_devs')
    else:
        form = DevForm(instance=devs)

    context = {
        'devs': devs,
        'form': form,
    }
    return render(request, 'orgs/devs/org_edit_dev.html', context)


# delete dev bulding
@login_required(login_url='signe_in')
def dev_delete(request, devs_id):
    devs = DevOrgOpp.objects.filter(publish=True).order_by('-created_at')

    myFilter = OrgsDevFilter(request.GET, queryset=devs)
    devs = myFilter.qs

    # PAGINATEUR
    paginator = Paginator(devs, 12)
    page = request.GET.get('page')
    try:
        devs = paginator.get_page(page)
    except(EmptyPage, InvalidPage):
        devs = paginator.page(paginator.num_pages)

    context = {
        'devs': devs,
        'myFilter': myFilter,
    }
    return render(request, 'orgs/devs/org_devs.html', context)


# @login_required(login_url='signe_in')
# def dev_delete(request, devs_id):
#     devs = get_object_or_404(DevOrgOpp, id=devs_id)

#     if request.method == 'POST' and request.user.is_superuser:
# 	devs.delete()

# 	messages.success(request, _(
#             'لقد تم حذف دليل التطوير بنجاح'))
# 	return redirect('orgs_devs')


# our news is filter of all the news that publiched by our site


def orgs_our_news(request):
    news = OrgNews.objects.filter(Q(publish=True) & Q(
        org_name__name='khalil')).order_by('-created_at')

    myFilter = OrgsNewsFilter(request.GET, queryset=news)
    news = myFilter.qs

    # PAGINATEUR
    paginator = Paginator(news, 12)
    page = request.GET.get('page')
    try:
        news = paginator.get_page(page)
    except(EmptyPage, InvalidPage):
        news = paginator.page(paginator.num_pages)

    context = {
        'news': news,
        'myFilter': myFilter,
    }
    return render(request, 'orgs/our_news/our_news.html', context)
# send invitions


@login_required(login_url='signe_in')
def friend_invite(request):
    if request.method == 'POST':
        form = FriendInviteForm(request.POST or None, files=request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.sender = request.user
            user.save()

            messages.success(request, _(
                'لقد تم ارسال الدعوة '))
            return redirect('profile_supper')

    else:
        form = FriendInviteForm()

    context = {
        'form': form,
    }

    return render(request, 'orgs/our_news/friend_invite.html', context)
