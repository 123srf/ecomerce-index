from django.contrib import admin
from modeltranslation.admin import TranslationAdmin, TranslationTabularInline
from .models import Size, Color, GeneralCategory, Category, Campaign, Product, ProductImage, Review


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    readonly_fields = ['image_tag']
    extra = 1


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0
    readonly_fields = ['created_at']
    fields = ['name', 'email', 'rating', 'message', 'is_approved', 'created_at']


@admin.register(Product)
class ProductAdmin(TranslationAdmin):
    inlines = [ProductImageInline, ReviewInline]
    list_display = ['title', 'price', 'old_price', 'featured', 'created_at']
    list_filter = ['categories', 'featured', 'campaigns']
    search_fields = ['title', 'description']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'name', 'email', 'rating', 'is_approved', 'created_at']
    list_filter = ['is_approved', 'rating', 'created_at']
    search_fields = ['name', 'email', 'message', 'product__title']
    list_editable = ['is_approved']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'


@admin.register(GeneralCategory)
class GeneralCategoryAdmin(TranslationAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    pass


@admin.register(Campaign)
class CampaignAdmin(TranslationAdmin):
    pass


admin.site.register(Size)
admin.site.register(Color)
admin.site.register(ProductImage)
