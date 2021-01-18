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


# Org_jobs show all jobs with order by pub_at
def orgs_jobs(request):
    jobs = OrgJob.objects.filter(Q(publish=True) & Q(
        lang=request.LANGUAGE_CODE)).order_by('-created_at')
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
    jobs = OrgJob.objects.filter(Q(publish=False) & Q(
        lang=request.LANGUAGE_CODE)).order_by('-created_at')
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
            return redirect(job)
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
    print(other)
    # other = get_object_or_404(OtherOrgs, job=job_id)

    if request.method == 'POST':
        form = JobsForm(request.POST or None,
                        files=request.FILES, instance=job)
        form_other = OtherOrgsForm(
            request.POST or None, instance=other)

        if form.is_valid() and form_other.is_valid():

            org_name = form.cleaned_data.get('org_name')
            other_org_name = form.cleaned_data.get('other_org_name')
            other_name = form_other.cleaned_data.get('name')
            # other_org_name = form_other.cleaned_data.get('name')

            at = form.save(commit=False)
            at.updated_at = datetime.utcnow()

            if org_name:
                at.org_name = org_name
                at.save()

                messages.success(request, _(
                    'لقد تم تعديل فرصة العمل بنجاح'))

                return redirect(job)

            elif other_org_name:
                at.other_org_name = other_org_name
                at.save()

                messages.success(request, _(
                    'لقد تم تعديل فرصة العمل بنجاح'))

                return redirect(job)

            elif other_name:
                creater = form_other.save(commit=False)
                creater.created_by = request.user
                creater.staff = request.user
                creater.job = job
                creater.save()

                at.other_org_name = creater
                at.save()

                messages.success(request, _(
                    'لقد تم تعديل فرصة العمل بنجاح'))

                return redirect(job)

            else:
                # EN CASE ORG -> USER
                request_org_name = OrgProfile.objects.filter(
                    user=request.user).first()
                at.org_name = request_org_name
                at.save()

                messages.success(request, _(
                    'لقد تم تعديل فرصة العمل بنجاح'))

                return redirect(job)

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
        Q(publish=True) & Q(lang=request.LANGUAGE_CODE)).order_by('-created_at')

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
            return redirect(perso)
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
            return redirect(perso)
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
        return redirect('finance_perso')

    context = {
        'funding': funding,
    }
    return render(request, 'orgs/funding_opport/pers/delete.html', context)


@login_required(login_url='signe_in')
def finance_perso_not_pub(request):
    fundings = PersFundingOpp.objects.filter(
        Q(publish=False) & Q(lang=request.LANGUAGE_CODE)).order_by('-created_at')
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
        Q(publish=True) & Q(lang=request.LANGUAGE_CODE)).order_by('-created_at')

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
        Q(publish=False) & Q(lang=request.LANGUAGE_CODE)).order_by('-created_at')

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
            return redirect(funding)
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
            return redirect(funding)
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
