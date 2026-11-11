from .models import ContactInfo


def contact_info(request):
    """Bütün şablonlar üçün mağazanın əlaqə məlumatlarını (ünvan, telefon, e-poçt, xəritə) təmin edir."""
    info = ContactInfo.objects.first()
    return {
        'contact_info': info
    }

