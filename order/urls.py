from django.urls import include, path
from order import views

urlpatterns = [
    path('chekout/', views.checkout)
]