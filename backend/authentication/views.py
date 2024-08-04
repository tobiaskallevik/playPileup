from django.shortcuts import render
from rest_framework.response import Response
from authentication.models import User, Profile
from authentication.serializer import UserSerializer, MyTokenObtainPairSerializer, RegisterSerializer, PasswordResetSerializer
from authentication.tokens import account_activation_token, password_reset_token
from rest_framework.decorators import api_view, permission_classes
from django.contrib.sites.shortcuts import get_current_site
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import generics, status
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib import messages

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
        '/authentication/token/refresh/',
        '/authentication/verify-email/',
        '/authentication/request_password_reset/',
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


# Endpoint to verify email. It sends an email to the user with a link to verify their email.
@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def verify_email(request):
    email = request.data.get('email')
    if not email:
        return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({'error': 'User with this email does not exist'}, status=status.HTTP_404_NOT_FOUND)

    current_site = get_current_site(request)
    subject = "Verify Email"
    message = render_to_string('authentication/verify_email_message.html', {
        'request': request,
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    })

    email_message = EmailMessage(
        subject, message, to=[email]
    )
    email_message.content_subtype = 'html'
    email_message.send()

    
    return Response({'response': 'Email sent'}, status=status.HTTP_200_OK)
   
    
# Endpoint to confirm email verification. It verifies the email and updates the user's email_verified field to True.
@api_view(['GET'])
@permission_classes([AllowAny])
def verify_email_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.email_verified = True
        user.save()
        return Response({'message': 'Your email has been verified.'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid token or user does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
    
    
# Endpoint to send password reset email. It sends an email to the user with a link to reset their password.
@api_view(['POST'])
def request_password_reset(request):
    email = request.data.get('email')
    if not email:
        return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({'error': 'User with this email does not exist'}, status=status.HTTP_404_NOT_FOUND)

    current_site = get_current_site(request)
    subject = "Reset password"
    message = render_to_string('authentication/password_reset_message.html', {
        'request': request,
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': password_reset_token.make_token(user),
    })

    email_message = EmailMessage(
        subject, message, to=[email]
    )
    email_message.content_subtype = 'html'
    email_message.extra_headers = {'X-Content-Type-Options': 'nosniff'}
    email_message.send()

    
    return Response({'response': 'Email sent'}, status=status.HTTP_200_OK)


# Endpoint to reset password given a valid token.
@api_view(['POST'])
@permission_classes([AllowAny])
def password_reset(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and password_reset_token.check_token(user, token):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            user.set_password(serializer.validated_data['password1'])
            user.save()
            return Response({'response': 'Password has been reset'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)