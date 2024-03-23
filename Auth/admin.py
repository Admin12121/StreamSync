from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Video)
admin.site.register(Comment)
admin.site.register(LiveStream)
admin.site.register(News)
admin.site.register(Events)
admin.site.register(UserInfo)