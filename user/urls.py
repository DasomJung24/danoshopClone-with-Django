from django.urls import path
from .           import views

app_name = 'user'
urlpatterns = [
    path('/signup', views.SignUpView.as_view(), name='signup'),
    path('/signin', views.SignInView.as_view(), name='signin'), 
]