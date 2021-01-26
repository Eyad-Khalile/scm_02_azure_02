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

# Capacity buildinng for opportunities


def orgs_capacity(request):
    Capacitys = OrgCapacityOpp.objects.filter(
        Q(publish=True) & Q(lang=request.LANGUAGE_CODE)).order_by('-created_at')

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


# add capacity
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
        Q(publish=False) & Q(lang=request.LANGUAGE_CODE)).order_by('-created_at')

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
            return redirect(capacity)
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
            at = form.save(commit=False)
            at.updated_at = datetime.utcnow()
            at.save()

            messages.success(request, _(
                'لقد تم تعديل فرصة بناء القدرات بنجاح'))

            return redirect(capacity)
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
    devs = DevOrgOpp.objects.filter(Q(publish=True) & Q(
        lang=request.LANGUAGE_CODE)).order_by('-created_at')

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
            org_name = form.cleaned_data.get('org_name')
            name_dev = form.cleaned_data.get('name_devv')

            user = form.save(commit=False)
            user.user = request.user

            if org_name or name_dev:
                user.created_by = request.user
                user.save()

                messages.success(request, _(
                    'لقد تمت إضافة دليل تطوير بنجاح و ستتم دراسته قريباً'))
                return redirect('orgs_devs')

            else:
                messages.error(request, _(
                    'رجاءً أدخل اسم المنظمة او اسم الجهة المانحة'))

    else:
        form = DevForm()

    context = {
        'form': form,
    }
    return render(request, 'orgs/devs/org_add_dev.html', context)


# devs list to confirme 0
@login_required(login_url='signe_in')
def org_devs_not_pub(request):
    devs = DevOrgOpp.objects.filter(Q(publish=False) & Q(
        lang=request.LANGUAGE_CODE)).order_by('-created_at')

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
            return redirect(dev)
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
            org_name = form.cleaned_data.get('org_name')
            name_dev = form.cleaned_data.get('name_devv')

            inst = form.save(commit=False)
            if org_name or name_dev:
                inst.updated_at = datetime.utcnow()
                inst.save()

                messages.success(request, _(
                    'لقد تم تعديل دليل التطوير بنجاح'))
                return redirect(devs)

            else:
                messages.error(request, _(
                    'رجاءً أدخل اسم المنظمة او اسم الجهة المانحة'))

    else:
        form = DevForm(instance=devs)

    context = {
        'devs': devs,
        'form': form,
    }
    return render(request, 'orgs/devs/org_edit_dev.html', context)


# DELETE DEVS
@login_required(login_url='signe_in')
def dev_delete(request, devs_id):
    devs = get_object_or_404(DevOrgOpp, id=devs_id)

    if request.method == 'POST' and request.user.is_superuser:
        devs.delete()
        messages.success(request, _('لقد تم حذف دليل التطوير بنجاح'))
        return redirect('orgs_devs')

    context = {
        'devs': devs,
    }

    return render(request, 'orgs/devs/org_dev_delete.html', context)
