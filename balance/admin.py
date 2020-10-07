from django.contrib import admin
from .models import Company_info, Company, History_info
from  django.utils.timezone import now

class Company_infoInline(admin.TabularInline):
    model = Company_info

@admin.register(Company)
class Company_infoAdmin(admin.ModelAdmin):
    inlines = [Company_infoInline]

admin.site.register(Company_info)


#admin.site.register(Company)
#admin.site.register(Company_info)
admin.site.register(History_info)
