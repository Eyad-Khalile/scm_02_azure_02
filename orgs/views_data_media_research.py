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


# ::::::::::: DATA :::::::::::::::
# DATA PUB
def data(request):
    datas = OrgData.objects.filter(Q(publish=True) & Q(
        lang=request.LANGUAGE_CODE)).order_by('-created_at')
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
            return redirect(data)

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
    datas = OrgData.objects.filter(Q(publish=False) & Q(
        lang=request.LANGUAGE_CODE)).order_by('-created_at')

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
            return redirect(data)

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
    medias = OrgMedia.objects.filter(Q(publish=True) & Q(
        lang=request.LANGUAGE_CODE)).order_by('-created_at')
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
            return redirect(media)

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
    medias = OrgMedia.objects.filter(Q(publish=False) & Q(
        lang=request.LANGUAGE_CODE)).order_by('-created_at')

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
            return redirect(media)

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
        Q(publish=True) & Q(lang=request.LANGUAGE_CODE)).order_by('-created_at')
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
            return redirect(research)

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
        Q(publish=False) & Q(lang=request.LANGUAGE_CODE)).order_by('-created_at')

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
            return redirect(research)

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
