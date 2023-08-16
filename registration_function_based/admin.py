from django.contrib import admin
from .models import UserProfile
from .models import ResetToken

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'age', 'gender')  # Customize the displayed fields
    # Add any other configuration options you want

# Register the UserProfileAdmin class
admin.site.register(UserProfile, UserProfileAdmin)

class ResetTokenAdmin(admin.ModelAdmin):
    list_display = ('user','token')  # Customize the displayed fields

admin.site.register(ResetToken, ResetTokenAdmin)