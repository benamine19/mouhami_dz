from django.shortcuts import render
from .serializers import GoogleSigninSerializer,ClientRegistrationSerializer,AdminRegistrationSerializer,AvocatRegistrationSerializer,ClientSerializer,UserSerializer
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import authenticate
from .models import User,Avocat,Client,Admin,Rendez_vous
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse
from rendez_vous.serializers import Rendez_vous_Serializer,Commentaire_Serializer
from django.shortcuts import get_object_or_404
import datetime
import jwt
from django.conf import settings
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import exceptions
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from .permissions import Is_Client,Is_Avocat,Is_Admin
from rest_framework import generics,status
from rest_framework.generics import GenericAPIView
from .serializers import generate_refresh_token,generate_access_token,AvocatSerializer,ClientSerializer,AdminSerializer

class ClientRegistrationView(CreateAPIView):
    serializer_class = ClientRegistrationSerializer
    permission_classes = (AllowAny,)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = {
            'success' : 'True',
            'status code' : status.HTTP_200_OK,
            'message': 'client registered  successfully',
            }
        status_code = status.HTTP_200_OK
        return Response(response, status=status_code)


class AdminRegistrationView(CreateAPIView):
    serializer_class = AdminRegistrationSerializer
    permission_classes = (AllowAny,)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = {
            'success' : 'True',
            'status code' : status.HTTP_200_OK,
            'message': 'client registered  successfully',
            }
        status_code = status.HTTP_200_OK
        return Response(response, status=status_code)

class AvocatRegistrationView(CreateAPIView):
    serializer_class = AvocatRegistrationSerializer
    permission_classes = (AllowAny,)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = {
            'success' : 'True',
            'status code' : status.HTTP_200_OK,
            'message': 'client registered  successfully',
            }
        status_code = status.HTTP_200_OK
        return Response(response, status=status_code)


@api_view(['POST'])
@permission_classes([AllowAny])
@ensure_csrf_cookie
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    response = Response()
    if (username is None) or (password is None):
        raise exceptions.AuthenticationFailed(
            'username and password required')

    user = User.objects.filter(email=username).first()
    if(user is None):
        raise exceptions.AuthenticationFailed('user not found')
    if (not user.password == password ):
        raise exceptions.AuthenticationFailed('wrong password')
    serialized_user = UserSerializer(user).data
    access_token = generate_access_token(user)
    refresh_token = generate_refresh_token(user)
    data  = {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": serialized_user,
    }
    return Response(data, status=status.HTTP_200_OK)






class UsersList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated ,Is_Admin]
    queryset = User.objects.all()
    serializer_class = UserSerializer




class GoogleSigninview(GenericAPIView):
    serializer_class = GoogleSigninSerializer
    def post(self,request):
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid()
        data=((serializer.validated_data)['access_token'])
        return Response(data ,status=status.HTTP_200_OK)
    

# class AvocatcompleteRegistrationView(CreateAPIView):
#     serializer_class = AvocatRegistrationSerializer
#     permission_classes = (Is_Avocat,)
#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         response = {
#             'success' : 'True',
#             'status code' : status.HTTP_200_OK,
#             'message': 'client registered  successfully',
#             }
#         status_code = status.HTTP_200_OK
#         return Response(response, status=status_code)       


# apres l'authentification avec google l'utilisateur de type avocat doit remplir ses informations personneles  


# class AvocatcompleteRegistrationView(CreateAPIView):
class AvocatcompleteRegistrationView(CreateAPIView):
    serializer_class = AvocatSerializer
    def post(self, request, *args, **kwargs):
        id_user = request.data.get('id_user')
        specialty = request.data.get('specialty')
        address = request.data.get('address')
        phone_number = request.data.get('phone_number')
        skills = request.data.get('skills')
        experiences = request.data.get('experiences')
        domaines_pratique = request.data.get('domaines_pratique')
        adresse_cabinet_avocats = request.data.get('adresse_cabinet_avocats')
        user = User.objects.filter(id=id_user).first()
        if user:
            # Mettre à jour le modèle User pour indiquer qu'il est un avocat
            user.is_avocat = True
            user.save()
            # Créer un objet Avocat associé à cet utilisateur
            avocat_instance = Avocat.objects.create(
                avocat=user,
                address=address,
                phone_number=phone_number,
                specialty=specialty,
                skills=skills,
                experiences=experiences,
                domaines_pratique=domaines_pratique,
                adresse_cabinet_avocats=adresse_cabinet_avocats
            )
            # Utilisez votre sérialiseur pour renvoyer une réponse JSON
            serializer = AvocatSerializer(avocat_instance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "Utilisateur non trouvé"}, status=status.HTTP_404_NOT_FOUND)


