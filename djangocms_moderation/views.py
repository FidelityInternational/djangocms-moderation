from __future__ import unicode_literals

from django.contrib import messages
from django.shortcuts import get_object_or_404, render
from django.utils.translation import ugettext_lazy as _
from django.views.generic import FormView

from cms.utils.urlutils import add_url_parameters

from .forms import ItemToCollectionForm
from .models import ConfirmationPage, ModerationCollection
from .utils import get_admin_url

from . import constants  # isort:skip


class ItemToCollectionView(FormView):
    template_name = 'djangocms_moderation/item_to_collection.html'
    form_class = ItemToCollectionForm
    success_template_name = 'djangocms_moderation/request_finalized.html'

    def get_form_kwargs(self):
        kwargs = super(ItemToCollectionView, self).get_form_kwargs()
        kwargs['initial'].update({
            'content_object_id': self.request.GET.get('content_object_id')
        })

        return kwargs

    def form_valid(self, form):
        collection = form.cleaned_data['collection']
        content_object = form.cleaned_data['content_object']
        collection.add_object(content_object)

        messages.success(self.request, _('Item successfully added to moderation collection'))
        return render(self.request, self.success_template_name, {})

    def get_context_data(self, **kwargs):

        context = super(ItemToCollectionView, self).get_context_data(**kwargs)
        opts_meta = ModerationCollection._meta
        collection_list = ModerationCollection.objects.filter(is_locked=False)
        collection_id = self.request.GET.get('collection_id')
        content_object_list = []

        if collection_list:
            if collection_id:
                collection = ModerationCollection.objects.get(pk=collection_id)
            else:
                collection = collection_list[0]
                collection_id = collection.pk

            content_object_list = collection.moderation_requests.all()

        context.update({
            'collection_id': int(collection_id),
            'collection_list': collection_list,
            'content_object_list':  content_object_list,
            'opts': opts_meta,
            'title': _('Add to collection'),
        })

        return context


item_to_collection = ItemToCollectionView.as_view()


def moderation_confirmation_page(request, confirmation_id):
    confirmation_page_instance = get_object_or_404(ConfirmationPage, pk=confirmation_id)
    content_view = bool(request.GET.get('content_view'))
    page_id = request.GET.get('page')
    language = request.GET.get('language')

    # Get the correct base template depending on content/build view
    if content_view:
        base_template = 'djangocms_moderation/base_confirmation.html'
    else:
        base_template = 'djangocms_moderation/base_confirmation_build.html'

    context = {
        'opts': ConfirmationPage._meta,
        'app_label': ConfirmationPage._meta.app_label,
        'change': True,
        'add': False,
        'is_popup': True,
        'save_as': False,
        'has_delete_permission': False,
        'has_add_permission': False,
        'has_change_permission': True,
        'instance': confirmation_page_instance,
        'is_form_type': confirmation_page_instance.content_type == constants.CONTENT_TYPE_FORM,
        'content_view': content_view,
        'CONFIRMATION_BASE_TEMPLATE': base_template,
    }

    if request.method == 'POST' and page_id and language:
        context['submitted'] = True
        context['redirect_url'] = add_url_parameters(
            get_admin_url(
                name='cms_moderation_approve_request',
                language=language,
                args=(page_id, language),
            ),
            reviewed=True,
        )
    return render(request, confirmation_page_instance.template, context)
