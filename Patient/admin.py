from django.contrib import admin
from .models import Address, Area, City, Profile

# Register your models here.
admin.site.register(Address)
admin.site.register(Area)
admin.site.register(City)
admin.site.register(Profile)
