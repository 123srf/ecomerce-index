from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

# Create your models here.

class WishItem(models.Model):
    pass


class BasketItem(models.Model):
    pass


class Customer(models.Model):
    pass
    # user=models.OneToOneField(User,on_delete=models.CASCADE)


class ContactMessage(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Ad"))
    email = models.EmailField(verbose_name=_("E-poçt"))
    subject = models.CharField(max_length=200, verbose_name=_("Mövzu"))
    message = models.TextField(verbose_name=_("Mesaj"))
    is_read = models.BooleanField(default=False, verbose_name=_("Oxunub"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Göndərilmə tarixi"))

    class Meta:
        verbose_name = _('Əlaqə Mesajı')
        verbose_name_plural = _('Əlaqə Mesajları')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.subject}"


class ContactInfo(models.Model):
    address = models.CharField(
        max_length=255,
        default='123 Street, New York, USA',
        verbose_name=_("Ünvan")
    )
    email = models.EmailField(
        default='info@example.com',
        verbose_name=_("E-poçt")
    )
    phone = models.CharField(
        max_length=50,
        default='+012 345 67890',
        verbose_name=_("Telefon")
    )
    map_embed_url = models.TextField(
        default='https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3001156.4288297426!2d-78.01371936852176!3d42.72876761954724!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x4ccc4bf0f123a5a9%3A0xddcfc6c1de189567!2sNew%20York%2C%20USA!5e0!3m2!1sen!2sbd!4v1603794290143!5m2!1sen!2sbd',
        verbose_name=_("Google Xəritə Embed URL-i")
    )

    class Meta:
        verbose_name = _('Əlaqə Məlumatı')
        verbose_name_plural = _('Əlaqə Məlumatları')

    def __str__(self):
        return self.address
