from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
import stripe.error
from restaurants.api.permissions import IsOwnerOrIsEmployee

from restaurants.models import *
from restaurants.api.serializers import OrderSerializer, OrderItemSerializer, StripePaymentSerializer

from datetime import datetime

import stripe


# get order of a user
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_my_orders(request):
    user = request.user
    orders = user.order.all()
    serializer = OrderSerializer(orders, many=True)

    return Response(serializer.data)


# getting orders of a restaurant
@api_view(['GET'])
@permission_classes([IsOwnerOrIsEmployee])
def get_restaurants_order(request, id):
    orders = Order.objects.filter(restaurant=id)
    serializer = OrderSerializer(orders, many=True)

    return Response(serializer.data)


# getting order by id
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_orders_by_id(request, id):
    order = Order.objects.get(pk=id)
    serializer = OrderSerializer(order)

    return Response(serializer.data)


# add order view
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_order(request):
    user = request.user
    data = request.data
    restaurant = data['restaurant']
    total_price = data['totalPrice']
    delivery_address = data['deliveryAddress']
    order_items = data['orderItems']
    restaurant_data = Restaurant.objects.get(pk=restaurant.id)

    order = Order.objects.create(
        user=user,
        restaurant=restaurant_data,
        total_price=total_price,
        delivery_address=delivery_address,
    )

    for order_item in order_items:
        # getting informations for the orderitem create
        food_item = FoodItem.objects.get(pk=order_item.id)
        menu = Menu.objects.get(pk=food_item.menu)
        category = Category.objects.get(pk=menu.category)

        created_order_item = OrderItems.objects.create(
            order=order,
            category=category,
            menu=menu,
            food_item=food_item,
        )

    serializer = OrderSerializer(order)
    return Response(serializer.data)


# order delete view
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_order(request, id):
    order = Order.objects.get(pk=id)

    if order != None:
        order.delete()
        return Response('Order deleted successfully')

    return Response('Can not found order to delete', status=status.HTTP_404_NOT_FOUND)


# stripe payment view
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def make_stripe_payment(request):
    serializer = StripePaymentSerializer(data=request.data)

    if serializer.is_valid():
        try:
            # creating token for payment with card
            token = stripe.Token.create(
                card={
                    'number': serializer.validated_data['card_num'],
                    'exp_month': serializer.validated_data['exp_month'],
                    'exp_year': serializer.validated_data['exp_year'],
                    'cvc': serializer.validated_data['cvc'],
                }
            )
            # charging the card for payment
            make_charge = stripe.Charge.create(
                amount=serializer.validated_data['amount'],
                currency=serializer.validated_data['currency'],
                source=token.id,
            )

            return Response({'success': 'Payment Successful', 'charge_id': make_charge.id})

        except stripe.error.StripeError as error:
            return Response({'error': str(error)}, status=status.HTTP_400_BAD_REQUEST)


# updating order view after payment
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_order_after_payment(request, id):
    order = Order.objects.get(pk=id)
    data = request.data

    if order != None:
        order.is_paid = True
        order.payment_method = data['paymentMethod']
        order.paid_at = datetime.now()

    order.save()
    serializer = OrderSerializer(order)
    return Response(serializer.data)
