from django.contrib import admin
from . models import Hit, HitCount, BlacklistIP, BlacklistUserAgent
# Register your models here.
admin.site.register(Hit)
admin.site.register(HitCount)
admin.site.register(BlacklistIP)
admin.site.register(BlacklistUserAgent)