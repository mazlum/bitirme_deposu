from django.contrib import admin
from forms import ProfileAdminForm
from models import Users, City


class UsersAdmin(admin.ModelAdmin):
    form = ProfileAdminForm


admin.site.register(Users, UsersAdmin)
admin.site.register(City)