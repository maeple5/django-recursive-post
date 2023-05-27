# from django.contrib import admin

# # Register your models here.
# # from django.contrib.auth.models import User
# from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
# from .models import User, Profile
# from django.utils.translation import gettext_lazy as _

# # Register your models here.

# class ProfileInline(admin.StackedInline):
#     model = Profile
#     max_num = 1
#     can_delete = False

# class UserAdmin(AuthUserAdmin):
#     inlines = [ProfileInline]
#     fieldsets = ( 
#         (None, {
#             "fields": (
#                 "screen_user_id",
#                 'password',
#                 'email',
#                 'is_active',
#                 'is_staff',
#                 'is_superuser',
#             ),
#         }),
#     )   
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': (
#                 "screen_user_id",
#                 'password',
#                 'email',
#                 'is_active',
#                 'is_staff',
#                 'is_superuser',
#             ),
#         }),
#     )

#     list_display = (
#         'screen_user_id',
#         'created_at',
#         'id',
#     )
#     list_filter = (
#         # "is_staff", 
#         "is_superuser", 
#         "is_active", 
#         "groups",
#     )

#     search_fields = ("screen_user_id", "id")
#     list_display_links = ("screen_user_id", "id")
#     ordering = ("screen_user_id", "created_at")

# # admin.site.unregister(User)
# admin.site.register(User, UserAdmin)