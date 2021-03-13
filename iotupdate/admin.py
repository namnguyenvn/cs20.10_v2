from django.contrib import admin
from .models import *


class DeviceGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')


admin.site.register(DeviceGroup, DeviceGroupAdmin)


class DeviceAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'parent_device', 'created_at', 'updated_at')


admin.site.register(Device, DeviceAdmin)
