from django.contrib import admin
from django.contrib.auth.models import User
from . import models as api_models

# Register your models here.
admin.site.register(api_models.User)
# admin.site.register(api_models.User)
admin.site.register(api_models.Message)
admin.site.register(api_models.Conversation)

