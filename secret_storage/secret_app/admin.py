from django.contrib import admin
from secret_app.models import Secret


class SecretAdmin(admin.ModelAdmin):
    pass


admin.site.register(Secret, SecretAdmin)
