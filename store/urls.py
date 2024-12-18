from django.urls import path, re_path, include
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('category/<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    re_path(r'^product/(?P<product_slug>[-\w]+)/$', views.product_detail, name='product_detail'),
    path('search/', views.product_search, name='product_search'),
    path('cart/', include('cart.urls', namespace='cart')),
    path('subscribe/<int:product_id>/', views.subscribe_product, name='subscribe'),
]
