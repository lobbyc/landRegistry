from django.contrib import admin
from django.utils.html import format_html

# Register your models here.

from django.contrib import admin
from django.core.mail import send_mail
from django.http import HttpResponse
from django.urls import reverse
import csv

# Import your models
from .models import Landmark, Location, OwnerDetail, GreenCard

# Customize the site header
admin.site.site_header = "Land Registry"

class LandmarkAdmin(admin.ModelAdmin):
    def get_image(self, obj):
        return format_html('<img src="{}" width="50" height="50" />', obj.sheet_image.url)
        
    get_image.short_description = "Image"
    
    list_display = ['location', 'owner', 'deed_no', 'sheet_no', 'get_image']
    search_fields = ['sheet_no', 'deed_no']

class GreenCardAdmin(admin.ModelAdmin):
    list_display = ('card_number', 'expiration_date', 'land', 'owner')
    actions = ['download_green_cards', 'share_green_cards_with_email']

    def download_green_cards(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="green_cards.csv"'

        writer = csv.writer(response)
        writer.writerow(["Card Number", "Expiration Date", "Landmark", "Owner"])
        for green_card in queryset:
            writer.writerow([green_card.card_number, green_card.expiration_date, green_card.land.name, green_card.owner.first_name])

        return response

    download_green_cards.short_description = "Download selected Green Cards as CSV"

    def share_green_cards_with_email(self, request, queryset):
        admin_url = reverse(
            'admin:%s_%s_changelist' % (
                queryset.model._meta.app_label,
                queryset.model._meta.model_name,
            ),
            current_app=self.admin_site.name,
        )

        subject = 'Shared Green Cards from Your Website'
        message = 'Here are the Green Cards you requested: %s' % (admin_url,)
        from_email = 'muusyajapheth12@gmail.com'
        recipient_list = ['muusyajapheth01@gmail.com']

        send_mail(subject, message, from_email, recipient_list)
        self.message_user(request, 'Green Cards shared via email successfully.')

    share_green_cards_with_email.short_description = "Share selected Green Cards via Email"

# Register your models with the custom admin classes

class LocationAdmin(admin.ModelAdmin):
    model = Location
    list_display = ['county','sub_county','home_location','sub_location']


class OwnerAdmin(admin.ModelAdmin):
    model = OwnerDetail
    list_display = ['first_name','last_name','email','id_number']


admin.site.register(Landmark, LandmarkAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(OwnerDetail, OwnerAdmin)
admin.site.register(GreenCard, GreenCardAdmin)


