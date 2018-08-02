from __future__ import unicode_literals

from django.conf.urls import url
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.utils.html import format_html, format_html_join
from django.utils.translation import ugettext, ugettext_lazy as _

from cms.admin.placeholderadmin import PlaceholderAdminMixin
from cms.models import Page

from adminsortable2.admin import SortableInlineAdminMixin

from .forms import WorkflowStepInlineFormSet
from .helpers import get_form_submission_for_step
from .models import (
    ConfirmationFormSubmission,
    ConfirmationPage,
    ModerationRequest,
    ModerationCollection,
    ModerationRequestAction,
    Role,
    Workflow,
    WorkflowStep,
)


from . import views  # isort:skip


try:
    PageAdmin = admin.site._registry[Page].__class__
except KeyError:
    from cms.admin.pageadmin import PageAdmin


class ModerationRequestActionInline(admin.TabularInline):
    model = ModerationRequestAction
    fields = ['show_user', 'message', 'date_taken', 'form_submission']
    readonly_fields = fields
    verbose_name = _('Action')
    verbose_name_plural = _('Actions')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def show_user(self, obj):
        _name = obj.get_by_user_name()
        return ugettext('By {user}').format(user=_name)
    show_user.short_description = _('Status')

    def form_submission(self, obj):
        instance = get_form_submission_for_step(obj.request, obj.step_approved)

        if not instance:
            return ''

        opts = ConfirmationFormSubmission._meta
        url = reverse(
            'admin:{}_{}_change'.format(opts.app_label, opts.model_name),
            args=[instance.pk],
        )
        return format_html(
            '<a href="{}" target="_blank">{}</a>',
            url,
            obj.step_approved.role.name
        )
    form_submission.short_description = _('Form Submission')


class ModerationRequestAdmin(admin.ModelAdmin):
    inlines = [ModerationRequestActionInline]
    list_display = ['id', 'language', 'collection', 'show_status', 'date_sent']
    list_filter = ['language', 'collection', 'id', 'compliance_number']
    fields = ['id', 'collection', 'workflow', 'language', 'is_active', 'show_status', 'compliance_number']
    readonly_fields = fields

    def has_add_permission(self, request):
        return False

    def show_status(self, obj):
        if obj.is_approved():
            status = ugettext('Ready for publishing')
        elif obj.is_active and obj.has_pending_step():
            next_step = obj.get_next_required()
            role = next_step.role.name
            status = ugettext('Pending %(role)s approval') % {'role': role}
        else:
            last_action = obj.get_last_action()
            user_name = last_action.get_by_user_name()
            message_data = {
                'action': last_action.get_action_display(),
                'name': user_name,
            }
            status = ugettext('%(action)s by %(name)s') % message_data
        return status
    show_status.short_description = _('Status')


class RoleAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'group', 'confirmation_page']
    fields = ['name', 'user', 'group', 'confirmation_page']


class WorkflowStepInline(SortableInlineAdminMixin, admin.TabularInline):
    formset = WorkflowStepInlineFormSet
    model = WorkflowStep

    def get_extra(self, request, obj=None, **kwargs):
        if obj and obj.pk:
            return 0
        return 1


class WorkflowAdmin(admin.ModelAdmin):
    inlines = [WorkflowStepInline]
    list_display = ['name', 'is_default']
    fields = ['name', 'is_default', 'identifier', 'requires_compliance_number', 'compliance_number_backend']


class ModerationCollectionAdmin(admin.ModelAdmin):
    view_on_site = True

    def get_urls(self):
        def _url(regex, fn, name, **kwargs):
            return url(regex, self.admin_site.admin_view(fn), kwargs=kwargs, name=name)

        url_patterns = [
          _url(
                r'^item/add/$',
                views.item_to_collection,
                name='item_to_collection',
            )
        ]

        return url_patterns + super(ModerationCollectionAdmin, self).get_urls()


class ConfirmationPageAdmin(PlaceholderAdminMixin, admin.ModelAdmin):
    view_on_site = True

    def get_urls(self):
        def _url(regex, fn, name, **kwargs):
            return url(regex, self.admin_site.admin_view(fn), kwargs=kwargs, name=name)

        url_patterns = [
            _url(
                r'^moderation-confirmation-page/([0-9]+)/$',
                views.moderation_confirmation_page,
                name='cms_moderation_confirmation_page',
            ),
        ]
        return url_patterns + super(ConfirmationPageAdmin, self).get_urls()


class ConfirmationFormSubmissionAdmin(admin.ModelAdmin):
    list_display = ['moderation_request', 'for_step', 'submitted_at']
    fields = ['moderation_request', 'show_user', 'for_step', 'submitted_at', 'form_data']
    readonly_fields = fields

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save'] = False
        extra_context['show_save_and_continue'] = False
        return super(ConfirmationFormSubmissionAdmin, self).change_view(
            request, object_id, form_url, extra_context=extra_context,
        )

    def moderation_request(self, obj):
        return obj.request_id
    moderation_request.short_description = _('Request')

    def show_user(self, obj):
        return obj.get_by_user_name()
    show_user.short_description = _('By User')

    def form_data(self, obj):
        data = obj.get_form_data()
        return format_html_join(
            '',
            '<p>{}: <b>{}</b><br />{}: <b>{}</b></p>',
            ((ugettext('Question'), d['label'], ugettext('Answer'), d['value']) for d in data)
        )
    form_data.short_description = _('Form Data')


admin.site.register(ModerationRequest, ModerationRequestAdmin)
admin.site.register(ModerationCollection, ModerationCollectionAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(Workflow, WorkflowAdmin)

admin.site.register(ConfirmationPage, ConfirmationPageAdmin)
admin.site.register(ConfirmationFormSubmission, ConfirmationFormSubmissionAdmin)
