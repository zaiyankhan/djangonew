from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from helpdesk.models import Queue, Ticket, FollowUp, PreSetReply, KBCategory
from helpdesk.models import EscalationExclusion, EmailTemplate, KBItem
from helpdesk.models import TicketChange, Attachment, IgnoreEmail
from helpdesk.models import CustomField
from website.models import AppUser


@admin.register(Queue)
class QueueAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'email_address', 'locale')
    prepopulated_fields = {"slug": ("title",)}

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        context['adminform'].form.fields['default_owner'].queryset = AppUser.objects.filter(is_staff=True)
        return super().render_change_form(request, context, add, change, form_url, obj)


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'assigned_to', 'queue', 'submitter_email',)
    date_hierarchy = 'created'
    list_filter = ('queue', 'assigned_to', 'status')

    def hidden_submitter_email(self, ticket):
        if ticket.submitter_email:
            username, domain = ticket.submitter_email.split("@")
            username = username[:2] + "*" * (len(username) - 2)
            domain = domain[:1] + "*" * (len(domain) - 2) + domain[-1:]
            return "%s@%s" % (username, domain)
        else:
            return ticket.submitter_email
    hidden_submitter_email.short_description = _('Submitter E-Mail')

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        context['adminform'].form.fields['assigned_to'].queryset = AppUser.objects.filter(is_staff=True)
        return super().render_change_form(request, context, add, change, form_url, obj)


class TicketChangeInline(admin.StackedInline):
    model = TicketChange


class AttachmentInline(admin.StackedInline):
    model = Attachment


@admin.register(FollowUp)
class FollowUpAdmin(admin.ModelAdmin):
    inlines = [AttachmentInline]
    list_display = ['title', 'ticket', 'date', 'user', 'new_status']

    def save_form(self, request, form, change):
        followup = super().save_form(request, form, change)
        followup.user = request.user
        followup.save()
        return followup


@admin.register(KBItem)
class KBItemAdmin(admin.ModelAdmin):
    list_display = ('category', 'title', 'last_updated',)
    list_display_links = ('title',)


@admin.register(CustomField)
class CustomFieldAdmin(admin.ModelAdmin):
    list_display = ('name', 'label', 'data_type')


@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ('template_name', 'heading', 'locale')
    list_filter = ('locale', )


admin.site.register(PreSetReply)
admin.site.register(EscalationExclusion)
admin.site.register(KBCategory)
admin.site.register(IgnoreEmail)
