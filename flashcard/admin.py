from django.contrib import admin

from . import models

admin.site.register(models.Flashcard)
admin.site.register(models.Stack)
