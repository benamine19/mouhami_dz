from django.shortcuts import render
from .serializers import Rendez_vous_Serializer,Commentaire_Serializer,Question_Serializer
from users.models import Rendez_vous ,Client,Avocat,Commentaire,Question,User
from rest_framework import generics,status
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view


# Create your views here.




@api_view(['GET'])
def mes_rendez_vous_client(request, pk):
        client = get_object_or_404(Client, id=pk)
        mes_rendez_vous=Rendez_vous.objects.filter(client=client)
        if request.method == 'GET':
            serializer = Rendez_vous_Serializer(mes_rendez_vous, many=True)
            return Response(serializer.data)

@api_view(['GET'])
def mes_rendez_vous_avocat(request, pk):
        avocat = get_object_or_404(Avocat, id=pk)
        mes_rendez_vous=Rendez_vous.objects.filter(avocat=avocat)
        if request.method == 'GET':
            serializer = Rendez_vous_Serializer(mes_rendez_vous, many=True)
            return Response(serializer.data)


class coomentaire_view(CreateAPIView):
    serializer_class = Rendez_vous_Serializer
    def post(self, request, *args, **kwargs):
        avocat_id = request.data.get('avocat')
        client_id = request.data.get('client')
        description = request.data.get('description')
        client = get_object_or_404(Client, id=client_id)
        avocat = get_object_or_404(Avocat, id=avocat_id)
        commentaire = Commentaire.objects.create(
            client=client,
            avocat=avocat,
            description=descripton,
        )
        serializer =Commentaire(commentaire)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def commentaires_avocat(request, pk):
        avocat = get_object_or_404(Avocat, id=pk)
        commentaires=Commentaire.objects.filter(avocat=avocat)
        if request.method == 'GET':
            serializer = Commentaire_Serializer(mes_rendez_vous, many=True)
            return Response(serializer.data)


class Question_view(CreateAPIView):
    serializer_class = Question_Serializer
    def post(self, request, *args, **kwargs):
        avocat_id = request.data.get('avocat')
          # Access the first element of the list
        user_id = request.data.get('client')
          # Access the first element of the list
        description = request.data.get('description')
        x=User.objects.filter(id=user_id).first() 
        
        client = Client.objects.filter(client=x).first()        
        avocat = get_object_or_404(Avocat, id=avocat_id)
        question = Question.objects.create(
            client=client,
            avocat=avocat,
            description=description
        )
        serializer = Question_Serializer(question)
        return Response(serializer.data, status=status.HTTP_201_CREATED)