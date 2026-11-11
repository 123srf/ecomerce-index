from django.db import models
from django.contrib.admin import display
from django.utils.html import format_html
from django.urls import reverse
from django.contrib.auth.models import User

# # Create your models here.


    
class Size(models.Model):
    title = models.CharField(max_length=10,unique=True)
    def __str__(self):
        return self.title

class Color(models.Model):
    title = models.CharField(max_length=20,unique=True)
    def __str__(self):
        return self.title

class GeneralCategory(models.Model):
    title=models.CharField(max_length=20)
    def __str__(self):
        return self.title

class Category(models.Model):
    title=models.CharField(max_length=20)
    image=models.ImageField(upload_to='categories')
    general_category=models.ForeignKey(GeneralCategory, on_delete=models.SET_NULL,blank=True, null=True, related_name='sub_categories')
    def __str__(self):
        return self.title

class  Campaign(models.Model):
    title=models.CharField(max_length=50)
    description=models.TextField()
    is_slider=models.BooleanField(default=False)
    image=models.ImageField(upload_to='campaigns')
    discount_percentage=models.FloatField()
    def __str__(self):
            return self.title
class  Product(models.Model):
    title=models.CharField(max_length=50)
    old_price=models.FloatField(blank=True, null=True)  #var
    featured=models.BooleanField(default=False)  #var
    price=models.FloatField()  #var
    description=models.TextField()
    sizes=models.ManyToManyField(Size, related_name='products')  #var
    colors=models.ManyToManyField(Color, related_name='products')  # var
    categories=models.ManyToManyField(Category, related_name='products')
    campaigns=models.ManyToManyField(Campaign, related_name='products')
    updated_at=models.DateTimeField(auto_now=True)
    created_at=models.DateTimeField(auto_now_add=True)                    
    def __str__(self):
        return self.title

    @property
    def approved_reviews(self):
        return self.reviews.filter(is_approved=True)

    @property
    def review_count(self):
        return self.approved_reviews.count()

    @property
    def average_rating(self):
        avg = self.approved_reviews.aggregate(models.Avg('rating'))['rating__avg']
        return round(avg, 1) if avg else 0.0

class  ProductImage(models.Model):
    product=models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image=models.ImageField(upload_to='product_images')

    @display(description="movcud sekil")
    def image_tag(self):
        return format_html(f'<img width="200" src="{self.image.url}" >')


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews', verbose_name="Məhsul")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="İstifadəçi")
    name = models.CharField(max_length=100, verbose_name="Ad")
    email = models.EmailField(verbose_name="E-poçt")
    rating = models.PositiveSmallIntegerField(
        default=5,
        choices=[(i, f"{i} ulduz") for i in range(1, 6)],
        verbose_name="Qiymətləndirmə"
    )
    message = models.TextField(verbose_name="Rəy")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Tarix")
    is_approved = models.BooleanField(default=True, verbose_name="Təsdiqlənib")

    class Meta:
        verbose_name = "Rəy"
        verbose_name_plural = "Rəylər"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.product.title} ({self.rating}★)"

        