import os
import subprocess
import datetime

from django.utils.translation import ugettext as _

from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True, null=True, blank=True)

    class Meta:
        abstract = True


class DeviceGroup(models.BaseModel):
    """
    Description: Model Description
    """
    name = models.CharField(_('Name'), max_length=255)

    class Meta:
        db_table = 'device_groups'
