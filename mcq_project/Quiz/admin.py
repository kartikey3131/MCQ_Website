from django.contrib import admin
from .import models
# Register your models here.
admin.site.register(models.Usertype)
admin.site.register(models.Question)
admin.site.register(models.Quiz)
admin.site.register(models.Marks_scored)