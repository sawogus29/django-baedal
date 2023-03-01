from django.urls import path

from . import views

app_name = 'baedal' # namespace
urlpatterns = [
  path('', views.index, name = 'index'),
  path('customer/signin', views.customer_signin, name='customer_signin'),
  path('customer/signup', views.customer_signup, name='customer_signup'),
]