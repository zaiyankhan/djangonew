from cms.extensions import PageExtensionAdmin
from django.contrib import admin
from django.contrib import messages
from django.shortcuts import redirect
from import_export.admin import ImportExportModelAdmin, ExportActionModelAdmin, ExportMixin
from import_export import fields
from website.forms.user import UserChangeFormAdmin, UserChangeForm, UserCreationForm
from website.models import *
from django.contrib.auth.admin import UserAdmin
from django import forms
from django.utils.translation import ugettext, ugettext_lazy as _
from import_export import resources


class UserResource(resources.ModelResource):

    class Meta:
        model = AppUser
        fields = ('id', 'email', 'first_name', 'last_name', 'company', 'business_type__name', 'city', 'state', 'country',
                  'phone', 'date_joined')

    interests = fields.Field()

    def dehydrate_interests(self, book):
        return book.interested

class AppUserChangeForm(UserChangeFormAdmin):
    class Meta(UserChangeForm.Meta):
        model = AppUser


class AppUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = AppUser

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            AppUser.objects.get(email=email)
        except AppUser.DoesNotExist:
            return email
        raise forms.ValidationError(self.error_messages['duplicate_email'])


class UserAdminExport(ExportActionModelAdmin, UserAdmin):
    resource_class = UserResource

class AppUserAdmin(UserAdminExport):
    form = AppUserChangeForm
    add_form = AppUserCreationForm
    fieldsets = (
        (None, {'fields': ('email', 'password', "first_name", "last_name")}),
        (_('Contact info'), {'fields': ('company', 'business_type', 'phone', 'city', 'state', 'country', 'interested_in', 'account', 'is_account_admin')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'receive_newsletter',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': 'wide',
            'fields': ('email', 'password1', 'password2', "first_name", "last_name")}),
    )
    list_display = ('email', 'first_name', 'last_name', 'company', 'phone', 'country', 'date_joined', 'interested',
                    'is_active', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'receive_newsletter', 'groups', 'date_joined')
    search_fields = ('email','first_name','last_name','company','phone')

    ordering = ('last_name',)
    filter_horizontal = ('groups', 'user_permissions', 'interested_in')


admin.site.register(AppUser, AppUserAdmin)

class AccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'city', 'state', 'postal_code', 'country', 'phone', 'created_at', 'updated_at')
    search_fields = ('name', 'address', 'city', 'state', 'postal_code', 'country', 'phone')
    list_filter = ('country', )

class BusinessTypeAdmin(admin.ModelAdmin):
    list_display = ('name', )


class ClientInterestsAdmin(admin.ModelAdmin):
    list_display = ('name',)


class SoftwareProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at', 'active')


class SoftwareModuleInline(admin.TabularInline):
    model = SoftwareProductPricing.software_modules.through

class SoftwareProductPricingAdmin(admin.ModelAdmin):
    list_display = ('name', 'software', 'price', 'created_at', 'updated_at', 'active')
    exclude = ['software_modules']
    inlines = [SoftwareModuleInline]


class SoftwareModuleAdmin(admin.ModelAdmin):
    list_display = ('name', 'software', 'price', 'created_at', 'updated_at', 'active')

class OrderItemInline(admin.TabularInline):
    model = SoftwareOrderItem

class PaymentsInline(admin.TabularInline):
    model = Payment

class SoftwareOrderAdmin(admin.ModelAdmin):
    inlines = [
        OrderItemInline
    ]
    list_display = ('order_code', 'user', 'total', 'created_at', 'is_completed')
    raw_id_fields = ['user']


class HeaderExtensionAdmin(PageExtensionAdmin):
    pass


class HighlightedMenuExtensionAdmin(PageExtensionAdmin):
    pass


admin.site.register(HighlightedMenuExtension, HighlightedMenuExtensionAdmin)

admin.site.register(HeaderBackgroundExtension, HeaderExtensionAdmin)

admin.site.register(BusinessType, BusinessTypeAdmin)
admin.site.register(ClientInterests, ClientInterestsAdmin)
admin.site.register(SoftwareProduct, SoftwareProductAdmin)
admin.site.register(SoftwareProductPricing, SoftwareProductPricingAdmin)
admin.site.register(SoftwareModule, SoftwareModuleAdmin)
admin.site.register(SoftwareOrder, SoftwareOrderAdmin)
admin.site.register(Account, AccountAdmin)


