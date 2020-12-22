from django.urls import path, include, re_path
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from . import views, views_prof_dash
from django.views.generic import TemplateView
from django.views.static import serve

urlpatterns = [
    # HOME AND LEGALE
    path('', views.home, name="home"),
    path('site_politic/', views.site_politic, name="site_politic"),

    # CITYES
    path('add_city/', views.add_city, name='add_city'),
    path('edit_city/<str:city_id>', views.edit_city, name='edit_city'),
    path('delete_city/<str:city_id>', views.delete_city, name='delete_city'),
    path('city/', views.view_city, name='city'),

    path('ajax/load-cities/', views.load_cities,
         name='ajax_load_cities'),  # AJAX


    # ORGS GUIDE
    path('guide/', views.guide, name="guide"),
    path('guide_conf/', views_prof_dash.guide_not_pub, name="guide_conf"),
    path('guide_filter/<str:work_id>', views.guide_filter, name="guide_filter"),

    # ORGS NEWS
    path('news/', views.news, name="news"),
    path('orgs_news/', views.orgs_news, name="orgs_news"),
    path('orgs_add_news/', views.orgs_add_news, name="orgs_add_news"),
    path('news_detail/<str:news_id>', views.news_detail, name="news_detail"),
    path('news_edit/<str:news_id>', views.news_edit, name="news_edit"),
    path('news_delete/<str:news_id>', views.news_delete, name="news_delete"),
    path('org_news_not_pub/', views.org_news_not_pub, name="org_news_not_pub"),
    
     # OUR NEWS
    path('our_news_not_pub/', views.our_news_not_pub, name="our_news_not_pub"),

    # ORGS RAPPORT
    path('add_rapport/', views.add_rapport, name="add_rapport"),
    path('orgs_rapport/', views.orgs_rapport, name="orgs_rapport"),
    path('orgs_rapport_detail/<str:rapport_id>',
         views.orgs_rapport_detail, name="orgs_rapport_detail"),
    path('edit_rapport/<str:rapport_id>',
         views.edit_rapport, name="edit_rapport"),
    path('orgs_rapport_delete/<str:rapport_id>',
         views.orgs_rapport_delete, name="orgs_rapport_delete"),
    path('orgs_rapport_not_pub/', views.orgs_rapport_not_pub,
         name="orgs_rapport_not_pub"),

    # ORGS DATA
    path('data/', views.data, name="data"),
    path('add_data/', views.add_data, name="add_data"),
    path('data_detail/<str:data_id>', views.data_detail, name="data_detail"),
    path('edit_data/<str:data_id>', views.edit_data, name="edit_data"),
    path('delete_data/<str:data_id>', views.delete_data, name="delete_data"),
    path('data_not_pub/', views.data_not_pub, name="data_not_pub"),

    # ORGS MEDIA
    path('media/', views.media, name="media"),
    path('add_media/', views.add_media, name="add_media"),
    path('media_detail/<str:media_id>', views.media_detail, name="media_detail"),
    path('edit_media/<str:media_id>', views.edit_media, name="edit_media"),
    path('delete_media/<str:media_id>', views.delete_media, name="delete_media"),
    path('media_not_pub/', views.media_not_pub, name="media_not_pub"),

    # ORGS RESEARCH
    path('research/', views.research, name="research"),
    path('add_research/', views.add_research, name="add_research"),
    path('research_detail/<str:research_id>',
         views.research_detail, name="research_detail"),
    path('edit_research/<str:research_id>',
         views.edit_research, name="edit_research"),
    path('delete_research/<str:research_id>',
         views.delete_research, name="delete_research"),
    path('research_not_pub/', views.research_not_pub, name="research_not_pub"),

    # RECOURCE
    path('resources/', views.resources, name="resources"),
    # jobs
    path('orgs_jobs/', views.orgs_jobs, name="orgs_jobs"),
    path('orgs_add_job/', views.orgs_add_job, name="orgs_add_job"),
    path('org_jobs_not_pub/', views.org_jobs_not_pub, name="org_jobs_not_pub"),
    path('jobs_detail/<str:job_id>', views.jobs_detail, name="jobs_detail"),
    path('jobs_edit/<str:job_id>', views.jobs_edit, name="jobs_edit"),
    path('jobs_delete/<str:job_id>', views.jobs_delete, name="jobs_delete"),
    # funding orgs opportutiite
    path('funding', views.funding, name="funding"),
    path('orgs_funding/', views.orgs_funding, name="orgs_funding"),
    path('orgs_add_funding/', views.orgs_add_funding, name="orgs_add_funding"),
    path('org_funding_not_pub/', views.org_funding_not_pub,
         name="org_funding_not_pub"),
    path('funding_detail/<str:funding_id>',
         views.funding_detail, name="funding_detail"),
    path('funding_edit/<str:funding_id>',
         views.funding_edit, name="funding_edit"),
    path('funding_delete/<str:funding_id>',
         views.funding_delete, name="funding_delete"),
    # Capacity orgs opportutiite
    path('orgs_capacity/', views.orgs_capacity, name="orgs_capacity"),
    path('orgs_add_capacity/', views.orgs_add_capacity, name="orgs_add_capacity"),
    path('org_capacity_not_pub/', views.org_capacity_not_pub,
         name="org_capacity_not_pub"),
    path('capacity_detail/<str:capacity_id>',
         views.capacity_detail, name="capacity_detail"),
    path('capacity_edit/<str:capacity_id>',
         views.capacity_edit, name="capacity_edit"),
    path('capacity_delete/<str:capacity_id>',
         views.capacity_delete, name="capacity_delete"),
    # devs guide
    path('orgs_devs/', views.orgs_devs, name="orgs_devs"),
    path('orgs_add_devs/', views.orgs_add_devs, name="orgs_add_devs"),
    path('org_devs_not_pub/', views.org_devs_not_pub, name="org_devs_not_pub"),
    path('devs_detail/<str:devs_id>', views.devs_detail, name="devs_detail"),
    path('dev_edit/<str:devs_id>', views.dev_edit, name="dev_edit"),
    path('dev_delete/<str:devs_id>', views.dev_delete, name="dev_delete"),
    # our news
    path('orgs_our_news/', views.orgs_our_news, name="orgs_our_news"),
    path('friend_invite/', views.friend_invite, name='friend_invite'),




    # FINANCE PERSO
    path('finance_perso/', views.finance_perso,
         name="finance_perso"),
    path('add_finance_perso/', views.add_finance_perso,
         name="add_finance_perso"),
    path('finance_perso_not_pub/', views.finance_perso_not_pub,
         name="finance_perso_not_pub"),
    path('finance_perso_detail/<str:pk>',
         views.finance_perso_detail, name="finance_perso_detail"),
    path('finance_perso_edit/<str:pk>',
         views.finance_perso_edit, name="finance_perso_edit"),
    path('finance_perso_delete/<str:pk>',
         views.finance_perso_delete, name="finance_perso_delete"),



    # CENTRE NEWS
    #     path('centre_news/', views.centre_news, name="centre_news"),
    #     path('centre_news_detail/<str:id>',
    #          views.centre_news_detail, name="centre_news_detail"),

    # CONTACT-US
    path('contact', views.contact, name="contact"),


    # SIGNE-IN AND SIGNE-UP
    # path('signe_in', views.signe_in, name="signe_in"),
    path('login/', auth_views.LoginView.as_view(template_name='register/signe-in.html'), name='signe_in'),
    path('signe_up/', views.signe_up, name="signe_up"),

    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
         views.activate, name='activate'),

    #     re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    #             views.activate, name='activate'),


    path('logout/', auth_views.LogoutView.as_view(template_name='register/logged_out.html'), name='logout'),
    path('profile/', views_prof_dash.profile, name="profile"),
    path('profile_supper/', views_prof_dash.admin_dashboard, name="profile_supper"),
    path('profile_staff/', views_prof_dash.profile_staff, name="profile_staff"),

    # Org Fill the form
    path('org_profile/', views_prof_dash.org_profile, name='org_profile'),
    # Org Edit the form
    path('org_profile_edit/<str:pk>',
         views_prof_dash.org_profile_edit, name='org_profile_edit'),
    path('org_profile_delete/<str:pk>',
         views_prof_dash.org_profile_delete, name='org_profile_delete'),
    path('orgs_orders_etude/', views_prof_dash.orgs_orders_etude,
         name='orgs_orders_etude'),
    path('orgs_orders_published/', views_prof_dash.orgs_orders_published,
         name='orgs_orders_published'),
    path('particip_detail/<str:par_id>',
         views_prof_dash.particip_detail, name="particip_detail"),

    # Password Reset
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='register/password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='register/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='register/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='register/password_reset_complete.html'), name='password_reset_complete'),

    # Password Change
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='register/password_change_done.html'), name='password_change_done'),
    path('password_change/', auth_views.PasswordChangeView.as_view(
        template_name='register/password_change.html'), name='password_change'),
]
