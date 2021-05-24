from django.db import models
from django.db.models.fields import GenericIPAddressField, IPAddressField

from django.utils.translation import ugettext as _


class GitServer(models.Model):

    name = models.CharField(_('Name'), max_length=255)
    ip = GenericIPAddressField(_('IP'))
    git_name = models.CharField(_('Git Name'), max_length=255)

    class Meta:
        verbose_name = _("Git Server")
        verbose_name_plural = _("Git Servers")

    def __str__(self):
        return self.name
