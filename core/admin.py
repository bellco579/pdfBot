from django.contrib import admin
from .models import Message, Docs, Photo

# Register your models here.
admin.site.register(Message)
admin.site.register(Docs)
admin.site.register(Photo)
