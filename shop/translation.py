from modeltranslation.translator import register, TranslationOptions
from .models import Product, Category, GeneralCategory, Campaign

@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ('title', 'description')

@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('title',)

@register(GeneralCategory)
class GeneralCategoryTranslationOptions(TranslationOptions):
    fields = ('title',)

@register(Campaign)
class CampaignTranslationOptions(TranslationOptions):
    fields = ('title', 'description')