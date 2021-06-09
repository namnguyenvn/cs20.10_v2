from django.utils.translation import ugettext as _
import hashlib
from django.db import models
import uuid


class BaseModel(models.Model):
    created_at = models.DateTimeField(
        _('Created at'), auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(
        _('Updated at'), auto_now=True, null=True, blank=True)

    class Meta:
        abstract = True


class DeviceGroup(BaseModel):
    """
    Description: Model Description
    """
    name = models.CharField(_('Name'), max_length=255)

    class Meta:
        db_table = 'device_groups'
        verbose_name = 'Device Group'
        verbose_name_plural = 'Device Groups'

    def __str__(self):
        return self.name


class Device(BaseModel):
    name = models.CharField(_('Name'), max_length=255)
    ip = models.CharField(_('IP Address'), max_length=255)
    ROLES = [
        ('MASTER', _('Master')),
        ('SLAVE', _('Slave')),
        ('NA', _('N/A'))
    ]
    role = models.CharField(max_length=10, choices=ROLES, default='NA')
    parent_device = models.ForeignKey(
        'self', blank=True,
        null=True,
        related_name='children',
        on_delete=models.SET_NULL)
    group = models.ForeignKey(DeviceGroup, blank=True, null=True,
                              related_name='devices', on_delete=models.SET_NULL)

    class Meta:
        db_table = 'devices'
        verbose_name = 'Device'
        verbose_name_plural = 'Devices'

    def __str__(self):
        return self.name


class DeviceTemp(models.Model):

    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    temp = models.CharField(_('Temp'), max_length=255)
    timestamp = models.CharField(_('Timestamp'), max_length=255)

    class Meta:
        verbose_name = _("Device Temp")
        verbose_name_plural = _("Device Temps")

    def __str__(self):
        return self.device.name


class RollbackLog(models.Model):
    type = models.CharField(_('Type'), max_length=255)
    # device = models.ForeignKey(
    #     Device, on_delete=models.CASCADE, related_name='rollback_logs', null=True, blank=True)
    detail = models.TextField(_('Detail'), null=True, blank=True)
    time_execution = models.FloatField(
        _('Time Execution'), null=True, blank=True)
    created_at = models.DateTimeField(
        _('Created at'), auto_now_add=True, null=True, blank=True)

    class Meta:
        verbose_name = _("Rollback Log")
        verbose_name_plural = _("Rollback Logs")

    def __str__(self):
        return self.type


class PackageVersion(models.Model):

    device = models.CharField(_('Device'), max_length=255)
    version = models.CharField(_('Version'), max_length=255)
    file = models.FileField(upload_to='file-versions')
    tx_hash = models.CharField(
        _('Tx Hash'), max_length=255, default=uuid.uuid4().hex)
    file_hash = models.CharField(_('File Hash'), max_length=255)
    note = models.CharField(_('Note'), max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(
        _('Created at'), auto_now_add=True, null=True, blank=True)

    class Meta:
        verbose_name = _("Package Version")
        verbose_name_plural = _("Package Versions")

    def __str__(self):
        return self.device
