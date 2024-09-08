from django.contrib.auth import authenticate

from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from restaurants.api.serializers import UserSeializer, UserRegistrationSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status


# user login view
@api_view(['POST'])
def user_login(request):
    username = request.data['username']
    password = request.data['password']

    user = authenticate(username=username, password=password)

    if user:
        Token.objects.get_or_create(user=user)
        serializer = UserSeializer(user)
        return Response(serializer.data)

    return Response('Invalid Credentials', status=status.HTTP_400_BAD_REQUEST)


# user registration view
@api_view(['POST'])
def user_register(request):
    serializer = UserRegistrationSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()
        Token.objects.get_or_create(user=user)

        return Response(UserSeializer(user).data)

    return Response("Can not create the User", status=status.HTTP_400_BAD_REQUEST)


# user logout view
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_logout(request):
    if request.method == 'POST':
        request.user.auth_token.delete()
        request.auth.delete()
        return Response('Logout Successfully')

    return Response("Can not Logout", status=status.HTTP_400_BAD_REQUEST)
