from django.core.mail import EmailMessage
from django.db.models import Q
from django.utils import translation
from django.utils.translation import ugettext_lazy as _
from django_rq import job

from django.contrib.auth import get_user_model
from whistle.helpers import notify


@job('exports')
def execute_export(exporter_class, exporter_params, language):
    # init exporter
    exporter = exporter_class(**exporter_params)

    # save export to DB
    export = exporter.save_export()

    # send mail with export to recipients
    export.send_mail(language, exporter_params.get('filename', None))


@job('exports')
def mail_export(export_id, language, filename=None):
    from outputs.models import Export
    export = Export.objects.get(id=export_id)

    export.status = Export.STATUS_PROCESSING
    export.save(update_fields=['status'])

    # set language
    translation.activate(language)

    # model = self.queryset.model
    model = export.content_type.model_class()
    verbose_name = model._meta.verbose_name_plural

    # get exporter
    exporter = export.exporter

    # get total number of exported items
    num_items = export.total

    # export data to stream
    try:
        exporter.export()
    except Exception as e:
        # update status of export
        export.status = Export.STATUS_FAILED
        export.save(update_fields=['status'])

        # details
        details = '{}: {}\n'.format(_('Creator'), export.creator)
        details += '{}: {}\n\n'.format(_('Total items'), num_items)
        details += exporter.get_message_body()
        details += '\n\n{}: {}\n\n'.format(_('Error'), str(e))

        notify_users = get_user_model().objects \
            .active()\
            .filter(
                Q(is_superuser=True) |
                Q(pk=export.creator.pk) |
                Q(pk__in=export.recipients.all())
            ).distinct()

        # notify creator, recipients and superusers about failed export
        for user in notify_users:
            notify(None, user, 'EXPORT_FAILED', object=export, target=export.content_type, details=details)

        raise

    message = get_message(
        exporter,
        count=num_items,
        recipient_list=export.recipients.values_list('email', flat=True),
        subject='{}: {}'.format(_('Export'), verbose_name),
        filename=filename
    )

    # update status of export
    export.status = Export.STATUS_FINISHED
    export.save(update_fields=['status'])

    # send
    return message.send(fail_silently=False)


def get_message(exporter, count, recipient_list, subject, filename=None):
    # message body
    body = '{}: {}\n\n'.format(_('Total items'), count)
    body += exporter.get_message_body()

    # prepare message
    message = EmailMessage(subject, body, to=recipient_list)

    # get the stream and set the correct mimetype
    message.attach(
        filename or exporter.get_filename(),
        exporter.get_output(),
        exporter.content_type
    )

    return message
