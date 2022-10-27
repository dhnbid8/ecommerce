from django.urls import path
from .views import go_to_gateway_view, callback_gateway_view
urlpatterns = [
    path('checkout/', go_to_gateway_view),
    path('callback-gateway/', callback_gateway_view, name="callback-gateway")
]