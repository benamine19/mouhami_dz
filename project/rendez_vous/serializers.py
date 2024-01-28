from rest_framework import serializers
from users.models import Rendez_vous,Commentaire,Question

class Rendez_vous_Serializer(serializers.ModelSerializer):
    class Meta :
        model = Rendez_vous
        fields = '__all__'

class Commentaire_Serializer(serializers.ModelSerializer):
    class Meta :
        model = Commentaire
        fields = '__all__'

class Question_Serializer(serializers.ModelSerializer):
    class Meta :
        model = Question
        fields = '__all__'






