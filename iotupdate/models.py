from django.utils.translation import ugettext as _

from django.db import models


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

    device = models.ForeignKey(
        Device, on_delete=models.CASCADE, related_name='rollback_logs')
    detail = models.TextField(_('Detail'), null=True, blank=True)
    time_execution = models.FloatField(
        _('Time Execution'), null=True, blank=True)
    created_at = models.DateTimeField(
        _('Created at'), auto_now_add=True, null=True, blank=True)

    class Meta:
        verbose_name = _("Rollback Log")
        verbose_name_plural = _("Rollback Logs")

    def __str__(self):
        return self.device.name
