from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category, Banner, Promotion, Manufacturer, Subscription
from django.db.models import Q
from django.views.decorators.cache import cache_page
from .forms import ReviewForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

def get_all_subcategories(category):
    subcategories = category.children.all()
    ids = []
    for sub in subcategories:
        ids.append(sub.id)
        ids += get_all_subcategories(sub)
    return ids

@cache_page(60 * 15)
def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.filter(parent__isnull=True)
    manufacturers = Manufacturer.objects.all()
    products = Product.objects.filter(available=True)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        sub_ids = get_all_subcategories(category)
        products = products.filter(Q(category=category) | Q(category__in=sub_ids))

    # Поиск
    query = request.GET.get('query')
    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))

    # Фильтрация по производителю
    manufacturer_name = request.GET.get('manufacturer')
    if manufacturer_name:
        products = products.filter(manufacturer__name=manufacturer_name)

    # Сортировка
    sort_by = request.GET.get('sort')
    if sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')

    paginator = Paginator(products, 9)  # Показывать по 9 товаров на странице
    page = request.GET.get('page')

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    return render(request, 'store/product_list.html', {
        'category': category,
        'products': products,
        'manufacturers': manufacturers,
        'current_manufacturer': manufacturer_name,
        'current_sort': sort_by,
        'current_query': query,
    })

def product_detail(request, product_slug):
    categories = Category.objects.all()
    product = get_object_or_404(Product, slug=product_slug, available=True)
    reviews = product.reviews.all()
    subscribed = False
    if request.user.is_authenticated:
        subscribed = Subscription.objects.filter(user=request.user, product=product).exists()
    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            new_review = review_form.save(commit=False)
            new_review.product = product
            new_review.user = request.user
            new_review.save()
            return redirect('store:product_detail', product_slug=product_slug)
    else:
        review_form = ReviewForm()
    return render(request, 'store/product_detail.html', {
        'product': product,
        'categories': categories,
        'reviews': reviews,
        'review_form': review_form,
        'subscribed': subscribed,
    })

@login_required
def subscribe_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    subscription, created = Subscription.objects.get_or_create(
        user=request.user, 
        product=product
    )
    
    if created:
        messages.success(request, f'Вы успешно подписались на товар "{product.name}"')
    else:
        subscription.delete()
        messages.info(request, f'Вы отписались от товара "{product.name}"')
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('store:home')))

def product_search(request):
    query = request.GET.get('query')
    categories = Category.objects.all()
    products = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query), available=True)
    return render(request, 'store/product_list.html', {
        'products': products,
        'categories': categories
    })

def home(request):
    categories = Category.objects.filter(parent__isnull=True)
    special_offers = Product.objects.filter(is_special_offer=True, available=True)
    banners = Banner.objects.filter(is_active=True)
    promotions = Promotion.objects.all()
    all_products = Product.objects.filter(available=True)
    
    # Get subscribed products for authenticated users
    subscribed_products = []
    if request.user.is_authenticated:
        subscribed_products = Product.objects.filter(subscriptions__user=request.user)
    
    return render(request, 'store/home.html', {
        'special_offers': special_offers,
        'categories': categories,
        'banners': banners,
        'promotions': promotions,
        'all_products': all_products,
        'subscribed_products': subscribed_products,
    })

