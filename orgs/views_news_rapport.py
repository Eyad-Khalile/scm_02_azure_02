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


# أخبار المجتمع المدني
def news(request):
    return render(request, 'orgs/news/orgs_news.html')



# ORGS NEWS / NEWS PUBLISHED أخبار المنظمات
def orgs_news(request):
    # print("current Lang from Views ======= :", request.LANGUAGE_CODE)
    news = OrgNews.objects.filter(Q(publish=True) & Q(lang=request.LANGUAGE_CODE) & ~Q(
        org_name__name='فريق البوابة')).order_by('-created_at')
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
    news = OrgNews.objects.filter(Q(publish=False) & Q(lang=request.LANGUAGE_CODE) & ~Q(
        org_name__name='فريق البوابة')).order_by('-created_at')

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
    news = OrgNews.objects.filter(Q(publish=False) & Q(lang=request.LANGUAGE_CODE) & Q(
        org_name__name='فريق البوابة')).order_by('-created_at')

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
            return redirect(new)
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
            return redirect(new)
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
    rapports = OrgRapport.objects.filter(Q(publish=True) & Q(
        lang=request.LANGUAGE_CODE)).order_by('-created_at')
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
    rapports = OrgRapport.objects.filter(Q(publish=False) & Q(
        lang=request.LANGUAGE_CODE)).order_by('-created_at')

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
            return redirect(rapport)
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

            return redirect(rapport)
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


# our news is filter of all the news that publiched by our site
def orgs_our_news(request):
    news = OrgNews.objects.filter(Q(publish=True) & Q(lang=request.LANGUAGE_CODE) & Q(
        org_name__name='فريق البوابة')).order_by('-created_at')

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
