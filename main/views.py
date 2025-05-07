from django.shortcuts import render, redirect,get_object_or_404
from .forms import PhoneSubscriptionForm
from .models import Product, Category, Brand,PhoneSubscription,Order, OrderItem
from django.db.models import Avg,Q
from django.core.paginator import Paginator

def product_list(request):
    #products = Product.objects.all()
    categories = Category.objects.all()
    brands = Brand.objects.all()
    products = Product.objects.filter(new=True)
    top_products = Product.objects.filter(top_seller=True)
    return render(request, 'index.html', {
        'products': products,
        'products': products,
        'categories': categories,
        'brands': brands,
        'top_products': top_products,
    })


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    images = product.images.all()
    reviews = product.reviews.all()
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0

    # Related products (same category, excluding current product)
    related_products = Product.objects.filter(category=product.category).exclude(pk=product.pk)[:4]
    categories = Category.objects.all()

    context = {
        'product': product,
        'images': images,
        'reviews': reviews,
        'average_rating': round(average_rating, 1),
        'related_products': related_products,
        'categories': categories,
    }
    return render(request, 'product_detail.html', context)


def store(request):
    selected_categories = request.GET.getlist('category')
    search_query = request.GET.get('q', '')  # Qidiruv so‘rovi
    sort = request.GET.get('sort')
    show = int(request.GET.get('show', 20))  # Nechta mahsulot ko‘rsatilsin

    products = Product.objects.all()

    # Kategoriya bo‘yicha filter
    if selected_categories:
        products = products.filter(category__id__in=selected_categories)

    # Qidiruv bo‘yicha filter
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    # Saralash
    if sort == 'new':
        products = products.order_by('-new')
    elif sort == 'top':
        products = products.order_by('-top_seller')

    # Paginator
    paginator = Paginator(products, show)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()

    return render(request, 'store.html', {
        'products': page_obj,
        'categories': categories,
        'selected_categories': selected_categories,
        'request': request,
        'search_query': search_query,
    })



def phone_subscribe(request):
    if request.method == 'POST':
        form = PhoneSubscriptionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')  # kerakli sahifaga yo‘naltiring
    return redirect('product_list')


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        cart[str(product_id)]['quantity'] += 1
    else:
        cart[str(product_id)] = {
            'name': product.name,
            'price': float(product.price),
            'quantity': 1,
        }

    request.session['cart'] = cart
    return redirect('checkout')  # Yoki 'product_list' sahifasiga

def checkout_view(request):
    cart = request.session.get('cart', {})
    total = sum(item['price'] * item['quantity'] for item in cart.values())
    categories = Category.objects.all()

    if request.method == 'POST':
        first_name = request.POST.get('first-name')
        last_name = request.POST.get('last-name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        city = request.POST.get('city')
        tel = request.POST.get('tel')

        order = Order.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            address=address,
            city=city,
            tel=tel,
        )

        for item in cart.values():
            OrderItem.objects.create(
                order=order,
                product_name=item['name'],
                quantity=item['quantity'],
                price=item['price'],
            )

        # Savatni tozalash
        request.session['cart'] = {}

        return redirect('checkout')  # yoki boshqa sahifaga

    return render(request, 'checkout.html', {'cart': cart, 'total': total, 'categories': categories})


def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    product_id = str(product_id)
    if product_id in cart:
        del cart[product_id]
        request.session['cart'] = cart
    return redirect('checkout')


# views.py

def increase_quantity(request, product_id):
    cart = request.session.get('cart', {})
    product_id = str(product_id)
    if product_id in cart:
        cart[product_id]['quantity'] += 1
        request.session['cart'] = cart
    return redirect('checkout')

def decrease_quantity(request, product_id):
    cart = request.session.get('cart', {})
    product_id = str(product_id)
    if product_id in cart:
        if cart[product_id]['quantity'] > 1:
            cart[product_id]['quantity'] -= 1
        else:
            del cart[product_id]  # Agar 1 tadan kam bo‘lsa — o‘chirilsin
        request.session['cart'] = cart
    return redirect('checkout')
