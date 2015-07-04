from django.contrib import admin
from .models import userStats
# Register your models here.

class userStatsAdmin(admin.ModelAdmin):
    fields = ['username', 'timestamp', 'currentViewers', 'totalViews', 'followers']
    
admin.site.register(userStats, userStatsAdmin)