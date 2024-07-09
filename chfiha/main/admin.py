from django.contrib import admin
from .models import Service, Profile, Project

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'profile_picture', 'is_client', 'is_freelancer')
    list_filter = ('is_client', 'is_freelancer')
    search_fields = ('user__email',)

admin.site.register(Profile, ProfileAdmin)

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'price_basic', 'price_standard', 'price_premium')
    search_fields = ('title', 'description')

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'client', 'freelancer', 'service', 'start_date', 'end_date')
    search_fields = ('order_number', 'client__email', 'freelancer__email', 'service__title')
    list_filter = ('start_date', 'end_date')
    fieldsets = (
        (None, {
            'fields': ('order_number', 'client', 'freelancer', 'service', 'description', 'start_date', 'end_date')
        }),
        ('Delivery Steps', {
            'fields': (
                ('step1_status', 'step1_file'),
                ('step2_status', 'step2_file'),
                ('step3_status', 'step3_file'),
                ('step4_status', 'step4_file'),
                ('step5_status', 'step5_file'),
            )
        }),
    )

admin.site.register(Project, ProjectAdmin)

