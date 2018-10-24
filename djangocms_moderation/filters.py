
from django.contrib import admin
from django.contrib.auth.models import User
from django.db.models import Q
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _

from . import constants
from . import helpers


class ModeratorFilter(admin.SimpleListFilter):
    """
    Provides a moderator filter limited to those users who have authored collections
    """
    title = _("moderator")
    parameter_name = "moderator"

    def lookups(self, request, model_admin):
        options = []
        moderators = User.objects.filter(moderationcollection__author__isnull=False).distinct()
        for user in moderators:
            options.append((force_text(user.pk), user.get_full_name() or user.get_username()))
        return options

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(
                author=self.value()
            ).distinct()
        return queryset


class ReviewerFilter(admin.SimpleListFilter):
    title = _("reviewer")
    parameter_name = "reviewer"
    currentuser = {}

    def lookups(self, request, model_admin):
        """
        Provides a reviewers filter if there are any reviewers
        """
        self.currentuser = request.user

        options = []
        # collect all unique users from the three queries
        for user in User.objects.filter(
            Q(groups__role__workflowstep__workflow__moderation_collections__isnull=False) |
            Q(role__workflowstep__workflow__moderation_collections__isnull=False)).distinct():
            options.append((force_text(user.pk), user.get_full_name() or user.get_username()))
        return options

    def queryset(self, request, queryset):
        if self.value() and self.value() != 'all':
            result = queryset.filter(
                Q(moderation_requests__actions__to_user=self.value()) |
                # also include those that have been assigned to a role, instead of directly to a user
                (
                    # include any direct user assignments to actions
                    Q(moderation_requests__actions__to_user__isnull=True)
                    # exclude status COLLECTING as these will hot have reviewers assigned
                    & ~Q(status=constants.COLLECTING)
                    # include collections with group or role that matches current user
                    & (
                        Q(workflow__steps__role__user=self.value()) |
                        Q(workflow__steps__role__group__user=self.value())
                    )
                )
            ).distinct()

            return result
        return queryset

    def choices(self, changelist):
        yield {
            'selected': self.value() == 'all',
            'query_string': changelist.get_query_string({self.parameter_name: 'all'}, []),
            'display': _('All'),
        }
        for lookup, title in self.lookup_choices:
            yield {
                'selected': self.value() == force_text(lookup),
                'query_string': changelist.get_query_string({self.parameter_name: lookup}, []),
                'display': title,
            }
