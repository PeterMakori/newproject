from django.contrib import admin
from authenticate.models import User, SendFeedback

# Register your models here.
admin.site.register(User)
admin.site.register(SendFeedback)

admin.site.site_header = 'Admin Portal'
