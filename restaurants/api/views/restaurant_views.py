from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from restaurants.models import Restaurant, Category, Menu, FoodItem, User, Employee, Modifier
from restaurants.api.serializers import (
    RestaurantSerializer,
    CategorySerializer,
    MenuSerializer,
    FoodItemSerializer,
    EmployeeSerializer,
    ModifierSerializer,
)
from restaurants.api.permissions import IsOwner, IsOwnerOrIsEmployee


# getting all restaurants view
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_restuarants(request):
    restaurants = Restaurant.objects.all()
    serializer = RestaurantSerializer(restaurants, many=True)

    return Response(serializer.data)


# create restaurant view
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_restaurants(request):
    data = request.data
    user = User.objects.get(pk=request.user.id)

    if data != None:
        user.is_owner = True
        restaurant = Restaurant.objects.create(
            owner=user,
            name=data['name'],
            location=data['location'],
        )
        user.save()
        serializer = RestaurantSerializer(restaurant)

        return Response(serializer.data)

    return Response('Can not create Restaurant', status=status.HTTP_400_BAD_REQUEST)


# restaurant edit view
@api_view(['PUT'])
@permission_classes([IsOwner])
def edit_restaurant(request, id):
    restaurant = Restaurant.objects.get(pk=id)
    data = request.data

    if not restaurant:
        return Response('No item found to edit', status=status.HTTP_404_NOT_FOUND)

    if data['name'] != '':
        restaurant.name = data['name']
    if data['location'] != '':
        restaurant.location = data['location']

    restaurant.save()
    serializer = RestaurantSerializer(restaurant)
    return Response(serializer.data)


# restaurant delete view
@api_view(['DELETE'])
@permission_classes([IsOwner])
def delete_restaurant(request, id):
    restaurant = Restaurant.objects.get(pk=id)

    if restaurant != None:
        restaurant.delete()
        return Response('Deleted Restaurant Successfully')

    return Response('Can not delete Restaurant', status=status.HTTP_400_BAD_REQUEST)


# getting employees of a restaurant
@api_view(['GET'])
@permission_classes([IsOwnerOrIsEmployee])
def get_all_empolyee_of_restaurant(request, id):
    employees = Employee.objects.filter(restaurant=id)
    serializer = EmployeeSerializer(employees, many=True)

    return Response(serializer.data)


# employee adding view
@api_view(['POST'])
@permission_classes([IsOwner])
def add_empolyee(request, id):
    data = request.data

    # getting restaurant info
    restaurant = Restaurant.objects.get(pk=id)
    # getting employee info
    employee_data = User.objects.get(username=data['username'])

    if restaurant != None and employee_data != None:
        employee_data.is_employee = True
        created_employee = Employee.objects.create(
            employee=employee_data,
            restaurant=restaurant,
        )

        serializer = EmployeeSerializer(created_employee)
        return Response(serializer.data)

    return Response('Can not add employee', status=status.HTTP_400_BAD_REQUEST)


# employee delete view
@api_view(['DELETE'])
@permission_classes([IsOwner])
def delete_employee(request, id):
    employee = Employee.objects.get(pk=id)

    if employee != None:
        employee.delete()
        return Response('Employee removed')

    return Response('Can not remove Employee', status=status.HTTP_400_BAD_REQUEST)


# getting categories of a restaurants view
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_categories_of_restaurant(request, id):
    # restaurants and categories are connected by foreignkey
    categories = Category.objects.filter(restaurant=id)
    serializer = CategorySerializer(categories, many=True)

    return Response(serializer.data)


# adding category view
@api_view(['POST'])
@permission_classes([IsOwnerOrIsEmployee])
def add_category(request, id):
    restaurant = Restaurant.objects.get(pk=id)
    data = request.data

    if data != None or restaurant != None:
        category = Category.objects.create(
            restaurant=restaurant,
            name=data['name']
        )

        serializer = CategorySerializer(category)
        return Response(serializer.data)

    return Response('Can not create Category', status=status.HTTP_400_BAD_REQUEST)


# edit category view
@api_view(['PUT'])
@permission_classes([IsOwnerOrIsEmployee])
def edit_category(request, id):
    category = Category.objects.get(pk=id)
    data = request.data

    if not category:
        return Response('No item found to edit', status=status.HTTP_404_NOT_FOUND)

    if data['name'] != '':
        category.name = data['name']
        category.save()
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    return Response('Can not edit Category', status=status.HTTP_400_BAD_REQUEST)


# category delete view
@api_view(['DELETE'])
@permission_classes([IsOwnerOrIsEmployee])
def delete_category(request, id):
    category = Category.objects.get(pk=id)

    if category != None:
        category.delete()
        return Response('Deleted Category Successfully')

    return Response('Can not delete Category', status=status.HTTP_400_BAD_REQUEST)


# getting menus of a category view
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_menus_of_category(request, id):
    # categories and menus are connected by foreignkey
    menus = Menu.objects.filter(category=id)
    serializer = MenuSerializer(menus, many=True)

    return Response(serializer.data)


