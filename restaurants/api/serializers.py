from rest_framework import serializers
from restaurants.models import *


# all necessary serializers for the models
class UserSeializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'email',
                  'is_owner', 'is_employee', 'auth_token',]


class UserRegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'password', 'email']
        # for security
        extra_kwargs = {
            'password': {'write_only': True}
        }

    # this method creates user after validating incoming data
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
        )
        return user


class RestaurantSerializer(serializers.ModelSerializer):

    class Meta:
        model = Restaurant
        fields = '__all__'


class EmployeeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employee
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class MenuSerializer(serializers.ModelSerializer):

    class Meta:
        model = Menu
        fields = '__all__'


class ModifierSerializer(serializers.ModelSerializer):

    class Meta:
        model = Modifier
        fields = '__all__'


class FoodItemSerializer(serializers.ModelSerializer):
    modifier = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = FoodItem
        fields = '__all__'

    def get_modifier(self, obj):
        modifiers = obj.modifier.all()
        serializer = ModifierSerializer(modifiers, many=True)
        return serializer.data


class OrderSerializer(serializers.ModelSerializer):
    user = UserSeializer()
    restaurant = RestaurantSerializer()
    order_items = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = '__all__'

    def get_order_items(self, obj):
        order_items = obj.order_items.all()
        serializer = OrderItemSerializer(order_items, many=True)
        return serializer.data


class OrderItemSerializer(serializers.ModelSerializer):

    category = CategorySerializer(many=True)
    menu = MenuSerializer(many=True)
    food_item = FoodItemSerializer(many=True)

    class Meta:
        model = OrderItems
        fields = '__all__'


class StripePaymentSerializer(serializers.Serializer):
    amount = serializers.IntegerField()
    currency = serializers.CharField(max_length=3)
    card_num = serializers.CharField(max_length=16)
    exp_month = serializers.IntegerField()
    exp_year = serializers.IntegerField()
    cvc = serializers.CharField(max_length=4)
