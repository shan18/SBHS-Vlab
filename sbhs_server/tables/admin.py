from sbhs_server.tables.models import Account
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from django.contrib.auth.forms import UserChangeForm

class AccountChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = Account

class AccountAdmin(UserAdmin):
    form = AccountChangeForm
    list_filter = ['email']
    fieldsets = (
            (None, {'fields': ('is_admin', 'groups')}),
    ) # UserAdmin.fieldsets +



admin.site.register(Account, AccountAdmin)