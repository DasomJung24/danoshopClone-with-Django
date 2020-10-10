from django.urls import path
from .           import views

app_name = 'review'

urlpatterns = [
    path('', views.ReviewView.as_view()),
    path('/<int:review_id>', views.ReviewView.as_view()),
    path('/detail/<int:review_id>', views.ReviewDetailView.as_view()),
]