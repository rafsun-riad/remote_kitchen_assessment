from django.urls import path
from restaurants.api.views import order_views as views

urlpatterns = [
    path('myorders/', views.get_my_orders, name='myorders'),

    path('restaurants/<str:id>/', views.get_restaurants_order,
         name='restaurant-order'),

    path('add/', views.add_order, name='add-order'),

    path('make-payment/', views.make_stripe_payment, name='stripe-payment'),

    path('<str:id>/success-payment/',
         views.update_order_after_payment, name='success-payment'),

    path('delete/<str:id>/', views.delete_order, name='delete-order'),

    path('<str:id>/', views.get_orders_by_id, name='order-by-id'),
]
