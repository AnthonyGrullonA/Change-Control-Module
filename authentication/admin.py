from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser, EmailGroup

class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', )}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_superuser'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'date_joined')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

admin.site.register(CustomUser, CustomUserAdmin)

class EmailGroupMemberInline(admin.TabularInline):
    model = EmailGroup.members.through
    extra = 1
    #verbose_name_plural = 'Members'

@admin.register(EmailGroup)
class EmailGroupAdmin(admin.ModelAdmin):
    inlines = (EmailGroupMemberInline,)
    list_display = ('name',)
    search_fields = ('name',)
    fields = ('name', 'members')
    readonly_fields = ['members']



