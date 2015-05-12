from django.contrib import admin
from forms import ProfileAdminForm, ThesisAdminForm
from models import *
from django.contrib.admin.widgets import AdminFileWidget
from django.utils.safestring import mark_safe


class ImageWidget(AdminFileWidget):
    def render(self, name, value, attrs=None):
        output = []
        if value and hasattr(value, "url"):
            output.append(('<a target="_blank" href="%s">'
                           '<img src="%s" title="%s"/></a>'
                           % (value.url, value.url, value.name)))
        output.append(super(AdminFileWidget, self).render(name, value, attrs))
        return mark_safe(u''.join(output))


class UsersAdmin(admin.ModelAdmin):
    form = ProfileAdminForm
    list_display = ['username', 'university', 'department', 'grade', 'city', 'sex', 'image_thumb']

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'image':
            request = kwargs.pop("request", None)
            kwargs['widget'] = ImageWidget
            return db_field.formfield(**kwargs)
        return super(UsersAdmin, self).formfield_for_dbfield(db_field, **kwargs)


class ThesisAdmin(admin.ModelAdmin):
    form = ThesisAdminForm
    list_display = ['name', 'user']
    filter_horizontal = ['image', 'file']


class ImageAdmin(admin.ModelAdmin):
    list_display = ['image', 'image_thumb']

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'image':
            request = kwargs.pop("request", None)
            kwargs['widget'] = ImageWidget
            return db_field.formfield(**kwargs)
        return super(ImageAdmin, self).formfield_for_dbfield(db_field, **kwargs)


admin.site.register(Users, UsersAdmin)
admin.site.register(City)
admin.site.register(Thesis, ThesisAdmin)
admin.site.register(File)
admin.site.register(Image, ImageAdmin)

