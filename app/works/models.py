from django.db import models
from django.conf import settings
from django.utils.translation import gettext as _


class Work(models.Model):
    """Work model definition"""

    STATUS_NOT_STARTED = "not started"
    STATUS_IN_PROGRESS = "in progress"
    STATUS_COMPLETE = "complete"

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateField()
    status = models.CharField(max_length=20,
                              choices=((STATUS_NOT_STARTED, _("Not started")),
                                       (STATUS_IN_PROGRESS, _("In progress")),
                                       (STATUS_COMPLETE, _("Complete"))),
                              default=STATUS_IN_PROGRESS)

    def __str__(self):
        return self.title
