from django.urls import path,include
from .views import mes_rendez_vous_client,mes_rendez_vous_avocat,commentaires_avocat,coomentaire_view,Question_view
urlpatterns = [
    path('mes_rendez_vous_client_view/<int:pk>/',mes_rendez_vous_client,name='mes_rendez_vous_client'),
    path('commentaires_avocat/<int:pk>/',commentaires_avocat,name='commentaires_avocat'),
    path('coomentaire_view/',coomentaire_view.as_view(),name='coomentaire_view'),
    path('Question_view/',Question_view.as_view(),name='Question_view'),
]