# add menu view
@api_view(['POST'])
@permission_classes([IsOwnerOrIsEmployee])
def add_menu(request, id):
    category = Category.objects.get(pk=id)
    data = request.data

    if category != None and data['name'] != '':
        menu = Menu.objects.create(
            category=category,
            name=data['name'],
        )
        serializer = MenuSerializer(menu)
        return Response(serializer.data)

    return Response('Can not create Menu', status=status.HTTP_400_BAD_REQUEST)


# menu edit view
@api_view(['PUT'])
@permission_classes([IsOwnerOrIsEmployee])
def edit_menu(request, id):
    menu = Menu.objects.get(pk=id)
    data = request.data

    if not menu:
        return Response('No item found to edit', status=status.HTTP_404_NOT_FOUND)

    if data['name'] != '':
        menu.name = data['name']
        menu.save()
        serializer = MenuSerializer(menu)
        return Response(serializer.data)

    return Response('Can not edit Menu', status=status.HTTP_400_BAD_REQUEST)


# menu delete view
@api_view(['DELETE'])
@permission_classes([IsOwnerOrIsEmployee])
def delete_menu(request, id):
    menu = Menu.objects.get(pk=id)

    if menu != None:
        menu.delete()
        return Response('Deleted Menu Successfully')

    return Response('Can not delete Menu', status=status.HTTP_400_BAD_REQUEST)


# getting fooditems of a menu view
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_fooditems_of_menu(request, id):
    # fooditem and menus are connected by foreignkey
    fooditems = FoodItem.objects.filter(menu=id)
    serializer = FoodItemSerializer(fooditems, many=True)

    return Response(serializer.data)


# getting fooditem by id view
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_fooditem_by_id(request, id):
    fooditem = FoodItem.objects.get(pk=id)
    serializer = FoodItemSerializer(fooditem)

    return Response(serializer.data)


# add fooditem view
@api_view(['POST'])
@permission_classes([IsOwnerOrIsEmployee])
def add_fooditem(request, id):
    menu = Menu.objects.get(pk=id)
    data = request.data

    if menu != None and data != None:
        fooditem = FoodItem.objects.create(
            menu=menu,
            name=data['name'],
            description=data['description'],
            price=data['price'],
        )

        serializer = FoodItemSerializer(fooditem)
        return Response(serializer.data)

    return Response('Can not create Fooditem', status=status.HTTP_400_BAD_REQUEST)


# fooditem edit view
@api_view(['PUT'])
@permission_classes([IsOwnerOrIsEmployee])
def edit_fooditem(request, id):
    fooditem = FoodItem.objects.get(pk=id)
    data = request.data

    if not fooditem:
        return Response('No item found to edit', status=status.HTTP_404_NOT_FOUND)

    if data['name'] != '':
        fooditem.name = data['name']
    if data['description'] != '':
        fooditem.description = data['description']
    if data['price'] != '':
        fooditem.price = data['price']

    fooditem.save()
    serializer = FoodItemSerializer(fooditem)
    return Response(serializer.data)


# fooditem delete view
@api_view(['DELETE'])
@permission_classes([IsOwnerOrIsEmployee])
def delete_fooditem(request, id):
    fooditem = FoodItem.objects.get(pk=id)

    if fooditem != None:
        fooditem.delete()
        return Response('Deleted Fooditem Successfully')

    return Response('Can not delete fooditem', status=status.HTTP_400_BAD_REQUEST)


# getting modifiers of a fooditem
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_modifier_of_fooditem(request, id):
    modifiers = Modifier.objects.filter(food_item=id)
    serializer = ModifierSerializer(modifiers, many=True)

    return Response(serializer.data)


# modifier add view
@api_view(['POST'])
@permission_classes([IsOwnerOrIsEmployee])
def add_modifiers(request, id):
    fooditem = FoodItem.objects.get(pk=id)
    data = request.data

    if fooditem != None and data != None:
        modifier = Modifier.objects.create(
            food_item=fooditem,
            name=data['name'],
            extra_price=data['extraPrice'],
        )

        serializer = ModifierSerializer(modifier)

        return Response(serializer.data)


# modfier edit view
@api_view(['PUT'])
@permission_classes([IsOwnerOrIsEmployee])
def edit_modifier(request, id):
    modifier = Modifier.objects.get(pk=id)
    data = request.data

    if not modifier:
        return Response('No item found to edit', status=status.HTTP_404_NOT_FOUND)

    if data['name'] != '':
        modifier.name = data['name']
    if data['extraPrice'] != '':
        modifier.extra_price = data['extraPrice']

    modifier.save()
    serializer = ModifierSerializer(modifier)
    return Response(serializer.data)


# modifier delete view
@api_view(['DELETE'])
@permission_classes([IsOwnerOrIsEmployee])
def delete_modifier(request, id):
    modifier = Modifier.objects.get(pk=id)

    if modifier != None:
        modifier.delete()
        return Response('Modifier deleted successfully')

    return Response('Can not find item to delete', status=status.HTTP_404_NOT_FOUND)
