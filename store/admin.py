from django.contrib import admin
from .models import Product, Category, Manufacturer, Banner, Promotion, Review, Subscription
from .models import Banner, Promotion

admin.site.register(Banner)
admin.site.register(Promotion)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created')
    search_fields = ('product__name', 'user__username')

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'created')
    search_fields = ('user__username', 'product__name')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('parent',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'discount', 'get_discounted_price', 'available', 'category', 'is_special_offer', 'manufacturer')
    list_filter = ('available', 'category', 'is_special_offer', 'manufacturer')
    list_editable = ('price', 'discount', 'available', 'is_special_offer')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

