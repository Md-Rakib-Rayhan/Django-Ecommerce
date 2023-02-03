from django.shortcuts import render, redirect
from django.views import View
from .models import Customer, Product, Cart, OrderPlaced
from .forms import CustomerRegistrationForm, CustomerProfileform
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required # for fun
from django.utils.decorators import method_decorator #for cls

# def home(request):
#  return render(request, 'app/home.html')

class ProductView(View):
    def get(self, request):
        topwears = Product.objects.filter(category='TW')
        bottomwears = Product.objects.filter(category='BW')
        mobiles = Product.objects.filter(category='M')
        return render(request, 'app/home.html', {'topwears':topwears, 'bottomwears': bottomwears, 'mobiles':mobiles})
        

# def product_detail(request):
#  return render(request, 'app/productdetail.html')
class ProductDetailView(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        item_already_in_cart = False
        if request.user.is_authenticated:
            item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists
        return render(request, 'app/productdetail.html', {'product':product, 'item_already_in_cart': item_already_in_cart})

@login_required
def add_to_cart(request):
 user = request.user
 product_id = request.GET.get('prod_id')
 product = Product.objects.get(id=product_id)
 Cart(user=user, product=product).save()
 return redirect('/cart')

@login_required
def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 0.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user==user]
                    #        -- all data aitate asbe
                    #                                 -- aitate condition check korbe ai user er data kina
                    #  -- then aitate last result / cart_product a final result asbe 
                # list comprehension python if else
        # print(cart) it's return query set
        # print(cart_product) it's return list
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount += tempamount
            shipping_amount = 70.0
            total_amount = amount + shipping_amount
        return render(request, 'app/addtocart.html', {'carts': cart, 'totalamount': total_amount, 'amount': amount, 'shipping': shipping_amount})

@login_required 
def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        # c = Cart.objects.filter(user=request.user).filter(product=prod_id) aita hobe nah bcuz aita quary set return kore
        c.quantity+=1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user==request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
        total_amount = amount + shipping_amount
        data = {
            'quantity' : c.quantity,
            'amount' : amount,
            'totalamount' : total_amount
        }
        return JsonResponse(data)
@login_required
def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user==request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
        total_amount = amount + shipping_amount
        data = {
            'quantity' : c.quantity,
            'amount' : amount,
            'totalamount' : total_amount
        }
        return JsonResponse(data)

@login_required
def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount = 0.0
        shipping_amount = 70.0
        c_num = 0
        cart_product = [p for p in Cart.objects.all() if p.user==request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
            c_num += 1
        total_amount = amount + shipping_amount
        data = {
            'amount' : amount,
            'totalamount' : total_amount,
            'c_num' : c_num
        }
        return JsonResponse(data)

@login_required
def cart_status(request):
    if request.method == 'GET':
        c_num = 0
        cart_product = [p for p in Cart.objects.all() if p.user==request.user]
        for p in cart_product:
            c_num += 1
        # print("helllo vaiiiiii",c_num)
        data = {
            'c_num' : c_num
        }
        return JsonResponse(data)

@login_required
def buy_now(request, data):
 cart = Cart.objects.filter(product=data).filter(user=request.user)
 if cart:
    return redirect('/checkout')
 else:
     product = Product.objects.get(id=data)
     Cart(user=request.user, product=product).save()
     return redirect('/checkout')

@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        form = CustomerProfileform()
        return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary'})
    def post(self, request):
        form = CustomerProfileform(request.POST)
        if form.is_valid():
            # form.save() same
            usr = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=usr, name=name, locality=locality, city=city, state =state, zipcode=zipcode)
            reg.save()
            messages.success(request, 'Congratulation!! Profile Updateed Successfully')
        form = CustomerProfileform()
        return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary'})

@login_required
def address(request):
 add = Customer.objects.filter(user=request.user)
 return render(request, 'app/address.html', {'add': add, 'active':'btn-primary'})

@login_required
def orders(request):
 op = OrderPlaced.objects.filter(user=request.user)
 return render(request, 'app/orders.html', {'order_placced': op})


# def mobile(request, data=None):
#  if data == None:
#     mobiles = Product.objects.filter(category='M')
#  elif data == 'Xiaomi' or data == 'Samsung' or data == 'Nothing' or data == 'Oppo' or data == 'Vivo' or data == 'Infinix':
#     mobiles = Product.objects.filter(category='M').filter(brand=data)
#  elif data == 'Below':
#     mobiles = Product.objects.filter(category='M').filter(discounted_price__lt=10000)
#  elif data == 'Above':
#     mobiles = Product.objects.filter(category='M').filter(discounted_price__gt=10000)
#  return render(request, 'app/mobile.html', {'mobiles':mobiles})
def mobile(request, data=None):
 product = 'M'
 if data == 'Xiaomi' or data == 'Samsung' or data == 'Nothing' or data == 'Oppo' or data == 'Vivo' or data == 'Infinix':
    products = Product.objects.filter(category='M').filter(brand=data)
 else:
    products = repeate(data, product)
 return render(request, 'app/filter.html', {'products':products, 'p':product})

def TopWear(request, data=None):
 product = 'TW'
 if data == 'adidas' or data == 'OP' or data == 'nick':
    products = Product.objects.filter(category='TW').filter(brand=data)
 else:
    products = repeate(data, product)
 return render(request, 'app/filter.html', {'products':products, 'p':product})

def BottomWear(request, data=None):
 product = 'BW'
 if data == 'adidas' or data == 'longi':
    products = Product.objects.filter(category='BW').filter(brand=data)
 else:
    products = repeate(data, product)
 return render(request, 'app/filter.html', {'products':products, 'p':product})
def Laptop(request, data=None):
 product = 'L'
 if data == 'Asos' or data == 'Hp':
    products = Product.objects.filter(category='L').filter(brand=data)
 else:
    products = repeate(data, product)
 return render(request, 'app/filter.html', {'products':products, 'p':product})

def repeate(data,product):
 if data == None:
    products = Product.objects.filter(category=product)
 elif data == 'Below':
    products = Product.objects.filter(category=product).filter(discounted_price__lt=10000)
 elif data == 'Above':
    products = Product.objects.filter(category=product).filter(discounted_price__gt=10000)
 return products

# def login(request):
#  return render(request, 'app/login.html')
# aitar kaj urls a kora hoise

# def customerregistration(request):
#  return render(request, 'app/customerregistration.html')

class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', {'form': form})
    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Congratulations! Registered Successfully')
            form.save()
            form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', {'form': form})

@login_required
def checkout(request):
 user = request.user
 add = Customer.objects.filter(user=user)
 cart_item = Cart.objects.filter(user=user)
 amount = 0.0
 shipping_amount = 70.0
 cart_product = [p for p in Cart.objects.all() if p.user==request.user]
 if cart_product:
    for p in cart_product:
        tempamount = (p.quantity * p.product.discounted_price)
        amount += tempamount
    total_amount = amount + shipping_amount
    return render(request, 'app/checkout.html', {'add': add, 'totalamount': total_amount,'cart_item':cart_item})
 else:
    return render(request, 'app/addtocart.html', {'amount':amount, 'shipping':'0.0', 'totalamount':'0.0' })


@login_required
def payment_done(request):
    user = request.user
    custid = request.GET.get('custid') 
    customer = Customer.objects.get(id = custid) #address
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
        c.delete()
    return redirect("orders")


def search(request):
    userenter = request.GET.get('search')
    result = Product.objects.filter(title__contains=userenter)

    return render(request, 'app/search.html', {'getproduct':result})

