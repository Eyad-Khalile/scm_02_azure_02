from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Permission, User, Group
from copy import deepcopy

from django.contrib import admin
from .models import *
from django.utils.translation import gettext_lazy as _

# Register your models here.
# ::::::::::::: CONF ADMIN PAGE TITLE ::::::::::::::
admin.site.site_header = _('إدارة موقع SCM ')
admin.site.site_title = _('إدارة موقع SCM ')


class MyUserAdmin(UserAdmin):

    # def formfield_for_dbfield(self, db_field, **kwargs):

    #     field = super(MyUserAdmin, self).formfield_for_dbfield(
    #         db_field, **kwargs)
    #     # print('Field ======== : ', field)
    #     user = kwargs['request'].user

    #     if not user.is_superuser:
    #         # print('db_field ======== : ', db_field)
    #         print('db_field name ======== : ', db_field.name)
    #         if db_field.name == 'is_superuser':
    #             field.widget.attrs = {'disabled': 'disabled'}
    #         if db_field.name == 'is_staff':
    #             field.widget.attrs = {'disabled': 'disabled'}
    #         if db_field.name == 'is_active':
    #             field.widget.attrs = {'disabled': 'disabled'}
    #     return field

    def get_fieldsets(self, request, obj=None):

        fieldsets = super(MyUserAdmin, self).get_fieldsets(request, obj)
        if not obj:
            return fieldsets

        # if not request.user.is_superuser or request.user.pk == obj.pk:
        if not request.user.is_superuser:
            fieldsets = deepcopy(fieldsets)
            for fieldset in fieldsets:
                print('Fieldset ==== : ', fieldset)

                if 'password' in fieldset[1]['fields']:
                    if type(fieldset[1]['fields']) == tuple:
                        fieldset[1]['fields'] = list(fieldset[1]['fields'])
                        fieldset[1]['fields'].remove('password')

                if 'is_superuser' in fieldset[1]['fields']:
                    if type(fieldset[1]['fields']) == tuple:
                        fieldset[1]['fields'] = list(fieldset[1]['fields'])
                        fieldset[1]['fields'].remove('is_superuser')
                        fieldset[1]['fields'].remove('is_active')
                        fieldset[1]['fields'].remove('is_staff')
                        fieldset[1]['fields'].remove('groups')
                        fieldset[1]['fields'].remove('user_permissions')
                    break

        return fieldsets


admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)


admin.site.register(Profile)
admin.site.register(NewsLetter)
admin.site.register(OrgProfile)
admin.site.register(City)