class ClientcompleteRegistrationView(CreateAPIView):
    serializer_class = ClientSerializer
    def post(self, request, *args, **kwargs):
        id_user = request.data.get('id_user')
        address = request.data.get('address')
        phone_number = request.data.get('phone_number')
        user = User.objects.filter(id=id_user).first()
        if user:
            # Mettre à jour le modèle User pour indiquer qu'il est un avocat
            user.is_client = True
            user.save()
            # Créer un objet Avocat associé à cet utilisateur
            client_instance = Client.objects.create(
                client=user,
                address=address,
                phone_number=phone_number,
            )
            # Utilisez votre sérialiseur pour renvoyer une réponse JSON
            serializer = ClientSerializer(client_instance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "Utilisateur non trouvé"}, status=status.HTTP_404_NOT_FOUND)

class AdmincompleteRegistrationView(CreateAPIView):
    serializer_class = AdminSerializer
    def post(self, request, *args, **kwargs):
        id_user = request.data.get('id_user')
        address = request.data.get('address')
        area = request.data.get('area')
        phone_number = request.data.get('phone_number')
        user = User.objects.filter(id=id_user).first()
        if user:
            # Mettre à jour le modèle User pour indiquer qu'il est un avocat
            user.is_admin = True
            user.save()
            # Créer un objet Avocat associé à cet utilisateur
            admin_instance = Admin.objects.create(
                admin=user,
                area=area,
                address=address,
                phone_number=phone_number,
            )
            # Utilisez votre sérialiseur pour renvoyer une réponse JSON
            serializer = AdminSerializer(admin_instance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "Utilisateur non trouvé"}, status=status.HTTP_404_NOT_FOUND)            



@api_view(['GET'])
def get_one_avocat(request,pk):
    avocat = Avocat.objects.filter(id=pk).first()
    avocat_data = {
            'first_name': avocat.avocat.first_name,
            'last_name': avocat.avocat.last_name,
            'email': avocat.avocat.email,
            'specialty': avocat.specialty,
            'address': avocat.address,
            'phone_number': avocat.phone_number,
            'skills': avocat.skills,
            'experiences': avocat.experiences,
            'domaines_pratique': avocat.domaines_pratique,
            'adresse_cabinet_avocats': avocat.adresse_cabinet_avocats,
            }
    if request.method == 'GET':
        return JsonResponse({'avocats': avocat_data})

@api_view(['GET'])
def get_avocat(request):
    avocats = Avocat.objects.all()
    avocats_list = []
    for avocat in avocats:
        avocat_data = {
            'user_id':avocat.id,
            'first_name': avocat.avocat.first_name,
            'last_name': avocat.avocat.last_name,
            'email': avocat.avocat.email,
            'specialty': avocat.specialty,
            'address': avocat.address,
            'phone_number': avocat.phone_number,
            'skills': avocat.skills,
            'experiences': avocat.experiences,
            'domaines_pratique': avocat.domaines_pratique,
            'adresse_cabinet_avocats': avocat.adresse_cabinet_avocats,
            }
        avocats_list.append(avocat_data)
    if request.method == 'GET':
        return JsonResponse({'avocats': avocats_list})

class Rendez_vous_view(CreateAPIView):
    serializer_class = Rendez_vous_Serializer
    def post(self, request, *args, **kwargs):
        print('request',request.data)
        avocat_id = request.data.get('avocat')
        print('avocat_id ',avocat_id )
        user_id = request.data.get('client')
        
        date = request.data.get('day')
        print('date ',date )

        time = request.data.get('time')  # Access the first element of the list
        print('time ',time )

        # Fix the typo here: 'Avoact' should be 'Avocat'

        x=User.objects.filter(id=user_id).first() 
        client = Client.objects.filter(client=x).first()
        
        print('client',client)
        avocat = get_object_or_404(Avocat, id=avocat_id)
        print('avocat',avocat)
        rendez_vous = Rendez_vous.objects.create(
            client=client,
            avocat=avocat,
            day=date,
            time=time
        )
        serializer = Rendez_vous_Serializer(rendez_vous)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
