from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password

from .models import Customer, Restaurant

# Create your views here.
def index(request):
    return render(request, 'baedal/index.html', {})

# =========== Customer =====================
def customer_signin(request):
    context = {}
    if request.method == "POST" :
        username = request.POST.get('username') 
        password = request.POST.get('password') 
        try:
            customer = Customer.objects.get(username=username)
            if not check_password(password, customer.password):
                raise Exception("Passowrd doen't not match")

            # happy path
            request.session['username'] = username
            return redirect('baedal:index')
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
# ============================================

# =========== Restaurant =====================
def restaurant_signin(request):
    return render(request, 'baedal/restaurant_signin.html', {})

def restaurant_signup(request):
    categories = [cat for cat, _ in Restaurant.category.field.choices]
    print(categories)

    return render(request, 'baedal/restaurant_signup.html', {'categories': categories})
# ============================================