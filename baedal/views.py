from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password

from .models import Customer, Restaurant

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
    return render(request, 'baedal/customer_home.html', context)
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
            return redirect('baedal:index')
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
# ============================================