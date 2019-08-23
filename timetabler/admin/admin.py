from django.contrib import admin
# from .model import Snippet

# Register your models here.
# admin.site.register(Snippet)

from .models import FacultySummary

@admin.register(FacultySummary)
class FacultySummaryAdmin(ModelAdmin):
    change_list_template = 'admin/faculty_summary_change_list.html'
    date_hierarchy = 'created'
