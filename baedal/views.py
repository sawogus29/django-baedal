from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'baedal/index.html', {})

def customer_signin(request):
    return render(request, 'baedal/customer_signin.html', {})

def customer_signup(request):
    return render(request, 'baedal/customer_signup.html', {})