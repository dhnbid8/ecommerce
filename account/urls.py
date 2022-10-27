from django.urls import include, path
from account import views

urlpatterns = [
    path('likes/', views.likesProducts().as_view()),
    path('likes/<int:id>', views.delete, name='deletelike'),
    path('profile/', views.ProfileViwe().as_view()),

]