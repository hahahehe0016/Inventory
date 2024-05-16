from django.contrib.admin.models import LogEntry, ADDITION, DELETION, CHANGE
from django.contrib.contenttypes.models import ContentType
from .models import User
from django.utils.encoding import force_str
from django.contrib.admin.models import LogEntryManager


def log_addition(request):
    return LogEntry.objects.log_action(
            user_id= User.pk,
            content_type_id=ContentType.objects.get_for_model(object).pk,
            object_id=object.pk,
            object_repr=force_str(object),
            action_flag=ADDITION,
    )

