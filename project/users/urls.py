from django.urls import path,include
from .views import GoogleSigninview,ClientRegistrationView,login_view,AdminRegistrationView,AvocatRegistrationView,UsersList,AvocatcompleteRegistrationView,ClientcompleteRegistrationView,AdmincompleteRegistrationView,get_avocat,get_one_avocat,Rendez_vous_view
urlpatterns = [
    path('signup/client/',ClientRegistrationView.as_view(),name='client_doctor'),
    path('signup/avocat/',AvocatRegistrationView.as_view(),name='client_doctor'),
    path('signup/admin/',AdminRegistrationView.as_view(),name='client_docr'),
    path('AvocatcompleteRegistrationView/',AvocatcompleteRegistrationView.as_view(),name='clioctor'),
    path('ClientcompleteRegistrationView/',ClientcompleteRegistrationView.as_view(),name='ClientcompleteRegistrationView'),
    path('AdmincompleteRegistrationView/',AdmincompleteRegistrationView.as_view(),name='AdmincompleteRegistrationView'),

    path('get_avocats/',get_avocat,name='get_avocat'),
    path('get_one_avocat/<int:pk>',get_one_avocat,name='get_one_avocat'),

    path('login/',login_view,name='get_avocat'),
    path('users_list/',UsersList.as_view(),name='Userslist'),
    path('GoogleSigninview/',GoogleSigninview.as_view(),name='GoogleSigninview'),
    path('rendez_vous_view/', Rendez_vous_view.as_view(), name='rendez_vous_view'),   
    
]