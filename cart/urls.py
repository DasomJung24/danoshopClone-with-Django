from django.urls import path
from .           import views

app_name='cart'

urlpatterns =[
    path('', views.CartView.as_view()),
    path('/<int:cart_id>', views.CartView.as_view()),
]