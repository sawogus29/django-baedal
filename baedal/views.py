from collections import defaultdict
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
from django.db import transaction

from .models import Customer, Restaurant, Menu, Purchase, PurchaseMenu

def signin_required(usertype):
    def real_decorator(func):
        def wrapper(request, *args, **kargs):
            try:
                if request.session['usertype'] != usertype:
                    raise Exception("usertype don't match")
            except Exception as e:
                print(e)
                return redirect(f'baedal:{usertype}_signin')

            return func(request, *args, **kargs)
        return wrapper
    return real_decorator

# Create your views here.
def index(request):
    return render(request, 'baedal/index.html', {})

# =========== Common ======================
def signout(request):
    request.session.clear()
    return redirect('baedal:index')

# =========== Customer =====================
def customer_signin(request):
    context = {}
    if request.method == "POST" :
        username = request.POST.get('username') 
        password = request.POST.get('password') 
        try:
            user = Customer.objects.get(username=username)
            if not check_password(password, user.password):
                raise Exception("Passowrd doen't not match")

            # happy path
            request.session['username'] = username
            request.session['usertype'] = 'customer'
            return redirect('baedal:customer_home')
        except Exception as e:
            print(e)
            # failure: user doesn't exist or password doesn't match
            context['error'] = "ID 혹은 PW가 잘못되었습니다"

    return render(request, 'baedal/customer_signin.html', context)

def customer_signup(request):
    context = {}
    if request.method == "POST" :
        username = request.POST.get('username') 
        # happy path
        if not Customer.objects.filter(username=username):
            # store Customer to DB
            customer = Customer(
                username=username, 
                password=make_password(request.POST.get('password')), 
                phone=request.POST.get('phone'), 
                address=request.POST.get('address'), 
            )
            customer.save()

            return redirect('baedal:customer_signin')
        
        # failure: username already exist
        context['error'] = "이미 존재하는 ID입니다"

    return render(request, 'baedal/customer_signup.html', context)

@signin_required('customer')
def customer_home(request):
    context = {}
    
    restaurants = Restaurant.objects.all()
    cat_rests = defaultdict(list)
    for rest in restaurants:
        cat_rests[rest.category].append(rest)
    context['cat_rests'] = dict(cat_rests)
    print(cat_rests)

    return render(request, 'baedal/customer_home.html', context)

@signin_required('customer')
def new_order(request, rest_name):
    context = {}
    try:
        rest = Restaurant.objects.get(username=rest_name)
        menus = Menu.objects.filter(restaurant=rest)
        context['rest_display_name'] = rest.display_name
        context['menus'] = menus

        if request.method == 'POST':
            order = {}
            for menu in menus:
                quantity = request.POST.get(f'{menu.id}_quantity')
                if not quantity:
                    continue
                quantity = int(quantity)
                if quantity <= 0:
                    raise Exception("invalid quantity")
                order[menu.id] = (menu.name, menu.price, quantity)
            
            if not order:
                raise Exception("empty order")

            total_price = sum(price*quantity for _, price, quantity in order.values())
            
            # save to DB
            customer = Customer(username=request.session['username'])
            with transaction.atomic():
                purchase = Purchase(
                    restaurant=rest, 
                    customer=customer,
                    total_price=total_price, 
                    status='대기', 
                    created_date=timezone.now()
                )
                purchase.save()
                for name, price, quantity in order.values():
                    purchaseMenu = PurchaseMenu(
                        purchase=purchase, 
                        name = name, 
                        price = price, 
                        quantity = quantity
                    )
                    purchaseMenu.save()

            return redirect('baedal:customer_home')
    except Exception as e:
        context['error'] = "주문 중 에러가 발생했습니다"
        print(e)
    
    return render(request, 'baedal/new_order.html', context)

@signin_required('customer')
def customer_orders(request):
    context = {}
    
    try:
        purchases = Purchase.objects.filter(customer=request.session['username'])
        purchases = [{'created_date': purchase.created_date, 
                      'restaurant':purchase.restaurant, 
                      'total_price': purchase.total_price,
                      'status': purchase.status,
                      'menus': PurchaseMenu.objects.filter(purchase=purchase)} 
                      for purchase in purchases]

        context['purchases'] = purchases
    except Exception as e:
        print(e)
        context['error'] = '주문내역을 불러오는 도중 에러가 발생했습니다'

    return render(request, 'baedal/customer_orders.html', context)
# ============================================

# =========== Restaurant =====================
def restaurant_signin(request):
    context = {}
    if request.method == "POST" :
        username = request.POST.get('username') 
        password = request.POST.get('password') 
        try:
            user = Restaurant.objects.get(username=username)
            if not check_password(password, user.password):
                raise Exception("Passowrd doen't not match")

            # happy path
            request.session['username'] = username
            request.session['usertype'] = 'restaurant'
            return redirect('baedal:restaurant_menus')
        except Exception as e:
            print(e)
            # failure: user doesn't exist or password doesn't match
            context['error'] = "ID 혹은 PW가 잘못되었습니다"

    return render(request, 'baedal/restaurant_signin.html', context)

def restaurant_signup(request):
    context = {}
    categories = [cat for cat, _ in Restaurant.category.field.choices]
    context['categories'] = categories

    if request.method == "POST" :
        username = request.POST.get('username') 
        # happy path
        if not Restaurant.objects.filter(username=username):
            # store Customer to DB
            customer = Restaurant(
                username=username, 
                password=make_password(request.POST.get('password')), 
                display_name=request.POST.get('display_name'), 
                category=request.POST.get('category'), 
            )
            customer.save()

            return redirect('baedal:restaurant_signin')
        
        # failure: username already exist
        context['error'] = "이미 존재하는 ID입니다"

    return render(request, 'baedal/restaurant_signup.html', context)

@signin_required('restaurant')
def restaurant_menus(request):
    context = {}
    username = request.session['username']
    
    try:
        restaurant = Restaurant.objects.get(username=username)
        menus = Menu.objects.filter(restaurant=restaurant)
        context['menus'] = menus
    except Exception as e:
        print(e)
        context['menus'] = []

    return render(request, 'baedal/restaurant_menus.html', context)

@signin_required('restaurant')
def new_menu(request):
    context = {}
    username = request.session['username']
    
    if request.method == 'POST':
        try:
            restaurant = Restaurant.objects.get(username=username)
            menu = Menu(
                restaurant=restaurant, 
                name=request.POST.get('name'), 
                price=request.POST.get('price')
            )
            menu.save()
        except Exception as e:
            print(e)
        return redirect('baedal:restaurant_menus')
    
    return render(request, 'baedal/new_menu.html', context)

@signin_required('restaurant')
def restaurant_orders(request):
    context = {}
    if request.method == 'POST':
        try:
            purchase_id = request.POST.get('purchase_id')
            purchase = Purchase.objects.get(id=purchase_id)
            purchase.status = request.POST.get('status')
            purchase.save()
        except Exception as e:
            context['error'] = "접수/반려 도중 에러가 발생 했습니다"
            print(e)
    
    try:
        purchases = Purchase.objects.filter(restaurant=request.session['username'])
        purchases = [{'id': purchase.id,
                      'created_date': purchase.created_date, 
                      'customer':purchase.customer, 
                      'total_price': purchase.total_price,
                      'status': purchase.status,
                      'menus': PurchaseMenu.objects.filter(purchase=purchase)} 
                      for purchase in purchases]

        context['purchases'] = purchases

    except Exception as e:
        print(e)
        context['error'] = "주문내역을 불러오는 도중 에러가 발생했습니다"

    return render(request, 'baedal/restaurant_orders.html', context)
# ============================================