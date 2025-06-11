from django.shortcuts import render, redirect, get_object_or_404
from .models import Brand, Product, CartItem,Sale,SaleItem,Cart
from .forms import BrandForm, ProductForm
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseForbidden
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages

@login_required
def home(request):
    brands = Brand.objects.all()
    return render(request, 'shop/home.html', {'brands': brands})

@login_required
def add_brand(request):
    if request.method == 'POST':
        form = BrandForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = BrandForm()
    return render(request, 'shop/add_brand.html', {'form': form})

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ProductForm()
    return render(request, 'shop/add_product.html', {'form': form})


@login_required
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        product.buying_price = request.POST.get('buying_price')
        product.selling_price = request.POST.get('selling_price')
        product.save()
        return redirect('brand_detail', brand_id=product.brand.id)

    return render(request, 'shop/edit_product.html', {'product': product})


@login_required
def brand_detail(request, brand_id):
    brand = get_object_or_404(Brand, id=brand_id)
    query = request.GET.get('q', '')
    
    if query:
        products = Product.objects.filter(brand=brand, name__icontains=query)
    else:
        products = Product.objects.filter(brand=brand)

    return render(request, 'shop/brand_detail.html', {
        'brand': brand,
        'products': products,
        'query': query,
    })


@csrf_exempt
def cart_view(request):
    if request.method == 'POST':
        if request.POST.get('clear') == 'true':
            CartItem.objects.all().delete()
            return redirect('cart')

        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        discount = float(request.POST.get('discount', 0.0))

        product = get_object_or_404(Product, id=product_id)
        CartItem.objects.create(product=product, quantity=quantity, discount=discount)

        return redirect('cart')

    cart_items = CartItem.objects.all()
    subtotal = sum(item.total_price() for item in cart_items)
    return render(request, 'shop/cart.html', {'cart_items': cart_items, 'subtotal': subtotal})

@login_required
def print_bill(request):
    cart_items = Cart.objects.filter(user=request.user)
    subtotal = sum(item.total_price for item in cart_items)

    sale = Sale.objects.create()
    for item in cart_items:
        SaleItem.objects.create(
            sale=sale,
            product=item.product,
            quantity=item.quantity,
            discount=item.discount
        )

    cart_items.delete()

    return render(request, 'shop/print_bill.html', {
        'cart_items': sale.items.all(),
        'subtotal': sale.total_amount(),  
        'now': sale.date
    })



@login_required
def sales_history(request):
    sales = Sale.objects.order_by('-date')
    return render(request, 'shop/sales_history.html', {'sales': sales})



def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Auto-login after registration
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'shop/register.html', {'form': form})


@login_required
def add_to_cart(request):
    if request.method == "POST":
        user = request.user
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        discount = float(request.POST.get('discount', 0.0))

        product = get_object_or_404(Product, id=product_id)

        cart_item, created = Cart.objects.get_or_create(user=user, product=product)

        if not created:
            cart_item.quantity += quantity
            cart_item.discount = discount  # ✅ important: update discount if changed
        else:
            cart_item.quantity = quantity
            cart_item.discount = discount

        cart_item.save()

        messages.success(request, f"{product.name} added to cart!")
    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required
def showcart(request):
    user = request.user

    if request.method == 'POST' and request.POST.get('clear') == 'true':
        Cart.objects.filter(user=user).delete()

    cart_items = Cart.objects.filter(user=user)
    subtotal = sum(item.total_price for item in cart_items)

    return render(request, 'shop/cart.html', {
        'cart_items': cart_items,
        'subtotal': subtotal,
    })

