from django.urls import path
from restaurants.api.views import user_views as views

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('logout/', views.user_logout, name='logout'),

]
# path('all/', views.get_user),
