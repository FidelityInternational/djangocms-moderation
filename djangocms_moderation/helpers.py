from django.contrib.contenttypes.models import ContentType

from .models import ConfirmationFormSubmission, ModerationRequest, Workflow


def get_default_workflow():
    try:
        workflow = Workflow.objects.get(is_default=True)
    except Workflow.DoesNotExist:
        workflow = None
    return workflow


def get_moderation_workflow():
    # TODO for now just return default, this would need to depend on the collection
    # Might be as well not needed in 4.x, leaving it here for now
    return get_default_workflow()


def get_active_moderation_request(obj, language):
    content_type = ContentType.objects.get_for_model(obj)
    try:
        return ModerationRequest.objects.get(
            content_type=content_type,
            object_id=obj.pk,
            language=language,
            is_active=True,
        )
    except ModerationRequest.DoesNotExist:
        return None


def get_page_or_404(obj_id, language):
    """
    TODO is this needed in 4.x?
    """
    content_type = ContentType.objects.get(app_label="cms", model="page")  # how do we get this

    return content_type.get_object_for_this_type(
        pk=obj_id,
        is_page_type=False,
        pagecontent_set__language=language,
    )


def get_form_submission_for_step(active_request, current_step):
    lookup = (
        ConfirmationFormSubmission
        .objects
        .filter(request=active_request, for_step=current_step)
    )
    return lookup.first()


class EditAndAddOnlyFieldsMixin(object):
    editonly_fields = ()
    addonly_fields = ()

    def get_readonly_fields(self, request, obj=None):
        """
        Override to provide editonly_fields and addonly_fields functionality
        """
        if obj:  # Editing an existing object
            return self.readonly_fields + self.editonly_fields
        else:  # Adding a new object
            return self.readonly_fields + self.addonly_fields
