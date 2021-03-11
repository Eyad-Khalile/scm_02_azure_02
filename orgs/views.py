# import phonenumbers
from django.forms.models import model_to_dict
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
import urllib
import json

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

                # RECAPTCHA
                # recaptcha_response = request.POST.get('g-recaptcha-response')
                # url = 'https://www.google.com/recaptcha/api/siteverify'
                # values = {
                #     'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                #     'response': recaptcha_response
                # }
                # data = urllib.parse.urlencode(values).encode()
                # req = urllib.request.Request(url, data=data)
                # response = urllib.request.urlopen(req)
                # result = json.loads(response.read().decode())

                # if result['success']:
                # else:
                #     messages.error(request, 'recptcha not valide')

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

# START PAGE
def start_page(request):

    context = {

    }
    return render(request, 'orgs/start_page.html', context)


# HOME PAGE
def home(request):
    orgs = OrgProfile.objects.filter(publish=True).order_by('-published_at')
    news = OrgNews.objects.filter(Q(publish=True) & Q(
        lang=request.LANGUAGE_CODE)).order_by('-published_at')
    jobs = OrgJob.objects.filter(Q(publish=True) & Q(
        lang=request.LANGUAGE_CODE)).order_by('-published_at')
    capacites = OrgCapacityOpp.objects.filter(
        Q(publish=True) & Q(lang=request.LANGUAGE_CODE)).order_by('-published_at')

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
    orgs = OrgProfile.objects.filter(
        publish=True).order_by('-published_at')
    # org_position = OrgProfile.objects.filter(position__position_work='SY')

    myFilter = OrgsFilter(request.GET, queryset=orgs.distinct())
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
        'qs_json': json.dumps(list(OrgProfile.objects.values('name', 'name_en_ku')), default=str)
    }
    return render(request, 'orgs//guid/orgs_guide.html', context)


# NEW FILTRE
def new_filtre(request):
    orgs = OrgProfile.objects.filter(
        publish=True).order_by('-published_at')

    context = {
        'orgs': orgs,
    }
    return render(request, 'orgs//guid/new_filtre.html', context)

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
        contact_subject = request.POST['contact_subject']
        contact_message = request.POST['contact_message']

        # print('========================== : ', contact_name, contact_email, contact_subject, contact_message)

        send_mail(
            # subject,
            # message,
            # from email,
            # to email,
            contact_subject,
            contact_message + '\n \n' + 'هذه الرسالة مرسلة من قبل ' + contact_email,
            contact_email,
            ['Civil.Society.Portal@csgateway.ngo'],

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
