from django.contrib import admin
from .models import Product, ProductImage, ProductReview, Brand, Category, PhoneSubscription, Order, OrderItem

admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(ProductReview)
admin.site.register(Brand)
admin.site.register(Category)

@admin.register(PhoneSubscription)
class PhoneSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'subscribed_at')


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'tel', 'created_at')
    inlines = [OrderItemInline]

admin.site.register(Order, OrderAdmin)