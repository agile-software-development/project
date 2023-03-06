from django.contrib import admin
from . import models
# Register your models here.


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = [field.name for field in models.User._meta.fields]
