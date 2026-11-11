from decimal import Decimal, InvalidOperation
from django import template
from django.utils.safestring import mark_safe
from ..models import Category, GeneralCategory

register = template.Library()


@register.filter
def convert(value, rate):
    """Qiyməti valyuta məzənnəsi ilə vurur və onluq hissəni qoruyur."""
    try:
        return Decimal(str(value)) * Decimal(str(rate))
    except (InvalidOperation, TypeError, ValueError):
        return value


@register.inclusion_tag('includes/nav-categories.html')
def nav_categories():
    pure_categories = Category.objects.filter(general_category__isnull=True)
    general_categories = GeneralCategory.objects.all()
    return {
        'pure_categories': pure_categories,
        'general_categories': general_categories
    }


@register.simple_tag(takes_context=True)
def query_transform(context, **kwargs):
    """Mövcud GET parametrlərini saxlayaraq istənilən parametri yeniləyir və ya əlavə edir."""
    request = context.get('request')
    if not request:
        return ''
    query_dict = request.GET.copy()
    for key, value in kwargs.items():
        if value is not None:
            query_dict[key] = value
        else:
            query_dict.pop(key, None)
    return query_dict.urlencode()


@register.simple_tag
def render_stars(rating, tag='small'):
    """Verilmiş reytinqə uyğun ulduzları (tam, yarım, boş) HTML formatında qaytarır."""
    try:
        r = float(rating or 0)
    except (ValueError, TypeError):
        r = 0.0
    full = int(r)
    half = 1 if (r - full) >= 0.5 else 0
    empty = max(0, 5 - full - half)

    t = tag if tag in ['small', 'i'] else 'small'
    html = []
    for _ in range(full):
        html.append(f'<{t} class="fas fa-star text-primary mr-1"></{t}>')
    if half:
        html.append(f'<{t} class="fas fa-star-half-alt text-primary mr-1"></{t}>')
    for _ in range(empty):
        html.append(f'<{t} class="far fa-star text-primary mr-1"></{t}>')
    return mark_safe(''.join(html))
