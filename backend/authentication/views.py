from django.shortcuts import render
from rest_framework.response import Response
from authentication.models import User, Profile
from authentication.serializer import UserSerializer, MyTokenObtainPairSerializer, RegisterSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import generics, status


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


@api_view(['GET'])
def get_routes(request):
    routes = [
        '/authentication/token/',
        '/authentication/register/',
        '/authentication/token/refresh/'
    ]
    return Response(routes)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def test_end_point(request):
    if request.method == 'GET':
        response = f"Hey {request.user}, you are seeing a GET response."
        return Response({'response': response}, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        text = request.POST.get('text')
        response = f"Hey {request.user}, you sent a POST request with the text: {text}"
        return Response({'response': response}, status=status.HTTP_200_OK)

    else:
        print('Invalid request')

    return Response({'response': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)


