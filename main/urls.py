from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),  # Bosh sahifa
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('store/', views.store, name='store'),
    path('subscribe/', views.phone_subscribe, name='phone_subscribe'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/increase/<int:product_id>/', views.increase_quantity, name='increase_quantity'),
    path('cart/decrease/<int:product_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('checkout/', views.checkout_view, name='checkout'),
]