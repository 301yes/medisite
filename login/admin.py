# login/admin.py
from django.contrib import admin
from . import models

admin.site.register([models.User,models.FraudText,models.TagText,models.FraudClass])

