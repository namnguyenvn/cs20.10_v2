from django.contrib import admin
from .models import *


class DeviceGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')


admin.site.register(DeviceGroup, DeviceGroupAdmin)


class DeviceAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'ip', 'parent_device',
                    'created_at', 'updated_at')
    list_filter = ['role', 'ip', 'parent_device']


admin.site.register(Device, DeviceAdmin)


class DeviceTempAdmin(admin.ModelAdmin):
    list_display = ('device', 'temp', 'timestamp')
    list_filter = ['device']


admin.site.register(DeviceTemp, DeviceTempAdmin)


class RollbackLogAdmin(admin.ModelAdmin):
    list_display = ('type', 'detail', 'time_execution', 'created_at')
    list_filter = ['type', 'created_at']


admin.site.register(RollbackLog, RollbackLogAdmin)


class PackageVersionAdmin(admin.ModelAdmin):
    list_display = ('device', 'version', 'file_hash', 'note', 'created_at')
    list_filter = ['device', 'note']


admin.site.register(PackageVersion, PackageVersionAdmin)
