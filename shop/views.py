from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from .models import Campaign, Category, Product, Size, Color
from .forms import ReviewForm
from .context_processors import RATES, SYMBOLS


def _currency_context(request):
    """Sessiyadan seçilmiş valyutanı oxuyub məzənnə və simvolu qaytarır."""
    currency = request.session.get('currency', 'USD')
    return {
        'currency': currency,
        'currency_rate': RATES.get(currency, 1),
        'currency_symbol': SYMBOLS.get(currency, '$'),
    }


def _apply_calculated_prices(products, currency_rate):
    """Hər məhsulun qiymətini məzənnəyə vurub calculated_price kimi əlavə edir."""
    for product in products:
        product.calculated_price = product.price * currency_rate
        product.calculated_old_price = (
            product.old_price * currency_rate if product.old_price else None
        )
    return products


def set_currency(request):
    currency = request.GET.get('currency', 'USD')
    request.session['currency'] = currency
    # İstifadəçinin əvvəl olduğu səhifəyə qayıtması üçün:
    return redirect(request.META.get('HTTP_REFERER', '/'))


def home(request):
    context = _currency_context(request)
    rate = context['currency_rate']

    slide_campaigns = Campaign.objects.filter(is_slider=True)[:3]
    nonslide_campaigns = Campaign.objects.filter(is_slider=False)[:4]
    if not nonslide_campaigns.exists():
        nonslide_campaigns = Campaign.objects.all()[:4]

    categories = Category.objects.annotate(product_count=Count('products'))
    featured_products = list(Product.objects.filter(featured=True)[:8])
    recent_products = list(Product.objects.all().order_by('-created_at')[:8])

    _apply_calculated_prices(featured_products, rate)
    _apply_calculated_prices(recent_products, rate)

    context.update({
        'slide_campaigns': slide_campaigns,
        'nonslide_campaigns': nonslide_campaigns,
        'categories': categories,
        'featured_products': featured_products,
        'recent_products': recent_products,
    })
    return render(request, 'home.html', context)


SORT_OPTIONS = {
    'latest': {'label': 'Latest', 'order': '-created_at'},
    'oldest': {'label': 'Oldest', 'order': 'created_at'},
    'price_low': {'label': 'Price: Low to High', 'order': 'price'},
    'price_high': {'label': 'Price: High to Low', 'order': '-price'},
    'name_asc': {'label': 'Name: A to Z', 'order': 'title'},
    'name_desc': {'label': 'Name: Z to A', 'order': '-title'},
}

SHOWING_CHOICES = [3, 6, 9, 12, 24]


def product_list(request):
    context = _currency_context(request)
    rate = context['currency_rate']

    products_qs = Product.objects.all()

    # Kateqoriyaya görə filter
    category_id = request.GET.get('category')
    if category_id and str(category_id).isdigit():
        products_qs = products_qs.filter(categories__id=int(category_id))

    # Axtarış
    query = request.GET.get('q')
    if query:
        products_qs = products_qs.filter(title__icontains=query)

    # Sıralama (Sorting)
    sort_key = request.GET.get('sort', 'latest')
    if sort_key not in SORT_OPTIONS:
        sort_key = 'latest'
    order_field = SORT_OPTIONS[sort_key]['order']
    products_qs = products_qs.order_by(order_field)

    # Göstəriləcək say (Showing) - default olaraq 3 məhsul (istifadəçi menyudan 6, 9, 12, 24 də seçə bilər)
    showing_param = request.GET.get('showing', '3')
    try:
        per_page = int(showing_param)
        if per_page not in SHOWING_CHOICES:
            per_page = 3
    except (ValueError, TypeError):
        per_page = 3

    # Görünüş növü (Grid və ya List)
    view_mode = request.GET.get('view', 'grid')
    if view_mode not in ['grid', 'list']:
        view_mode = 'grid'

    # Səhifələmə (Pagination)
    paginator = Paginator(products_qs, per_page)
    page_number = request.GET.get('page', 1)
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    # Səhifə nömrələri siyahısı (çoxluq olduqda elided göstərilməsi)
    try:
        page_range = paginator.get_elided_page_range(page_obj.number, on_each_side=2, on_ends=1)
    except Exception:
        page_range = paginator.page_range

    # Cari səhifədəki məhsullara valyuta məzənnəsini tətbiq et
    _apply_calculated_prices(page_obj.object_list, rate)

    categories = Category.objects.annotate(product_count=Count('products'))
    sizes = Size.objects.all()
    colors = Color.objects.all()

    context.update({
        'products': page_obj.object_list,
        'page_obj': page_obj,
        'paginator': paginator,
        'page_range': page_range,
        'categories': categories,
        'sizes': sizes,
        'colors': colors,
        'selected_category': int(category_id) if category_id and str(category_id).isdigit() else None,
        'query': query or '',
        'sort_key': sort_key,
        'sort_label': SORT_OPTIONS[sort_key]['label'],
        'sort_options': SORT_OPTIONS,
        'showing': per_page,
        'showing_choices': SHOWING_CHOICES,
        'view_mode': view_mode,
    })
    return render(request, 'product-list.html', context)


def product_detail(request, pk):
    context = _currency_context(request)
    rate = context['currency_rate']

    product = get_object_or_404(Product, pk=pk)
    _apply_calculated_prices([product], rate)

    show_reviews_tab = request.GET.get('tab') == 'reviews'

    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.product = product
            if request.user.is_authenticated:
                review.user = request.user
            review.save()
            messages.success(request, 'Rəyiniz uğurla göndərildi.')
            return redirect(f"{reverse('shop:product-detail', kwargs={'pk': pk})}?tab=reviews")
        show_reviews_tab = True
    else:
        review_form = ReviewForm()
        if request.user.is_authenticated:
            review_form.fields['name'].initial = (
                request.user.get_full_name() or request.user.username
            )
            if request.user.email:
                review_form.fields['email'].initial = request.user.email

    related_products = list(
        Product.objects.filter(categories__in=product.categories.all())
        .exclude(pk=product.pk)
        .distinct()[:4]
    )
    if not related_products:
        related_products = list(Product.objects.exclude(pk=product.pk)[:4])
    _apply_calculated_prices(related_products, rate)

    context.update({
        'product': product,
        'related_products': related_products,
        'reviews': product.approved_reviews.all(),
        'review_form': review_form,
        'show_reviews_tab': show_reviews_tab,
    })
    return render(request, 'product-detail.html', context)


def product_detail_default(request):
    """Navbar-dakı 'Shop Detail' birbaşa vurulduqda ilk məhsula və ya məhsullar səhifəsinə yönləndirir."""
    product = Product.objects.first()
    if product:
        return redirect('shop:product-detail', pk=product.pk)
    return redirect('shop:product-list')
