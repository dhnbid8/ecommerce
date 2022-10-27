from django.urls import include, path
from product import views

urlpatterns = [
    path('lastes-products/', views.LastesProductsList.as_view()),
    path('p/<slug:product_slug>/', views.ProductDetail().as_view()),
    path('p/search', views.search),
    path('c/<slug:category_slug>/', views.CategoryDatail().as_view())
]