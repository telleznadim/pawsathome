from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, PetOwnerProfile, PetSitterProfile, Avatar

admin.site.register(CustomUser, UserAdmin)
admin.site.register(PetOwnerProfile)
admin.site.register(PetSitterProfile)
admin.site.register(Avatar)
