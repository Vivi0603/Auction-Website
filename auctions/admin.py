from django.contrib import admin
from .models import User,Category,Listings,watchlist
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display=("id","categoryName")

class watchAdmin(admin.ModelAdmin):
    list_display=("id","watcher","listing")

admin.site.register(User)
admin.site.register(Category,CategoryAdmin)

admin.site.register(Listings)

admin.site.register(watchlist)