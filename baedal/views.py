from django.shortcuts import render
from .models import Restaurant

# Create your views here.
def index(request):
    return render(request, 'baedal/index.html', {})

# =========== Customer =====================
def customer_signin(request):
    return render(request, 'baedal/customer_signin.html', {})

def customer_signup(request):
    return render(request, 'baedal/customer_signup.html', {})
# ============================================

# =========== Restaurant =====================
def restaurant_signin(request):
    return render(request, 'baedal/restaurant_signin.html', {})

def restaurant_signup(request):
    categories = [cat for cat, _ in Restaurant.category.field.choices]
    print(categories)

    return render(request, 'baedal/restaurant_signup.html', {'categories': categories})
# ============================================