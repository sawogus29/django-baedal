from django.urls import path

from . import views

app_name = 'baedal' # namespace
urlpatterns = [
  path('', views.index, name = 'index'),
  # common
  path('signout', views.signout, name='singout'),
  
  # customer
  path('customer/signin', views.customer_signin, name='customer_signin'),
  path('customer/signup', views.customer_signup, name='customer_signup'),

  # restaurant
  path('restaurant/signin', views.restaurant_signin, name='restaurant_signin'),
  path('restaurant/signup', views.restaurant_signup, name='restaurant_signup'),
]