from django.contrib import admin

# Register your models here.
from bot.models import Producer, CraneModel

admin.site.register(Producer)
admin.site.register(CraneModel)
