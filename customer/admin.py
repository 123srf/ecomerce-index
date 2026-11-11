from django.contrib import admin
from .models import WishItem, BasketItem, Customer, ContactMessage, ContactInfo


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('created_at',)
    list_editable = ('is_read',)
    date_hierarchy = 'created_at'


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ('address', 'email', 'phone')

    def has_add_permission(self, request):
        # Əgər artıq 1 qeyd varsa, yenisini əlavə etməyə ehtiyac yoxdur, yalnız mövcud olanı redaktə edilsin
        if self.model.objects.count() >= 1:
            return False
        return super().has_add_permission(request)
