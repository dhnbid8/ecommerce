from django.urls import include, path
from card import views

urlpatterns = [
	path('card/', views.get),
	path('item/<int:id>', views.deleteItem),
	path('item/', views.addItemToCard),
]