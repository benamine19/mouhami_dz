from rest_framework import serializers
from .models import User,Admin,Avocat,Client
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import authenticate
from google.auth.transport import requests
from google.oauth2 import id_token
from .models import User
from django.contrib.auth import authenticate
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed
from django.views.decorators.csrf import ensure_csrf_cookie
import datetime
import jwt
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email','first_name','is_admin','is_avocat','is_client')



class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = ('area', 'phone_number', 'address')
class AdminRegistrationSerializer(serializers.ModelSerializer):  
    password1 = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    admin_data = AdminSerializer(required=False)
    class Meta:
        model = User
        fields = ('username','first_name','last_name','email', 'password1','password2','admin_data')
        extra_kwargs = {'password1': {'write_only': True}}
    def validate(self, data):
        password1 = data.get('password1')
        password2 = data.get('password2')

        if password1 != password2:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        username = validated_data.pop('username')
        first_name = validated_data.pop('first_name')
        last_name = validated_data.pop('last_name')
        email= validated_data.pop('email')
        password = validated_data.pop('password1')
        profile_data = validated_data.pop('admin_data')
        user = User.objects.create(username=username,first_name=first_name,last_name=last_name,email=email,password=password,is_admin=True,auth_provider='gmail')
        user.save()
        Ad=Admin.objects.create(
            admin=user,
            address=profile_data['address'],
            phone_number=profile_data['phone_number'],
            area=profile_data['area'],
        )
        return Ad




class AvocatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avocat
        fields = ('specialty', 'address', 'phone_number', 'skills', 'experiences', 'domaines_pratique', 'adresse_cabinet_avocats')

class AvocatRegistrationSerializer(serializers.ModelSerializer):  
    password1 = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    Avocat_data = AvocatSerializer(required=False)
    class Meta:
        model = User
        fields = ('username','first_name','last_name','email', 'password1','password2','Avocat_data')
        extra_kwargs = {'password1': {'write_only': True}}
    def validate(self, data):
        password1 = data.get('password1')
        password2 = data.get('password2')
        if password1 != password2:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        username = validated_data.pop('username')
        first_name = validated_data.pop('first_name')
        last_name = validated_data.pop('last_name')
        email= validated_data.pop('email')
        password = validated_data.pop('password1')
        profile_data = validated_data.pop('Avocat_data')
        user = User.objects.create(username=username,first_name=first_name,last_name=last_name,email=email,password=password,is_avocat=True,auth_provider='gmail',is_active=False)
        user.save()
        Av=Avocat.objects.create(
            avocat=user,
            address=profile_data['address'],
            phone_number=profile_data['phone_number'],
            specialty=profile_data['specialty'],
            skills=profile_data['skills'],
            experiences=profile_data['experiences'],
            domaines_pratique=profile_data['domaines_pratique'],
            adresse_cabinet_avocats=profile_data['adresse_cabinet_avocats'],
        )
        return Av




class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('address', 'phone_number')


class ClientRegistrationSerializer(serializers.ModelSerializer):  
    password1 = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    Client_data = ClientSerializer(required=False)
    class Meta:
        model = User
        fields = ('username','first_name','last_name','email', 'password1','password2','Client_data')
        extra_kwargs = {'password1': {'write_only': True}}
    def validate(self, data):
        password1 = data.get('password1')
        password2 = data.get('password2')

        if password1 != password2:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        username = validated_data.pop('username')
        first_name = validated_data.pop('first_name')
        last_name = validated_data.pop('last_name')
        email= validated_data.pop('email')
        password = validated_data.pop('password1')
        profile_data = validated_data.pop('Client_data')
        user = User.objects.create(username=username,first_name=first_name,last_name=last_name,email=email,password=password,is_client=True,is_active=True,auth_provider='gmail')
        user.save()
        cl=Client.objects.create(
            client=user,
            address=profile_data['address'],
            phone_number=profile_data['phone_number'],
        )
        return cl






def generate_access_token(user):
    access_token_payload = {
        'user_id': user.id,
        'is_admin':user.is_admin,
        'is_avocat':user.is_avocat,
        'is_client':user.is_client,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=5),
        'iat': datetime.datetime.utcnow(),
    }
    access_token = jwt.encode(access_token_payload,settings.SECRET_KEY, algorithm='HS256')
    return access_token
def generate_refresh_token(user):
    refresh_token_payload = {
        'user_id': user.id,
        'username': user.username,
        'is_admin':user.is_admin,
        'is_avocat':user.is_avocat,
        'is_client':user.is_client,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
        'iat': datetime.datetime.utcnow()
    }
    refresh_token = jwt.encode(
        refresh_token_payload, settings.SECRET_KEY, algorithm='HS256')
    return refresh_token






# class google():
class Google():
    @staticmethod
    def validate(access_token):
        try:
            id_info = id_token.verify_oauth2_token(access_token, requests.Request())
            print('id_info : ',id_info)
            if 'accounts.google.com' in id_info['iss']:
                return id_info
                
        except Exception as error:
            return 'token is invalid or has expired'


def login_user_social(email ,password):
    if (email is None) or (password is None):
        raise exceptions.AuthenticationFailed(
            'username and password required')
    user = User.objects.filter(email=email).first()
    if(user is None):
        raise exceptions.AuthenticationFailed('user not found')
    if (not user.password == password ):
        raise exceptions.AuthenticationFailed('wrong password')
    serialized_user = UserSerializer(user).data
    access_token = generate_access_token(user)
    refresh_token = generate_refresh_token(user)
    return {
        'access_tokeen':str( access_token),
        'refresh_token': str(refresh_token),
        'user': serialized_user,
    }





def register_social_user(provider ,username,email,first_name,last_name):
    user=User.objects.filter(email=email)
    if user.exists() :
        if provider == user[0].auth_provider:
            return login_user_social(email,settings.SOCIAL_AUTH_PASSWORD)
        else :
            raise AuthenticationFailed(
                detail=f"please continue your login with {user[0].auth_provider}"
            )  
    else :
        register_user=User.objects.create(username=username,first_name=first_name,last_name=last_name,email=email,password=settings.SOCIAL_AUTH_PASSWORD,auth_provider=provider)
        register_user.save()
        result=login_user_social(register_user.email,settings.SOCIAL_AUTH_PASSWORD)
        return result




class GoogleSigninSerializer(serializers.Serializer):
    access_token=serializers.CharField(min_length=6)
    def validate_access_token(self,access_token):
        google_user=Google.validate(access_token)
        print('google user',google_user)
        try:
            user_id=google_user["sub"]
            print('user_id',user_id)
        except Exception as error:
            raise serializers.ValidationError('this token is invalid or expire ')
        if google_user['aud'] != settings.GOOGLE_CLIENT_ID :
            raise AuthenticationFailed(detail="could not verify_user")  
        else:
            email=google_user['email']
            username=google_user['name']
            last_name=google_user['family_name']
            provider='google'
            first_name=google_user['given_name']
            return register_social_user(provider,username,email,first_name,last_name)





# class Avocatcompleteserialzers(CreateAPIView):
