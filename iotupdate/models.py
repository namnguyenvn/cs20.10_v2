from django.utils.translation import ugettext as _

from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(
        _('Created at'), auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(
        _('Updated at'), auto_now=True, null=True, blank=True)

    class Meta:
        abstract = True


class DeviceGroup(models.BaseModel):
    """
    Description: Model Description
    """
    name = models.CharField(_('Name'), max_length=255)

    class Meta:
        db_table = 'device_groups'
        verbose_name = 'Device Group'
        verbose_name_plural = 'Device Groups'


class Device(models.BaseModel):
    name = models.CharField(_('Name'), max_length=255)
    ip = models.CharField(_('IP Address'), max_length=255)
    ROLES = [
        ('MASTER', _('Master')),
        ('SLAVE', _('Slave')),
        ('NA', _('N/A'))
    ]
    role = models.CharField(max_length=10, choices=ROLES, default='NA')
    parent_device = models.ForeignKey(
        Device, blank=True,
        null=True,
        related_name='parent_device',
        on_delete=models.SET_NULL)

    class Meta:
        db_table = 'devices'
        verbose_name = 'Device'
        verbose_name_plural = 'Devices'
