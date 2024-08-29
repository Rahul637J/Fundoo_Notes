
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User,Log
from .serializer import UserRegistrationSerializer, UserLoginSerializer
from django.contrib.auth import authenticate
from  rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sites.shortcuts import get_current_site
from rest_framework.reverse import reverse
from django.conf import settings
from django.core.mail import send_mail
from rest_framework.decorators import api_view
import jwt
from .task import send_email_task
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi



class RegistrationUser(APIView):
    
    @swagger_auto_schema( operation_description="An User Regsitration  API endpoint",
        request_body=UserRegistrationSerializer,
        responses={200: UserRegistrationSerializer(many=True)})
    
    def post(self,request):
        
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user=serializer.save()  
            
            token = RefreshToken.for_user(user)
            access_token = str(token.access_token)
            # # refresh_token = str(token)
            link=reverse('verify_email',args=[access_token],request=request)
            email_subject = 'Verify your email address'
            email_body = f'Use this token to verify your email: {link}'
            send_email_task.delay(email_subject,email_body,user.email)
            
            return Response({"message": "User created successfully", "status": "Success","data":serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
       
class LoginUser(APIView):
    
    @swagger_auto_schema( operation_description="An User Login  API endpoint",
        request_body=UserLoginSerializer,
        responses={200: UserLoginSerializer(many=True)})
    
    def post(self,request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
            
        token = RefreshToken.for_user(serializer.instance)
        
        return Response({"Message": "Login successful", "status": "Success","data":{'refresh':str(token),'access':str(token.access_token)}},status=status.HTTP_200_OK)
   
    
@api_view(["GET"])
def verify_email(request,token):
    try:
        
        payload=jwt.decode(token,settings.SECRET_KEY,algorithms=["HS256"])
        user = User.objects.get(id=payload['user_id'])
        user.is_verified = True
        user.save()

        return Response({"Message": "User email verified successfully"}, status=200)
    except Exception as e:
        return Response({"Message": "Invalid token or user not found", "Error": str(e)}, status=400)
    
        
        
       
        
